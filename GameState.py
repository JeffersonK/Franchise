#import random
#import ProbabilityEngine as PrEng
from FieldGameState import *
from Player import *
import PlayerDB
import AtBatResult
from Globals import *

########################
#
#
#
#
########################
class GameState:
   
    def __init__(self, HomeTeam, AwayTeam, playerDB):

        #this is a reference to the global object
        #that acts as the caching interface to persistent player
        #objects
        self.__playerDB = playerDB

        self.__fieldGameState = DefensiveFieldState(BasesState(), 0)

        self.__HomeTeam = HomeTeam
        self.__AwayTeam = AwayTeam

        self.__inning = 1
        self.__homeTeamUp = False

        self.__gameEventLog = []

    def __str__(self):
        header    =  "--- H:%d A:%d in %s of %d %d outs ---\n" % (self.__HomeTeam.getRunsScored(), 
                                                                  self.__AwayTeam.getRunsScored(), 
                                                                  "bottom" if self.__homeTeamUp else "top", 
                                                                  self.__inning, 
                                                                  self.__fieldGameState.getNumOuts())

        second =     "              %d    \n" % self.__fieldGameState.playerOn(2)
        thirdfirst = "           %d  %d  %d\n" % (self.__fieldGameState.playerOn(3), 
                                                  self._getPitcherGUID(), 
                                                  self.__fieldGameState.playerOn(1))
        home =       "              %d    \n" % self.__fieldGameState.playerOn(0)
        return header + second + thirdfirst + home
    

    def _getNextBatterGUID(self):
        offenseTeamObj = self._getOffenseTeamObject()
        return offenseTeamObj.getNextBatterGUID()
    
    def _getPlayerAbilities(self, guid):
        player = self.__playerDB.getObjectHandle(guid)
        if player != None:
            return player.getPlayerAbilities()
        return None

    def _getPitcherGUID(self):
        defenseTeamObj = self._getDefenseTeamObject()
        return defenseTeamObj.getCurrentPitcherGUID()

    def _appendGameEvents(self, eventList):
        self.__gameEventLog += eventList

    def _logGameEvent(self, eventStr):
        self.__gameEventLog += [eventStr]
            
    def _isScoreEqual(self):
        return self.__HomeTeam.getRunsScored() == self.__AwayTeam.getRunsScored()

    def _isEndGame(self):
        if self.__inning < gsMAXGAMEINNINGS:
            return False

        if self._isScoreEqual():
            return False

        if self.__homeTeamUp and \
                self.__fieldGameState.getNumOuts() == gsOUTSPERINNING:
            return True

        if self.__homeTeamUp and \
                self.__HomeTeam.getRunsScored() > self.__AwayTeam.getRunsScored():
            return True

        return False

    def _isEndTeamAtBat(self):
        return self.__fieldGameState.isChangeSides()

    #should only called if we know its the end of the inning
    #should return whether end of game
    def handleChangeSides(self): #"handleEndInning()

        #DEBUG
        #print "--- CHANGE SIDES --- (homeTeamUp:%s)" % self.__homeTeamUp

        #DEBUG
        #if not self._isEndTeamAtBat():
        #    print "Called Handled Change Sides when not isEndTeamAtBat()\n"

        if self._isEndGame():
            return True

        if self.__homeTeamUp:
            self._logGameEvent("end of inning %d." % self.__inning)
            self.__inning += 1

        self.__homeTeamUp = not self.__homeTeamUp

        #NEW
        self.__fieldGameState.reset()

        return self._isEndGame()
    
    def _getOffenseTeamObject(self):

        offenseTeam = None

        if self.__homeTeamUp:
            offenseTeam = self.__HomeTeam
        else:
            offenseTeam = self.__AwayTeam

        return offenseTeam

    def _getDefenseTeamObject(self):

        defenseTeam = None

        if not self.__homeTeamUp:
            defenseTeam = self.__HomeTeam
        else:
            defenseTeam = self.__AwayTeam

        return defenseTeam

    #who scored is implicit from who is up
    #should return whether end of game
    def handleTeamScored(self, atBatResultObj):
        
        offenseTeam = self._getOffenseTeamObject()
        
        runnersScoredList = atBatResultObj.getRunnersScored()

        #DEBUG
        #if runnersScoredList == None or len(runnersScoredList) == 0:
        #    print "DEBUG: handleTeamScored called but runnersScored list is empty\n"

        #need to check for case of HR because if its a walkoff
        #all runs score
        if atBatResultObj.HomeRun():

            offenseTeam.incRunsScored(len(runnersScoredList))
            if len(runnersScoredList) == 1:
                atBatResultObj.logAtBatEvent("%d hit a HR." % (atBatResultObj.getBatterGUID()))

            else:
                if len(runnersScoredList) == 4:
                    atBatResultObj.logAtBatEvent("%d hit a GRANDSLAM HR." % (atBatResultObj.getBatterGUID()))
                else:
                    atBatResultObj.logAtBatEvent("%d hit a %d run HR." % (atBatResultObj.getBatterGUID(), len(runnersScoredList)))
                
                for runnerGUID in runnersScoredList:#[0:-1]:
                    atBatResultObj.logAtBatEvent("%d scores." % runnerGUID)
                    plyr = self.__playerDB.getObjectHandle(runnerGUID)
                    if plyr != None:
                        plyr.incRunsScored()
                        plyr = None
                        
            return self._isEndGame()

        #case of not HR, need to score them one at a time
        #because if its the bottom of the ninth the score stop
        #incrementing after the winning run comes in
        for runnerGUID in runnersScoredList:
            offenseTeam.incRunsScored(1)

            plyr = self.__playerDB.getObjectHandle(runnerGUID)
            if plyr != None:
                plyr.incRunsScored()
            plyr = None

            atBatResultObj.logAtBatEvent("%d scores." % runnerGUID)
            if self._isEndGame():
                return True
            
        return self._isEndGame()

    #pass the number of outs just made
    #should return (bool:is end of inning, bool:is end game) 
    #valid return states:
    #(true, true) 
    #(true, false)
    #(false, false)
    def _handleOut(self, atBatResultObj):

        OLD = """if atBatResultObj.StrikeOut():
            self.__outs += 1

        elif atBatResultObj.GroundOut():
            self.__outs += 1

        elif atBatResultObj.FlyOut():
            self.__outs += 1

        elif atBatResultObj.SacrificeOut():
            self.__outs += 1

        elif atBatResultObj.DoublePlay():
            self.__outs += 2
            
        elif atBatResultObj.TriplePlay():
            self.__outs += 3

        else:
            print "handleOut received a non-Out event (%s)\n" % resultCode"""

        return (self._isEndTeamAtBat(), self._isEndGame())

    def getGameEvents(self):
        return []

    #endSim()
    #don't reset state because successive 
    #calls to isSimDone() must
    #all be true
    def handleEndGame(self):
        #generate appropriate events
        #update pitcher record
        #update team record
        
        #don't copy Games stats into Players Stats
        #person who ran the sim should pass TeamGameState to Franchise object
        print self.__gameEventLog
        print "FINAL SCORE: H:%d A:%d" % (self.__HomeTeam.getRunsScored(), self.__AwayTeam.getRunsScored())
        #TODO: return 'GAMEOVER' event
        return ['GAMEOVER']

    #startSim()
    def handleStartGame(self):
        #TODO: give the pitchers the start
        self.__fieldGameState.reset()
        return ['GAMESTART'] #gameStateEvent('Start Game')

    def handleStartAtBat(self):

        self.__fieldGameState.setBatterGUID(self._getNextBatterGUID())
        
        #DEBUG
        print self

    def handleAtBatResult(self, atBatEventObj):
        #if hit:
        #if atBatEventObj.runnersAdvance():
            #self._handleAdvanceAllRunners(atBatEventObj)
            
        if atBatEventObj.teamScored():
            isGameOver = self.handleTeamScored(atBatEventObj) 
            #can't exit here because game could end
            #on SAC out in which case we need to record the out

        #handleOut        
        if atBatEventObj.isOut():
            (endTeamAtBat, endGame) = self._handleOut(atBatEventObj)
            return (endTeamAtBat, endGame)

        return (False, False)

    #update the play log
    def handleEndAtBat(self, atBatEventObj):
        
        teamObj = self._getOffenseTeamObject()

        teamObj.advanceBattingLineup()
        
        #here is where you update playerGameState Stats
        teamObj.updateTeamGameState(atBatEventObj, True)
        
        defTeamObj = self._getDefenseTeamObject()

        #print "Updating Defensive Team State"
        defTeamObj.updateTeamGameState(atBatEventObj, False)
        
        self._appendGameEvents(atBatEventObj.atBatEventLog())

        #DEBUG
        print atBatEventObj
        #print self
        
        return

    #should be called before handleStartAtBat or after handleEndAtBat() 
    #so that the 0th element in the list is gsBASEEMPTY
    def _getStateForNextAtBatEvent(self):
        return self.__fieldGameState#(self.__outs, len([p for p in self.__bases[1:] if p != gsBASEEMPTY]))

    #
    # IMPLEMENT THE SIM RUNNER INTERFACE
    #
    #    
    def generateSimEvent(self):

        batterGUID = self._getNextBatterGUID()
        batterAbilities = self._getPlayerAbilities(batterGUID)
        if batterAbilities == None:
            print "could't get batter abilities"
            return None
        
        pitcherGUID = self._getPitcherGUID()
        pitcherAbilities = self._getPlayerAbilities(pitcherGUID)
        if pitcherAbilities == None:
            print "could't get pitcher abilities"
            return None

        
        atBatEvent = AtBatResult.AtBatResult(self._getNextBatterGUID(),
                                             batterAbilities,
                                             self._getPitcherGUID(),
                                             pitcherAbilities,
                                             self._getStateForNextAtBatEvent())

        
        atBatEvent.simAtBat()          

        return atBatEvent

    def initSim(self):
        events = self.handleStartGame()
        return events

    def isSimDone(self):
        return self._isEndGame()

    def stepSim(self):#, simEvent):

        if self.isSimDone():
            return "GAMEOVER"

        self.handleStartAtBat()     

        atBatEvent = self.generateSimEvent()

        (changeSides, gameOver) = self.handleAtBatResult(atBatEvent)

        self.handleEndAtBat(atBatEvent)

        if gameOver:
            return ["GAMEOVER"] #gameStateEvent().setGameOver()

        if changeSides:
            self.handleChangeSides()

        #if sim finish return True        
        #TODO: generate a real event
        if len(self.__gameEventLog) > 0:
            return [self.__gameEventLog[-1]] #gameEvents()
        return []

    def finishSim(self):
        gameStateEvents = self.handleEndGame()
        return gameStateEvents


    #sets list of playerGUIDs that scored [3,6] in the event object
    #if was a HomeRun includes man at bat in list
    OLD = """def _handleAdvanceAllRunners(self, atBatResultObj):
        
        runnersScored = []
        basesReversed = self.__bases[:]
        basesReversed.reverse()

        if atBatResultObj.Single():

            runnersScored = [basesReversed[0]]
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY] + self.__bases[0:3]
            
        elif atBatResultObj.Double():
            
            runnersScored = basesReversed[0:2]
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY]*2 + self.__bases[0:2]
         
        elif atBatResultObj.Triple():

            runnersScored = basesReversed[0:3]
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY]*3 + [self.__bases[0]]

        elif atBatResultObj.HomeRun():

            runnersScored = basesReversed
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY]*4

        elif atBatResultObj.Walk() or atBatResultObj.HitByPitch():
            
            if not self._manOn(1):
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = gsBASEEMPTY
                
            elif self._manOn(1) and not self._manOn(2):
                self.__bases[2] = self.__bases[1]
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = gsBASEEMPTY

            elif self._manOn(1) and self._manOn(2) and not self._manOn(3):
                self.__bases[3] = self.__bases[2]
                self.__bases[2] = self.__bases[1]
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = gsBASEEMPTY

            elif self._manOn(1) and self._manOn(2) and self._manOn(3):
                runnersScored = [self.__bases[3]]
                self.__bases = [gsBASEEMPTY] + self.__bases[0:3]

            else:
                print "DEBUG: Hit Default Case in _handleAdvanceAllRunners()\n"

        elif atBatResultObj.SacrificeOut():
            runnersScored = [basesReversed[0]]
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY]*2 + self.__bases[1:3]
        
        atBatResultObj.setRunnersScored(runnersScored)
        return #runnersScored"""
    

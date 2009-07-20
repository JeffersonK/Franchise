import random
import ProbabilityEngine as PrEng

nextPitch = 0
gsPitches = None
#nextSwing = 0
#gsSwings = None

####
#
#
####
class AtBatResult:

    gsBATTINGEVENTS = ['S','2B','3B','HR','BB','SO','HBP',
                       'GO','AO','SAC','DP','TP']#,'IBB']
    gsHITS = ['S','2B','3B','HR']
    gsNOTATBAT = ['BB','HBP']
    gsDONTADDPITCH = ['SO','BB']
    gsSINGLEOUTPLAYS = ['GO','SO','AO','SAC']
    gsMULTIOUTPLAYS = ['DP','TP']
    gsOUTEVENTS = gsSINGLEOUTPLAYS + gsMULTIOUTPLAYS
    gsRUNNERSADVANCEEVENTS = gsHITS + ['BB','HBP','SAC']
    gsMAXPITCHCOUNT = 10

    def __init__(self, 
                 batterGUID, 
                 pitcherGUID,
                 currentState): #(numOuts, numOnBase)
            
        self.__pitcher_playerGUID = pitcherGUID
        self.__batter_playerGUID = batterGUID

        self.__currentState = currentState

        #we have to copy this because we are going to modify it
        self.__allowedEvents = self.gsBATTINGEVENTS[:]

        #initialize pitch counts
        self.__fouls = 0
        self.__strikeCount = 0
        self.__ballCount = 0
        self.__totPitches = 0

        self.__contactMade = False

        #fill these in later
        self.__atBatEventLog = [] #list of strings
        self.__runnersOut = [] 
        self.__runnersScored = [] #[playerGUID,]

        global gsPitches
        global gsSwings

        if gsPitches == None:
             file = open("pitch.loc", "r")
             pitches = file.readline()
             file.close()
             gsPitches = eval(pitches)

        #if gsSwings == None:
        #    file = open("swing.loc", "r")
        #    swings = file.readline()
        #    file.close()
        #    gsSwings = eval(swings)


    def _getNextPitch(self):
        global gsPitches
        global nextPitch
        #print gsPitches[nextPitch]
        nextPitch += 1
        return gsPitches[nextPitch]

    #def _getNextSwing(self):
    #    global gsSwings
    #    global nextSwing
    #    print gsSwings[nextSwing]
    #    nextSwing += 1
    #    return gsSwings[nextSwing]

    def simAtBat(self):
        while 1:
            pitchZone = self._getNextPitch()
            self.__totPitches += 1

            if pitchZone == 9:
                self.__ballCount += 1

            
            else:
                pr = PrEng.PrContact(PrEng.pitcherAbil, 
                                     PrEng.batterAbil,
                                     ('fastball', pitchZone))

                r = random.randint(0,999)
                if r <= (pr * 1000):
                    #fuckin' contact!
                    self.__contactMade = True
                    self._generateAtBatResult()
                    return

                else:
                    #he whiff'd!
                    self.__strikeCount += 1

            if self.__strikeCount == 3:
                self.__resultCode = 'SO'
                return

            if self.__ballCount == 4:
                self.__resultCode = 'BB'
                return
            
        return

    def _simAtBat(self):
        #TODO: handle fouls and HBP
        while 1:            
            pitch = self._getNextPitch()
            self.__totPitches += 1

            swing = self._getNextSwing()

            if pitch == 0 and swing in range(0,5):
                #or HBP
                self.__ballCount += 1
            
            elif pitch == 0 and swing != 0:
                self.__strikeCount += 1  
            
            elif pitch == swing:
             #contact
                self._generateAtBatResult()
                return

            else:
                self.__strikeCount += 1

            if self.__strikeCount == 3:
                self.__resultCode = 'SO'
                return

            if self.__ballCount == 4:
                self.__resultCode = 'BB'
                return
            
        return

    def _findAllowedEvents(self):
        (numOuts, numOnBase) = self.__currentState

        #allowedEvents = self.gsBATTINGEVENTS[:]
        if numOuts == 2 or numOnBase == 0:
            self.__allowedEvents.remove('SAC')
            self.__allowedEvents.remove('DP')
            self.__allowedEvents.remove('TP')

        elif numOuts <= 1 and numOnBase > 0:
            if numOuts == 0 and numOnBase >= 2:
                #allowedEvents = allowedEvents
                None
            else:
                self.__allowedEvents.remove('SAC')
                self.__allowedEvents.remove('TP')

        if self.__strikeCount < 3:
            self.__allowedEvents.remove('SO')

        if self.__ballCount < 4:
            self.__allowedEvents.remove('BB')
        
        if self.__contactMade:
            self.__allowedEvents.remove('HBP')

        return

    def _generateAtBatResult(self):
        self._findAllowedEvents()

        if self.__ballCount == 4:
            self.__resultCode == 'BB'
            return

        if self.__strikeCount == 3:
            self.__resultCode == 'SO'
            return
        
        random.seed()
        r = random.randint(0,len(self.__allowedEvents)-1)
        self.__resultCode = self.__allowedEvents[r]
        return

    def RANDOMLYgeneratePitchCount(self):

        #generate pitches
        if self.__resultCode == 'SO':
            self.__strikeCount = 3     
            self.__ballCount = random.randint(0,3)

        elif self.__resultCode == 'BB':
            self.__strikeCount = random.randint(0,2)     
            self.__ballCount = 4
            
        else:
            self.__strikeCount = random.randint(0,2)     
            self.__ballCount = random.randint(0,3)     

        if self.__strikeCount >= 2:
            self.__fouls = random.randint(self.__ballCount + self.__strikeCount,
                                          self.gsMAXPITCHCOUNT)
            self.__totPitches = self.__ballCount + self.__strikeCount + self.__fouls
        else:
            self.__totPitches = self.__ballCount + self.__strikeCount
            
        if self.__resultCode == 'HBP':
            self.__ballCount += 1

        if self.__resultCode not in self.gsDONTADDPITCH:
            self.__totPitches += 1

    
        #fill these in later
        self.__atBatEventLog = [] #list of strings
        self.__runnersOut = [] 
        self.__runnersScored = [] #[playerGUID,]

        return
    
    def __str__(self):
        return "%d - %s" % ( self.__batter_playerGUID, self.__resultCode)


    def logAtBatEvent(self, eventStr):
        self.__atBatEventLog += [eventStr]

    def atBatEventLog(self):
        return self.__atBatEventLog

    def isOut(self):
        return self.__resultCode in self.gsOUTEVENTS

    def outsMade(self):
        if self.__resultCode in self.gsSINGLEOUTPLAYS:
            return 1

        if self.DoublePlay():
            return 2

        if self.TriplePlay():
            return 3

        return 0

    def countsAsAtBat(self):
        return self.__resultCode not in self.gsNOTATBAT

    def runsScored(self):
        return len(self.__runnersScored)

    def runnersAdvance(self):
        return self.__resultCode in self.gsRUNNERSADVANCEEVENTS

    def teamScored(self):
        return len(self.__runnersScored) > 0

    def Single(self):
        return self.__resultCode == 'S'

    def isHit(self):
        return self.__resultCode in self.gsHITS

    def Double(self):
        return self.__resultCode == '2B'

    def Triple(self):
        return self.__resultCode == '3B'

    def HomeRun(self):
        return self.__resultCode == 'HR'

    def Walk(self):
        return self.__resultCode == 'BB'

    def HitByPitch(self):
        return self.__resultCode == 'HBP'

    def StrikeOut(self):
        return self.__resultCode == 'SO'

    def GroundOut(self):
        return self.__resultCode == 'GO'

    def FlyOut(self):
        return self.__resultCode == 'AO'

    def SacrificeOut(self):
        return self.__resultCode == 'SAC'

    def DoublePlay(self):
        return self.__resultCode == 'DP'

    def TriplePlay(self):
        return self.__resultCode == 'TP'

    def setRunnersScored(self, runnerGUIDList):
        self.__runnersScored = runnerGUIDList

    def getRunnersScored(self):
        return self.__runnersScored

    def getResultCode(self):
        return self.__resultCode

    def getPitcherGUID(self):
        return self.__pitcher_playerGUID

    def getBatterGUID(self):
        return self.__batter_playerGUID

    #def getStrikesThrown(self):
    #    return self.__strikes + self.__fouls

    #def getTotPitches(self):
    #    return self.__totPitches

    def getPitchCounts(self):
        return (self.__totPitches, self.__strikeCount + self.__fouls, self.__ballCount)


########################
#
#
#
#
########################
class GameState:
   

    gsMAXGAMEINNINGS = 9
    gsOUTSPERINNING = 3
    gsBASEEMPTY = -1
   

    def __init__(self, HomeTeam, AwayTeam):

        self.__HomeTeam = HomeTeam
        self.__AwayTeam = AwayTeam
        self.__bases = [self.gsBASEEMPTY]*4
        self.__inning = 1
        self.__homeTeamUp = False
        self.__outs = 0

        self.__gameEventLog = []

    def __str__(self):
        header    =  "H:%d - A:%d  %s of %d  %d outs\n" % (self.__HomeTeam.getRunsScored(), self.__AwayTeam.getRunsScored(), "bottom" if self.__homeTeamUp else "top", self.__inning, self.__outs)
        second =     "              %d    \n" % self.__bases[2]
        thirdfirst = "           %d  %d  %d\n" % (self.__bases[3], self._getPitcherGUID(), self.__bases[1])
        home =       "              %d    \n" % self.__bases[0]
        return header + second + thirdfirst + home
    
    def _getNextBatterGUID(self):
        
        if self.__homeTeamUp:
            return self.__HomeTeam.getNextBatterGUID()
        
        return self.__AwayTeam.getNextBatterGUID()
        

    def _getPitcherGUID(self):
        if self.__homeTeamUp:
            return self.__AwayTeam.getCurrentPitcherGUID()

        return self.__HomeTeam.getCurrentPitcherGUID()

    def _appendGameEvents(self, eventList):
        self.__gameEventLog += eventList

    def _logGameEvent(self, eventStr):
        self.__gameEventLog += [eventStr]

    def _manOn(self, n):
        return self.__bases[n] != self.gsBASEEMPTY
            
    def _isScoreEqual(self):
        return self.__HomeTeam.getRunsScored() == self.__AwayTeam.getRunsScored()

    def _isEndGame(self):
        if self.__inning < self.gsMAXGAMEINNINGS:
            return False

        if self._isScoreEqual():
            return False

        if self.__homeTeamUp and self.__outs == self.gsOUTSPERINNING:
            return True

        if self.__homeTeamUp and self.__HomeTeam.getRunsScored() > self.__AwayTeam.getRunsScored():
            return True

        return False

    def _isEndTeamAtBat(self):
        
        if self.__outs > 3:
            while 1:
                mynuts = 0
        return self.__outs == self.gsOUTSPERINNING

    #should only called if we know its the end of the inning
    #should return whether end of game
    def handleChangeSides(self): #"handleEndInning()

        #DEBUG
        if not self._isEndTeamAtBat():
            print "Called Handled Change Sides when not isEndTeamAtBat()\n"

        if self._isEndGame():
            return True

        if self.__homeTeamUp:
            self._logGameEvent("end of inning %d." % self.__inning)
            self.__inning += 1

        self.__bases = [self.gsBASEEMPTY]*4
        self.__homeTeamUp = not self.__homeTeamUp
        self.__outs = 0
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
        if runnersScoredList == None or len(runnersScoredList) == 0:
            print "handleTeamScored called but runnersScored list is empty\n"

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
                
            
            return self._isEndGame()

        #case of not HR
        for runnerGUID in runnersScoredList:
            offenseTeam.incRunsScored(1)
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

        #TODO: add event logging
        if atBatResultObj.StrikeOut():
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
            print "handleOut received a non-Out event (%s)\n" % resultCode

        return (self._isEndTeamAtBat(), self._isEndGame())

    #sets list of playerGUIDs that scored [3,6] in the event object
    #if was a HomeRun includes man at bat in list
    def _handleAdvanceAllRunners(self, atBatResultObj):
        

        runnersScored = []
        basesReversed = self.__bases[:]
        basesReversed.reverse()

        if atBatResultObj.Single():

            runnersScored = [basesReversed[0]]
            runnersScored = [runner for runner in runnersScored if runner != self.gsBASEEMPTY]            
            self.__bases = [self.gsBASEEMPTY] + self.__bases[0:3]
            
        elif atBatResultObj.Double():
            
            runnersScored = basesReversed[0:2]
            runnersScored = [runner for runner in runnersScored if runner != self.gsBASEEMPTY]            
            self.__bases = [self.gsBASEEMPTY]*2 + self.__bases[0:2]
         
        elif atBatResultObj.Triple():

            runnersScored = basesReversed[0:3]
            runnersScored = [runner for runner in runnersScored if runner != self.gsBASEEMPTY]            
            self.__bases = [self.gsBASEEMPTY]*3 + [self.__bases[0]]

        elif atBatResultObj.HomeRun():

            runnersScored = basesReversed
            runnersScored = [runner for runner in runnersScored if runner != self.gsBASEEMPTY]            
            self.__bases = [self.gsBASEEMPTY]*4

        elif atBatResultObj.Walk() or atBatResultObj.HitByPitch():
            
            if not self._manOn(1):
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = self.gsBASEEMPTY
                
            elif self._manOn(1) and not self._manOn(2):
                self.__bases[2] = self.__bases[1]
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = self.gsBASEEMPTY

            elif self._manOn(1) and self._manOn(2) and not self._manOn(3):
                self.__bases[3] = self.__bases[2]
                self.__bases[2] = self.__bases[1]
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = self.gsBASEEMPTY

            elif self._manOn(1) and self._manOn(2) and self._manOn(3):
                runnersScored = [self.__bases[3]]
                self.__bases = [self.gsBASEEMPTY] + self.__bases[0:3]

            else:
                print "DEBUG: Hit Default Case in _handleAdvanceAllRunners()\n"

        elif atBatResultObj.SacrificeOut():
            runnersScored = [basesReversed[0]]
            runnersScored = [runner for runner in runnersScored if runner != self.gsBASEEMPTY]            
            self.__bases = [self.gsBASEEMPTY]*2 + self.__bases[1:3]
        
        atBatResultObj.setRunnersScored(runnersScored)
        return #runnersScored
    
    def getGameEvents(self):
        #self.__HomeTeam.getRunsScored()
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
        
        #TODO: return 'GAMEOVER' event
        return ['GAMEOVER']

    #startSim()
    def handleStartGame(self):
        #give the pitchers the start
        
        return ['Game Start'] #gameStateEvent('Start Game')

    def handleStartAtBat(self, atBatEventObj):
        #put batter in 0th place 
        self.__bases[0] = atBatEventObj.getBatterGUID()
        return

    def handleAtBatResult(self, atBatEventObj):
        #if hit:
        if atBatEventObj.runnersAdvance():
            self._handleAdvanceAllRunners(atBatEventObj)

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

        #need to do for AO and SO because handleRunnerAdvanced is not called
        self.__bases[0] = self.gsBASEEMPTY

        #here is where you update playerGameState Stats
        teamObj.updateTeamGameState(atBatEventObj, True)
        
        defTeamObj = self._getDefenseTeamObject()

        defTeamObj.updateTeamGameState(atBatEventObj, False)

        
        self._appendGameEvents(atBatEventObj.atBatEventLog())

        print teamObj.printPlayerGameState(atBatEventObj.getBatterGUID())

        
        return

    #should be called before handleStartAtBat or after handleEndAtBat() 
    #so that the 0th element in the list is gsBASEEMPTY
    def _getStateForNextAtBatEvent(self):
        return (self.__outs, len([p for p in self.__bases[1:] if p != self.gsBASEEMPTY]))

    #
    # IMPLEMENT THE SIM RUNNER INTERFACE
    #
    #
    
    def generateSimEvent(self):
        
        atBatEvent = AtBatResult(self._getNextBatterGUID(),
                                 self._getPitcherGUID(),
                                 self._getStateForNextAtBatEvent())

        atBatEvent.simAtBat()          
        #atBatEvent.generateAtBatResult()

        #print atBatEvent
        return atBatEvent

    def initSim(self):
        events = self.handleStartGame()
        return events

    def isSimDone(self):
        return self._isEndGame()

    def stepSim(self):#, simEvent):

        if self.isSimDone():
            return "GAMEOVER"

        atBatEvent = self.generateSimEvent()

        self.handleStartAtBat(atBatEvent)     

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

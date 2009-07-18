import random
import Globals
import Player

####
#
#
####
class AtBatResult:

    def __init__(self, batterGUID, pitcherGUID, resultCode, totPitches, 
                 strikes, balls, fouls, runsScored):
        self.__pitcher_playerGUID = pitcherGUID
        self.__batter_playerGUID = batterGUID
        self.__resultCode = resultCode
        self.__ballCount = balls
        self.__strikeCount = strikes
        self.__totPitches = totPitches
        self.__fouls = fouls
        self.__runsScored = runsScored
        #DEBUG
        #print "%s - (%d-%d):%d\n" % (self.__resultCode, self.__ballCount, 
        #                             self.__strikeCount, self.__fouls)

        return
    
    #def __str__(self):
    #    return ""

    def incRunsScored(self):
        self.__runsScored += 1
        return self.__runsScored

    def getResultCode(self):
        return self.__resultCode

    def getPitcherGUID(self):
        return self.__pitcher_playerGUID

    def getBatterGUID(self):
        return self.__batter_playerGUID

    def getStrikesThrown(self):
        return self.__strikes + self.__fouls

    def getTotPitches(self):
        return self.__totPitches

    def getPitchCounts(self):
        return (self.__totPitches, self.__strikeCount + self.__fouls, self.__ballCount)


########
#
#
########
class TeamGameState:
    
    def __init__(self, franchise):
        #last pitcher in this list is the current pitcher
        #list of tuples (number of outs, pitcher object)
        self.__pitchers = [] 
        self.__nextBatterIndex = 0
        self.__runsScored = 0
        self.__playerStates = {}
        self.__lineup = []
        self.__onFirst = Globals.gsBASEEMPTY #playerGUID
        self.__onSecond = Globals.gsBASEEMPTY #player GUID
        self.__onThird = Globals.gsBASEEMPTY #player GUID
        self.__nOnBase = 0
        self.__outs = 0
        
        nextPitcher = franchise.nextPitcherInRotation()
        self.__pitchers = [(0, nextPitcher)]

        for playerGUID in franchise.getPlayerGUIDs():
            self.__playerStates[playerGUID] = Player.PlayerGameState(playerGUID)
            
        self.__lineup = franchise.getLineup()

    def __str__(self):
        s = ""
        return s

    def getRunsScored(self):
        return self.__runsScored

    def updatePlayerState(self, playerGUID, playerGameState):
        if playerGUID not in self.__playerStates:
            return -1

        playerState = self.__playerStates[playerGUID]
        
    def getCurrentPitcherGUID(self):
        return self.__pitchers[-1][1]

    def _generatePitchCount(self, thisAtBatResultCode):
        ballCount = 0
        strikeCount = 0
        totPitches = 0
        numFouls = 0
        if thisAtBatResultCode == 'SO':
            strikeCount = 3
            ballCount = random.randint(0,3)
        elif thisAtBatResultCode == 'BB':
            ballCount = 4
            strikeCount = random.randint(0,2)
        else:
            ballCount = random.randint(0,3)
            strikeCount = random.randint(0,2)

        if strikeCount >= 2:
            numFouls = random.randint(ballCount + strikeCount, Globals.gsMAXPITCHCOUNT)
            totPitches = ballCount + strikeCount + numFouls
        else:
            totPitches = ballCount + strikeCount

        #must count the HBP event as a ball thrown
        if thisAtBatResultCode == 'HBP':
            ballCount += 1

        if thisAtBatResultCode not in Globals.gsDONTADDPITCH:
            totPitches += 1

        print "(%s) %d (%d-%d) %d\n" % (thisAtBatResultCode, totPitches, ballCount, strikeCount, numFouls)
        return (totPitches, strikeCount, ballCount, numFouls)

    def simAtBat(self, defenseTeamGameState):
        
        maxint =  len(Globals.gsBatterResults)-1
        if self.__nOnBase == 0 or self.__outs == 2:
            maxint = maxint - 3 #no SAC, DP, or TP
            
        elif self.__outs <= 1 and self.__nOnBase > 0:
            if self.__outs == 0 and self.__nOnBase >= 2:
                maxint = maxint #EVERYTHING
            else:
                maxint = maxint - 1 #SAC + DP
                

        r = random.randint(0, maxint)
        thisAtBatResultCode = Globals.gsBatterResults[r]
        
        #randomly generate pitch count
        (totPitches, strikeCount, ballCount, numFouls) = self._generatePitchCount(thisAtBatResultCode)
  
        return AtBatResult(self.__lineup[self.__nextBatterIndex], 
                           defenseTeamGameState.getCurrentPitcherGUID(),
                           thisAtBatResultCode,
                           totPitches, strikeCount, ballCount, numFouls, 0)
    
    #do some cleanup and reset some shit
    def endTeamAtBat(self):
        self._clearBaseState()
        self.__outs = 0
        return

    def endTeamInField(self):
        return

    def _getPlayerGUIDOnBase(self, base):
        if base == 1:
            return self.__onFirst 

        if base == 2:
            return self.__onSecond 

        if base == 3:
            return self.__onThird 

    def _getPlayerStateOn(self, base):
        guid = self._getPlayerGUIDOnBase(base)
        if guid == Globals.gsBASEEMPTY:
            return None
        
        if guid in self.__playerStates:
            return self.__playerStates[guid]
        
        #DEBUG
        print "DEBUG: STATE INCONSISTENCY - MAN ON BASE HAS NO PLAYER STATE!!!"
        return None

    #base is 1,2,3
    def _manOn(self, base):
        if base == 1:
            return self.__onFirst != Globals.gsBASEEMPTY

        if base == 2:
            return self.__onSecond != Globals.gsBASEEMPTY

        if base == 3:
            return self.__onThird != Globals.gsBASEEMPTY

    #def _scoreManOn(self, base):
    #    if not self._manOn(base):
    #        print "DEBUG: INCONSISTENCY - NO MAN ON BASE %d TO SCORE!!!" % base
    #        return
    #    playerState = self._getPlayerStateOn(base)
    #    playerState.incRunsScored()
    #    return

    def _setBaseState(self, onFirst, onSecond, onThird):
        #order here matters
        self.__onThird = onThird
        self.__onSecond = onSecond
        self.__onFirst = onFirst

        self.__nOnBase = 0
        for base in [self.__onThird, self.__onSecond, self.__onFirst]:
            if base != Globals.gsBASEEMPTY:
                self.__nOnBase += 1

    def _incOuts(self, n):
        self.__outs += n

    def _incTeamScore(self):
        self.__runsScored += 1
        return self.__runsScored

    def _clearBaseState(self):
        self._setBaseState(Globals.gsBASEEMPTY, Globals.gsBASEEMPTY, Globals.gsBASEEMPTY)

    def _getCurrentBatterGameState(self):
        return self.__playerStates[self.__lineup[self.__nextBatterIndex]]

    def _getCurrentPitcherGameState(self):
        return self.__playerStates[self.getCurrentPitcherGUID()]

    #side is 'offense' or 'defense'
    def updateDefenseTeamGameState(self, thisAtBatResult):
        return 0

    def updateOffenseTeamGameState(self, thisAtBatResult):
        
        batterGameState = self._getCurrentBatterGameState()
        pitcherGameState = self._getCurrentPitcherGameState()
        
#update pitcher state
    
    #update batter state
    #update offense game state
    
    #update defense gamesate

        #['S','2B','3B','HR','BB','SO','HBP','GO','AO','SAC','DP','TP']#,'IBB']        
        #DEBUG
            
        if 1:#side == 'offense':
            if thisAtBatResult.getResultCode() == 'SO':
                pitcherGameState.incKs()
                

            if thisAtBatResult.getResultCode() == 'S':
                batterGameState.incHits()
                pitcherGameState.incHitsAllowed()
                if self._manOn(3):

                    #update game state
                    self._incTeamScore()
                    #update pitcher states
                    pitcherGameState.incEarnedRuns()
                    
                    #update batter states
                    batterGameState.incRBIs()
                    batterGameState.incHits()
                
                    #increment player on 3rd runs scored
                    playerStateOnThird = self._getPlayerStateOn(3)
                    playerStateOnThird.incRunsScored()

                    #increment the atBatResult
                    thisAtBatResult.incRunsScored()
                    
                #no mattter what advance all 1 base
                self._setBaseState(self.__lineup[self.__nextBatterIndex],
                                   self.__onFirst,
                                   self.__onSecond)
            
            elif thisAtBatResult.getResultCode() == '2B':
                batterGameState.incHits()
                pitcherGameState.incHitsAllowed()
                #if man 3rd
                if self._manOn(3):
                    
                    #update game state
                    self._incTeamScore()

                    #update the pitcher states
                    pitcherGameState.incEarnedRuns()


                    batterGameState.incRBIs()

                    #increment player on 3rd runs scored
                    playerStateOnThird = self._getPlayerStateOn(3)
                    playerStateOnThird.incRunsScored()

                    #inc at bat result
                    thisAtBatResult.incRunsScored()
                     
                     
                #if man on 2nd
                if self._manOn(2):

                    self._incTeamScore()

                    pitcherGameState.incEarnedRuns()
                    batterGameState.incRBIs()
  
                    #increment player on 2nd runs scored
                    playerStateOnSecond = self._getPlayerStateOn(2)
                    playerStateOnSecond.incRunsScored()
                
                    thisAtBatResult.incRunsScored()

                #always advance everyone 2 bases
                self._setBaseState(Globals.gsBASEEMPTY,
                                    self.__lineup[self.__nextBatterIndex],
                                    self.__onFirst)

            
            elif thisAtBatResult.getResultCode() == '3B':
                batterGameState.incHits()
                pitcherGameState.incHitsAllowed()

                if self._manOn(3):
                    self._incTeamScore()
                    pitcherGameState.incEarnedRuns()
                    batterGameState.incRBIs()
                    #increment player on 3rd runs scored
                    playerStateOnThird = self._getPlayerStateOn(3)
                    playerStateOnThird.incRunsScored()
                    thisAtBatResult.incRunsScored()

                if self._manOn(2):
                    self._incTeamScore()
                    pitcherGameState.incEarnedRuns()
                    batterGameState.incRBIs()
                     #increment player on 2nd runs scored
                    playerStateOnSecond = self._getPlayerStateOn(2)
                    playerStateOnSecond.incRunsScored()
                    thisAtBatResult.incRunsScored()

                if self._manOn(1):
                    self._incTeamScore()
                    pitcherGameState.incEarnedRuns()
                    batterGameState.incRBIs()
                    #increment player on 1st runs scored
                    playerStateOnFirst = self._getPlayerStateOn(1)
                    playerStateOnFirst.incRunsScored()
                    thisAtBatResult.incRunsScored()

                self._setBaseState(Globals.gsBASEEMPTY,  Globals.gsBASEEMPTY, self.__lineup[self.__nextBatterIndex])
                
            elif thisAtBatResult.getResultCode() == 'HR':
                pitcherGameState.incHitsAllowed()
                pitcherGameState.incHRsAllowed()
                batterGameState.incHits()
                self._incTeamScore()
                pitcherGameState.incEarnedRuns()
                batterGameState.incRBIs()
                    
                if self._manOn(3):
                    self._incTeamScore()
                    pitcherGameState.incEarnedRuns()
                    batterGameState.incRBIs()
                    #increment player on 3rd runs scored
                    playerStateOnThird = self._getPlayerStateOn(3)
                    playerStateOnThird.incRunsScored()
                    thisAtBatResult.incRunsScored()
                        
                if self._manOn(2):
                    self._incTeamScore()
                    pitcherGameState.incEarnedRuns()
                    batterGameState.incRBIs()
                    #increment player on 2nd runs scored
                    playerStateOnSecond = self._getPlayerStateOn(2)
                    playerStateOnSecond.incRunsScored()
                    thisAtBatResult.incRunsScored()
                
                if self._manOn(1):
                    self._incTeamScore()
                    pitcherGameState.incEarnedRuns()
                    batterGameState.incRBIs()
                    #increment player on 1st runs scored
                    playerStateOnFirst = self._getPlayerStateOn(1)
                    playerStateOnFirst.incRunsScored()
                    thisAtBatResult.incRunsScored()
                
                self._clearBaseState()
                    
            elif thisAtBatResult.getResultCode() in ['BB', 'HBP']:
                pitcherGameState.incWalks()
                if not self._manOn(1):
                    self._setBaseState(self.__lineup[self.__nextBatterIndex],
                                       self.__onSecond,
                                       self.__onThird)

                elif self._manOn(1) and not self._manOn(2):
                    self._setBaseState(self.__lineup[self.__nextBatterIndex],
                                       self.__onFirst,
                                       self.__onThird)

                elif self._manOn(1) and self._manOn(2) and not self._manOn(3):
                    self._setBaseState(self.__lineup[self.__nextBatterIndex],
                                       self.__onFirst,
                                       self.__onSecond)

                elif self._manOn(1) and self._manOn(2) and self._manOn(3):
                    self._setBaseState(self.__lineup[self.__nextBatterIndex],
                                       self.__onFirst,
                                       self.__onSecond)
                    self._incTeamScore()
                    pitcherGameState.incEarnedRuns()
                    batterGameState.incRBIs()
                    thisAtBatResult.incRunsScored()

                else:
                    print "SHOULDN'T GET HERE MISSING CASE"

            resCode = thisAtBatResult.getResultCode() 
        #print "res:%s outs:%d\n" %(resCode, self.__outs)
            

            #update the batter index, must do this after so we now place in lineup
            self.__nextBatterIndex = (self.__nextBatterIndex + 1) % Globals.gsBATTING_LINEUP_LENGTH

            if resCode in Globals.gsSINGLEOUTS:#['GO','SO','AO','SAC']:
                self._incOuts(1)
                pitcherGameState.incOutsPitched(1)

            elif resCode == 'DP':
                self._incOuts(2)
                pitcherGameState.incOutsPitched(2)
                
            elif resCode == 'TP':
                self._incOuts(3)
                pitcherGameState.incOutsPitched(3)

            batterGameState.addBattingResult(thisAtBatResult)       
            pitcherGameState.addPitchingResult(thisAtBatResult)
            #DEBUG
            print batterGameState
            #print pitcherGameState
            #print "res:%s outs:%d\n" %(resCode, self.__outs)
            #print "[runs %d] base state: %d %d %d\n" % (self.__runsScored, 
            #                                            self.__onFirst, self.__onSecond, 
            #                                            self.__onThird)

            return self.__outs
        
class GameRunner:

    def __init__(self, homeTeam=None, awayTeam=None):

        random.seed()

        self.__inning = 1
        self.__isHomeAtBat = False  


        if homeTeam==None or awayTeam==None:
            return None
        
        self.__homeTeam = homeTeam
        self.__awayTeam = awayTeam

        self.__homeTeamGameState = TeamGameState(homeTeam)
        self.__awayTeamGameState = TeamGameState(awayTeam)

        #StadiumGameState
        #    ConcessionStandInGameSate
        #    GiftShopInGameState
        #    Attendance 
        #    TotalRevenue
        return

    def __str__(self):
        s = "--- GAME STATE ---\n"
        s += "Home Team: %s\n" % str(self.__homeTeam.teamName())
        s += "Away Team: %s\n" % str(self.__awayTeam.teamName())
        return s

    def _endGame(self):
        return

    def _scoreEqual(self):
        return self.__awayTeamGameState.getRunsScored() == self.__homeTeamGameState.getRunsScored()

    def _endInning(self):

        #reset internal state
        if self.__isHomeAtBat:
            self.__inning += 1
            self.__homeTeamGameState.endTeamAtBat()
        else:
            self.__awayTeamGameState.endTeamAtBat()
        
        #flip the bit char
        self.__isHomeAtBat = not self.__isHomeAtBat

        return

    def _simAtBat(self):
        endGame = False

        #offsensive team simAtBat
        numOuts = -1
        if self.__isHomeAtBat:
            thisAtBatResult = self.__homeTeamGameState.simAtBat(self.__awayTeamGameState)
            numOuts = self.__homeTeamGameState.updateOffenseTeamGameState(thisAtBatResult)
            self.__awayTeamGameState.updateDefenseTeamGameState(thisAtBatResult)

        else:
            thisAtBatResult = self.__awayTeamGameState.simAtBat(self.__homeTeamGameState)
            numOuts = self.__awayTeamGameState.updateOffenseTeamGameState(thisAtBatResult)
            self.__homeTeamGameState.updateDefenseTeamGameState(thisAtBatResult)
            
            #num_outs = self._updateGameState(atBatResult)
        if numOuts == Globals.gsOUTSPERINNING and self.__inning >= Globals.gsMAXGAMEINNINGS and self.__isHomeAtBat and not self._scoreEqual():
            #DEBUG
            print "FINAL --- %s [%d - %d] ---\n" % (self.__inning, 
                                              self.__awayTeamGameState.getRunsScored(),
                                              self.__homeTeamGameState.getRunsScored())
            self._endInning()
            self._endGame()
            endGame = True

        elif numOuts == 3:
            #DEBUG
            print "--- %s [%d - %d] ---\n" % (self.__inning, 
                                              self.__awayTeamGameState.getRunsScored(),
                                              self.__homeTeamGameState.getRunsScored())

            self._endInning()
            
            
    #if 3 outs
    #check for end of game
    #call endInning/endGame
        return endGame

    #######
    #
    #Run the game simulation forward nsteps
    #######
    def run(self, nsteps=1):
        
        if nsteps == -1: #run to done
            while 1:
                if self._simAtBat():
                    return
                
        else:
            for i in range(nsteps):
                result = self._simAtBat()
                if not result:
                    break
               
        return


##########
#
#
#
##########
def main():
    return

if __name__ == "__main__":
    main()

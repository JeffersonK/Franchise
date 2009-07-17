import random

#gs = global static
gsPlayerPositions = ['P','C','1B','2B','3B','SS','LF','CF','RF']

#don't change this order !!! (add things to the front if they are always possible)
gsBatterResults = ['S','2B','3B','HR','BB','SO','HBP','GO','AO','SAC','DP','TP']#,'IBB']
gsSINGLEOUTS = ['GO','SO','AO','SAC']
gsHITS = ['S','2B','3B','HR']
gsDONTADDPITCH = ['SO','BB']
gsMAXPITCHCOUNT = 10
gsMAXGAMEINNINGS = 9
gsOUTSPERINNING = 3
gsBATTING_LINEUP_LENGTH = 9
gsBASEEMPTY = -1
#can happen anytime
#['S','2B','3B','HR','BB','SO','HBP','GO','AO']
# can only happen if < 2 out & runner on base
#['SAC', 'DP']
# >= 2 people on base and 0 outs
#['TP']

class GlobalState:

    __next_playerGUID = 0
    __franchises = {}
    

    def __init__(self):
        #read from disk
        return

    def __str__(self):
        return

    def nextPlayerGUID(self):
        self.__next_playerGUID += 1
        return self.__next_playerGUID - 1

    def addFranchise(self, franchise):
        if franchise == None:
            return

        self.__franchises.append(franchise)
        return

globalState = GlobalState()


class Player:

    #__name = ""
    __playerGUID = -1
    __position = "" #1B, 2B, SS, etc..
    #__picture = None

    #pitcher Stats
    __totKs = 0
    __totWalks = 0
    __totInnings = 0
    __totEarnedRuns = 0

    #abilities as pitcher 0-10
    #__stamina = 0
    #__control = 0
    #__power = 0

    #batting stats
    __totAtBats = 0
    __totHits = 0
    __tot1b = 0
    __tot2b = 0
    __tot3b = 0
    __totHR = 0
    __totWalks = 0
    
    #abilities as batter 0-10
    #__power = 0
    #__contact = 0

    #abilities as runner

    #abilities as fielder
    
    #personal characteristics

    def __init__(self, playerGUID, position):
        
        self.__playerGUID = playerGUID
        
        if position not in gsPlayerPositions:
            return None
        
        self.__position = position
        
        #if position.upper() == "P":
        #else:
            
        return

    def __str__(self):
        return "PlayerGUID: " + str(self.__playerGUID) + " Position: " + self.__position

    def isPitcher(self):
        return self.__position == 'P'

    def guid(self):
        return self.__playerGUID

class Franchise:
    
    #General Info
    __owner = ""
    __teamName = ""
    #__hometown

    #__stadium = None 


    #__farmteam = None
    #__trainingfacility = None

    #Team
    __players = []
    __lineup = []
    __rotation = []

    #Record
    __wins = 0
    __losses = 0


    #Financials
    #__salaryCap = 0

    def __init__(self):
        self.__players = []
        self.__lineup = []
        self.__rotation = []

        return

    def loadFromDisk(self, file):
        return

    #randomly generate players
    
    def create(self, owner, teamName):
    
        self.__owner = owner
        self.__teamName = teamName
        
        for position in gsPlayerPositions:
    
            p = Player(globalState.nextPlayerGUID(), position)

            if p.isPitcher():
                self.__rotation.append(p)

            self.__players.append(p)
            self.__lineup.append(p)
         
    def __str__(self):
        s = "Owner: " + self.__owner + "\n"
        s += "Team Name: " + self.__teamName + "\n"

        s += "Players: \n" 
        for p in self.__players:
            s += "\t" + p.__str__() + "\n"

        s += "Lineup: \n" 
        for p in self.__lineup:
            s += "\t" + str(p) + "\n"

        s += "Rotation: \n" 
        for p in self.__rotation:
            s += "\t" + str(p) + "\n"

        return s

    def teamName(self):
        return self.__teamName

    def owner(self):
        return self.__owner

    def getLineup(self):
        return self.__lineup

    def getPlayers(self):
        return self.__players

    def nextPitcherInRotation(self):
        return self.__rotation[0]

####
#
#
####
class AtBatResult:
    #__pitcher_playerGUID = -1
    #__batter_playerGUID = -1
    #__resultCode = "" #['S','2B','3B','HR','BB','SO','HBP','GO','AO','SAC','DP','TP']#,'IBB']        
    #__ballCount = 0
    #__strikeCount = 0
    #__totPitches = 0
    #__fouls = 0
    #__runsScored = 0

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
    
    def __str__(self):
        return ""

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

class PlayerGameState:

    def __init__(self, playerGUID):
        
        self.__playerGUID = playerGUID

        #hitting 
        self.__atBats = [] #(pitcher playerGUID, AtBatResultStr)
        self.__hits = 0
        self.__rbis = 0
        self.__runs = 0
        
        #pitching
        self.__battersFaced = [] #(batter playerGUID, AtBatResultStr)
        self.__ks = 0
        self.__walks = 0
        self.__hitsAllowed = 0
        self.__HRsAllowed = 0
        self.__earnedRuns = 0
        self.__totPitches = 0
        self.__totBalls = 0
        self.__totStrikesThrown = 0 #strikes + fouls
        self.__outsPitched = 0
        
        
        #fielding
        
        return

    def __str__(self):
        s = "Player: %s\n" % str(self.__playerGUID)
        s += "--- HITTING ---\n"
        s += "\tAt Bats: %s\n" % str(self.__atBats)
        s += "\tRBIs: %d\n" % self.__rbis
        s += "\tRuns: %d\n" % self.__runs
        s += "--- PITCHING ---\n"
        s += "Batter Results: %s\n" % str(self.__battersFaced)
        s += "\tKs: %d\n" % self.__ks
        s += "\tWalks: %d\n" % self.__walks
        s += "\tHits: %d\n" % self.__hitsAllowed
        s += "\tHRs: %d\n" % self.__HRsAllowed
        s += "\tRuns: %d\n" % self.__earnedRuns
        s += "\tOuts Pitched: %d\n" % self.__outsPitched
        s += "\tTot Pitches: %d\n" % self.__totPitches
        s += "\tTot Strikes: %d\n" % self.__totStrikesThrown
        s += "\tTot Balls: %d\n" % self.__totBalls
        return s

    #For Hitters
    def incRunsScored(self):
        self.__runs += 1
        return self.__runs

    def incRBIs(self, n=1):
        self.__rbis += n
        return self.__rbis
        
    def incHits(self):
        self.__hits += 1
        return self.__hits

    #FOR Pitchers
    def incHitsAllowed(self):
        self.__hitsAllowed += 1
        return self.__hitsAllowed

    def incHRsAllowed(self):
        self.__HRsAllowed += 1
        return self.__HRsAllowed

    def incEarnedRuns(self, n=1):
        self.__earnedRuns += n
        return self.__earnedRuns

    def incOutsPitched(self, n=1):
        self.__outsPitched += n
        return self.__outsPitched

    def incKs(self):
        self.__ks +=1
        return self.__ks

    def incWalks(self):
        self.__walks += 1
        return self.__walks

    def addBattingResult(self, atBatResult):
        self.__atBats.append([(atBatResult.getPitcherGUID(), atBatResult.getResultCode())])
        return

    def addPitchingResult(self, atBatResult):
        self.__battersFaced.append([(atBatResult.getBatterGUID(), atBatResult.getResultCode())])
        (totPitches, totStrikesThrown, totBalls) = atBatResult.getPitchCounts()
        self.__totPitches += totPitches
        self.__totStrikesThrown += totStrikesThrown
        self.__totBalls += totBalls
        
        if (self.__totPitches != (self.__totStrikesThrown + self.__totBalls + self.__outsPitched + self.__hitsAllowed - self.__ks)):
            print "**********ASSERT FAILURE **********"

        return

class TeamGameState:
    
    def __init__(self, franchise):
        #last pitcher in this list is the current pitcher
        #list of tuples (number of outs, pitcher object)
        self.__pitchers = [] 
        self.__nextBatterIndex = 0
        self.__runsScored = 0
        self.__playerStates = {}
        self.__lineup = []
        self.__onFirst = gsBASEEMPTY #playerGUID
        self.__onSecond = gsBASEEMPTY #player GUID
        self.__onThird = gsBASEEMPTY #player GUID
        self.__nOnBase = 0
        self.__outs = 0
        
        nextPitcher = franchise.nextPitcherInRotation()
        self.__pitchers = [(0, nextPitcher)]

        for player in franchise.getPlayers():
            self.__playerStates[player.guid()] = PlayerGameState(player.guid())
            
        self.__lineup = franchise.getLineup()

    def __str__(self):
        s = ""
        return s

    def getRunsScored(self):
        return self.__runsScored

    def getCurrentPitcher(self):
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
            numFouls = random.randint(ballCount + strikeCount, gsMAXPITCHCOUNT)
            totPitches = ballCount + strikeCount + numFouls
        else:
            totPitches = ballCount + strikeCount

        #must count the HBP event as a ball thrown
        if thisAtBatResultCode == 'HBP':
            ballCount += 1

        if thisAtBatResultCode not in gsDONTADDPITCH:
            totPitches += 1

        print "(%s) %d (%d-%d) %d\n" % (thisAtBatResultCode, totPitches, ballCount, strikeCount, numFouls)
        return (totPitches, strikeCount, ballCount, numFouls)

    def simAtBat(self, defenseTeamGameState):
        
        maxint =  len(gsBatterResults)-1
        if self.__nOnBase == 0 or self.__outs == 2:
            maxint = maxint - 3 #no SAC, DP, or TP
            
        elif self.__outs <= 1 and self.__nOnBase > 0:
            if self.__outs == 0 and self.__nOnBase >= 2:
                maxint = maxint #EVERYTHING
            else:
                maxint = maxint - 1 #SAC + DP
                

        r = random.randint(0, maxint)
        thisAtBatResultCode = gsBatterResults[r]
        
        #randomly generate pitch count
        (totPitches, strikeCount, ballCount, numFouls) = self._generatePitchCount(thisAtBatResultCode)
  
        return AtBatResult(self.__lineup[self.__nextBatterIndex], 
                           defenseTeamGameState.getCurrentPitcher().guid(),
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
        if guid == gsBASEEMPTY:
            return None
        
        if guid in self.__playerStates:
            return self.__playerStates[guid]
        
        #DEBUG
        print "DEBUG: STATE INCONSISTENCY - MAN ON BASE HAS NO PLAYER STATE!!!"
        return None

    #base is 1,2,3
    def _manOn(self, base):
        if base == 1:
            return self.__onFirst != gsBASEEMPTY

        if base == 2:
            return self.__onSecond != gsBASEEMPTY

        if base == 3:
            return self.__onThird != gsBASEEMPTY

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
            if base != gsBASEEMPTY:
                self.__nOnBase += 1

    def _incOuts(self, n):
        self.__outs += n

    def _incTeamScore(self):
        self.__runsScored += 1
        return self.__runsScored

    def _clearBaseState(self):
        self._setBaseState(gsBASEEMPTY, gsBASEEMPTY, gsBASEEMPTY)

    def _getCurrentBatterGameState(self):
        return self.__playerStates[self.__lineup[self.__nextBatterIndex].guid()]

    def _getCurrentPitcherGameState(self):
        return self.__playerStates[self.getCurrentPitcher().guid()]

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
                self._setBaseState(self.__lineup[self.__nextBatterIndex].guid(),
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
                self._setBaseState(gsBASEEMPTY,
                                    self.__lineup[self.__nextBatterIndex].guid(),
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

                self._setBaseState(gsBASEEMPTY,  gsBASEEMPTY, self.__lineup[self.__nextBatterIndex].guid())
                
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
                    self._setBaseState(self.__lineup[self.__nextBatterIndex].guid(),
                                       self.__onSecond,
                                       self.__onThird)

                elif self._manOn(1) and not self._manOn(2):
                    self._setBaseState(self.__lineup[self.__nextBatterIndex].guid(),
                                       self.__onFirst,
                                       self.__onThird)

                elif self._manOn(1) and self._manOn(2) and not self._manOn(3):
                    self._setBaseState(self.__lineup[self.__nextBatterIndex].guid(),
                                       self.__onFirst,
                                       self.__onSecond)

                elif self._manOn(1) and self._manOn(2) and self._manOn(3):
                    self._setBaseState(self.__lineup[self.__nextBatterIndex].guid(),
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
            self.__nextBatterIndex = (self.__nextBatterIndex + 1) % gsBATTING_LINEUP_LENGTH

            if resCode in gsSINGLEOUTS:#['GO','SO','AO','SAC']:
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
            #print batterGameState
            print pitcherGameState
            #print "res:%s outs:%d\n" %(resCode, self.__outs)
            #print "[runs %d] base state: %d %d %d\n" % (self.__runsScored, 
            #                                            self.__onFirst, self.__onSecond, 
            #                                            self.__onThird)

            return self.__outs
        
class GameRunner:

    #__homeTeam = None
    #__homeTeamGameState = None

    #__awayTeam = None
    #__awayTeamGameState = None

    
    #ConcessionStandInGameSate
    #GiftShopInGameState

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
        if numOuts == gsOUTSPERINNING and self.__inning >= gsMAXGAMEINNINGS and self.__isHomeAtBat and not self._scoreEqual():
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


############
#
#
#############
class Stadium:    
    
    __name = ""
    __maxAttendance = 0
    __giftshop = None
    __concessions = None
    __ticketprice = 0
    
    def __init__(self):
        return

    def __str__(self):
        return ""


    
class GiftShop:
    
    __jerseyprice = 0
    __hatprice = 0
    
    def __init__(self):
        return

    def __str__(self):
        return ""

class ConcessionStand:
    
    __beerprice = 0
    __sodaprice = 0
    __hotdogprice = 0
    __popcornprice = 0
    __pretzelprice = 0
    
    def __init__(self):
        return

    def __str__(self):
        return ""



def main():
    f1 = Franchise()
    f1.create("frza", "frzaites")
    #print f1
    
    f2 = Franchise()
    f2.create("jza", "jzites")
    #print f2

    sim = GameRunner(f1, f2)
    sim.run(-1)

if __name__ == "__main__":
    main()

import random

#gs = global static
gsPlayerPositions = ['P','C','1B','2B','3B','SS','LF','CF','RF']

#don't change this order !!! (add things to the front if they are always possible)
gsBatterResults = ['S','2B','3B','HR','BB','SO','HBP','GO','AO','SAC','DP','TP']#,'IBB']
gsSINGLEOUTS = ['GO','SO','AO','SAC']
gsHITS = ['S','2B','3B','HR']
gsDONTADDPITCH = ['SO','BB']
gsMAXPITCHCOUNT = 15
gsBATTING_LINEUP_LENGTH = 9
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
    __pitcher_playerGUID = -1
    __batter_playerGUID = -1
    __result = "" #['S','2B','3B','HR','BB','SO','HBP','GO','AO','SAC','DP','TP']#,'IBB']        
    __finalCount = None #(3,2)
    __totalPitches = 0


    def __init__(self, batterGUID, pitcherGUID, result, totalPitches, strikes, balls ):
        self.__pitcher_playerGUID = pitcherGUID
        self.__batter_playerGUID = batterGUID
        self.__result = result
        self.__finalCount = "(%s,%s)" % (str(balls),str(strikes))
        self.__totalPitches = totalPitches

        #DEBUG
        print "%s - %s:%d\n" % (self.__result, self.__finalCount, self.__totalPitches)

        return
    
    def __str__(self):
        return ""

    def getResultCode(self):
        return self.__result

class PlayerGameState:
    __playerGUID = None

    #hitting
    __atBats = [] #(pitcher playerGUID, BatterResult Object)
    __rbis = 0
    __runs = 0

    #pitching
    __batterResults = [] #(batter playerGUID, BatterResult Object)
    __ks = 0
    __walks = 0
    __runs = 0
    __totPitches = 0
    __totBalls = 0
    __totStrikes = 0
    __inningspitched = 0

    #fielding
    def __init__(self, playerGUID):
        self.__atBats = []
        self.__batterResults = []
        self.__playerGUID = playerGUID
        return

    def __str__(self):
        s = "Player: %s\n" % str(self.__playerGUID)
        s += "--- HITTING ---\n"
        s += "\tAt Bats: %s\n" % str(self.__atBats)
        s += "\tRBIs: %d\n" % self.__rbis
        s += "\tRuns: %d\n" % self.__runs
        s += "--- PITCHING ---\n"
        s += "Batter Results: %s\n" % str(self.__batterResults)
        s += "\tKs: %d\n" % self.__ks
        s += "\tWalks: %d\n" % self.__walks
        s += "\tRuns: %d\n" % self.__runs
        s += "\tInnings Pitched: %d\n" % self.__inningspitched
        s += "\tTot Pitches: %d\n" % self.__totPitches
        s += "\tTot Strikes: %d\n" % self.__totStrikes
        s += "\tTot Balls: %d\n" % self.__totBalls
        return s
   
    def addBattingResult(self, atBatResult):
        return

    def addPitchingResult(self, atBatResult):
        return

class TeamGameState:
    
    #last pitcher in this list is the current pitcher
    #list of tuples (number of outs, pitcher object)
    __pitchers = [] 
    __nextBatterIndex = 0
    __runsScored = 0
    __playerStates = {}
    __lineup = []
    __onFirst = -1 #playerGUID
    __onSecond = -1 #player GUID
    __onThird = -1 #player GUID
    __nOnBase = 0
    __outs = 0

    def __init__(self, franchise):

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
        ballcount = 0
        strikecount = 0
        pitchcount = 0
        if thisAtBatResultCode == 'SO':
            strikecount = 3
            ballcount = random.randint(0,3)
        elif thisAtBatResultCode == 'BB':
            ballcount = 4
            strikecount = random.randint(0,2)
        else:
            ballcount = random.randint(0,3)
            strikecount = random.randint(0,2)

        if strikecount >= 2:
            pitchcount = random.randint(ballcount+strikecount, gsMAXPITCHCOUNT)
        else:
            pitchcount = ballcount + strikecount

        if thisAtBatResultCode not in gsDONTADDPITCH:
            pitchcount += 1

        return (ballcount, strikecount, pitchcount)

    def simAtBat(self, defenseTeamGameState):
        
        maxint =  len(gsBatterResults)-1
        if self.__nOnBase == 0 or self.__outs == 2:
            maxint = maxint - 3 #no SAC, DP, or TP
            
        elif self.__outs <= 1 and self.__nOnBase > 0:
            if self.__outs == 0 and self.__nonBase >= 2:
                maxint = maxint #EVERYTHING
            else:
                maxint = maxint - 1 #SAC + DP
                

        r = random.randint(0, maxint)
        thisAtBatResultCode = gsBatterResults[r]
        
        #randomly generate pitch count
        (ballcount, strikecount, pitchcount) = self._generatePitchCount(thisAtBatResultCode)
  
        return AtBatResult(self.__lineup[self.__nextBatterIndex], 
                           defenseTeamGameState.getCurrentPitcher().guid(),
                           thisAtBatResultCode,
                           pitchcount, strikecount, ballcount)
    
    #do some cleanup and reset some shit
    def endAtBat(self):   
        self.__onFirst = -1 #playerGUID
        self.__onSecond = -1 #player GUID
        self.__onThird = -1 #player GUID
        self.__nOnBase = 0
        self.__outs = 0
        return

    def _setBaseState(self, onFirst, onSecond, onThird):
        #order here matters
        self.__onThird = onThird
        self.__onSecond = onSecond
        self.__onFirst = onFirst

    def _clearBaseState(self):
        self._setBaseState(-1,-1,-1)

    #side is 'offense' or 'defense'
    def updateTeamGameState(self, side, thisAtBatResult):

    #increment batter
        self.__nextBatterIndex = (self.__nextBatterIndex + 1) % gsBATTING_LINEUP_LENGTH
    #update pitcher state
    #update batter state
    #update offense game state
    
    #update defense gamesate

        #['S','2B','3B','HR','BB','SO','HBP','GO','AO','SAC','DP','TP']#,'IBB']        
        if side == 'offense':
            if thisAtBatResult.getResultCode() == 'S':
                if self.__onThird != -1:
                    self.__runsScored += 1

                    self._setBaseState(self.__lineup[self.__nextBatterIndex].guid(),
                                       self.__onFirst,
                                       self.__onSecond)

            # TODO: increment player runs scored
            # TODO: increment RBIs

            #advance all runners
            
            elif thisAtBatResult.getResultCode() == '2B':
            #if man 2nd and 3rd
                if self.__onThird != -1:
                    self.__runsScored += 1
                
                if self.__onSecond != -1:
                    self.__runsScored += 1

                self.__onThird = self.__onFirst
                self.__onSecond = self.__lineup[self.__nextBatterIndex].guid()

                # TODO: increment player runs scored
                # TODO: increment RBIs

                # - increment scored runs +2
                # - increment each player run scored
            
            elif thisAtBatResult.getResultCode() == '3B':
                if self.__onThird != -1:
                    self.__runsScored += 1
                        
                if self.__onSecond != -1:
                    self.__runsScored += 1

                if self.__onFirst != -1:
                    self.__runsScored += 1
            
                self._setBaseState(-1, -1, self.__lineup[self.__nextBatterIndex].guid())
                
                # TODO: increment player runs scored
                # TODO: increment RBIs          
  
            elif thisAtBatResult.getResultCode() == 'HR':
                self.__runsScored += 1
                    
                if self.__onThird != -1:
                    self.__runsScored += 1
                        
                if self.__onSecond != -1:
                    self.__runsScored += 1

                if self.__onFirst != -1:
                    self.__runsScored += 1

                self._clearBaseState()
                    
            elif thisAtBatResult.getResultCode() in ['BB', 'HBP']:
                if self.__onFirst == -1:
                    self._setBaseState(self.__lineup[self.__nextBatterIndex].guid(),
                                       self.__onSecond,
                                       self.__onThird)

                elif self.__onFirst != -1 and self.__onSecond == -1:
                    self._setBaseState(self.__lineup[self.__nextBatterIndex].guid(),
                                       self.__onFirst,
                                       self.__onThird)

                elif self.__onFirst != -1 and self.__onSecond != -1 and self.__onThird == -1:
                    self._setBaseState(self.__lineup[self.__nextBatterIndex].guid(),
                                       self.__onFirst,
                                       self.__onSecond)

                elif self.__onFirst != -1 and self.__onSecond != -1 and self.__onThird != -1:
                    self._setBaseState(self.__lineup[self.__nextBatterIndex].guid(),
                                       self.__onFirst,
                                       self.__onSecond)
                    self.__runsScored += 1

                else:
                    print "SHOULDN'T GET HERE MISSING CASE"

            resCode = thisAtBatResult.getResultCode() 
        #print "res:%s outs:%d\n" %(resCode, self.__outs)
            if resCode in gsSINGLEOUTS:#['GO','SO','AO','SAC']:
                self.__outs += 1
                
            elif resCode == 'DP':
                self.__outs += 2
                
            elif resCode == 'TP':
                self.__outs += 3
       
            #print "res:%s outs:%d\n" %(resCode, self.__outs)
            return self.__outs
        
        #if its defense (TODO: FIX - THIS IS MAD DIRTY)
        return -1
        
class GameRunner:

    __homeTeam = None
    __homeTeamGameState = None

    __awayTeam = None
    __awayTeamGameState = None

    __inning = 1
    __isHomeAtBat = False  


    #ConcessionStandInGameSate
    #GiftShopInGameState

    def __init__(self, homeTeam=None, awayTeam=None):

        random.seed()

        if homeTeam==None or awayTeam==None:
            return None
        
        self.__homeTeam = homeTeam
        self.__awayTeam = awayTeam

        self.__homeTeamState = TeamGameState(homeTeam)
        self.__awayTeamState = TeamGameState(awayTeam)

        return

    def __str__(self):
        s = "--- GAME STATE ---\n"
        s += "Home Team: %s\n" % str(self.__homeTeam.teamName())
        s += "Away Team: %s\n" % str(self.__awayTeam.teamName())
        return s

    def _endGame(self):
        return

    def _endInning(self):

        #reset internal state
        if self.__isHomeAtBat:
            self.__inning += 1
            self.__homeTeamState.endAtBat()
        else:
            self.__awayTeamState.endAtBat()
        
        #flip the bit char
        self.__isHomeAtBat = not self.__isHomeAtBat

        return

    def _simAtBat(self):
        endGame = False

        #offsensive team simAtBat
        numOuts = -1
        if self.__isHomeAtBat:
            thisAtBatResult = self.__homeTeamState.simAtBat(self.__awayTeamState)
            numOuts = self.__homeTeamState.updateTeamGameState('offense', thisAtBatResult)
            self.__awayTeamState.updateTeamGameState('defense', thisAtBatResult)

        else:
            thisAtBatResult = self.__awayTeamState.simAtBat(self.__homeTeamState)
            numOuts = self.__awayTeamState.updateTeamGameState('offense', thisAtBatResult)
            self.__homeTeamState.updateTeamGameState('defense', thisAtBatResult)
            
            #num_outs = self._updateGameState(atBatResult)
        if numOuts == 3 and self.__inning == 9 and self.__isHomeAtBat:
            #DEBUG
            print "FINAL --- %s [%d - %d] ---\n" % (self.__inning, 
                                              self.__awayTeamState.getRunsScored(),
                                              self.__homeTeamState.getRunsScored())
            self._endInning()
            self._endGame()
            endGame = True

        elif numOuts == 3:
            #DEBUG
            print "--- %s [%d - %d] ---\n" % (self.__inning, 
                                              self.__awayTeamState.getRunsScored(),
                                              self.__homeTeamState.getRunsScored())

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

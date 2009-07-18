import Globals
import PlayerDB
import cPickle

def generateTeam():
    team = {}
    for pos in Globals.gsPlayerPositions:
        p = Player(Globals.globalState.nextPlayerGUID(), pos)
        PlayerDB.gsPlayerDB.addPlayer(p.guid(), p)
        team[p.guid()] = pos

    return team

class Player:


    def __init__(self, playerGUID, position):

        #Book Keeping
        self.__playerGUID = playerGUID

        if position.upper() not in Globals.gsPlayerPositions:
            return None
        
        self.__position = position.upper()
        
        self.__franchiseGUID = Globals.gsPLAYERFREEAGENT
        #self.__franchiseGUIDHistory = [(franchiseGUID, datefrom, dateto)]
        
        #self.__isAAAPlayer
        #self.__dateDrafted

        #Player Personality/Character
        #__playerName = ""
        #__picture = None
        #__playerHomeTown =
        #__playerSalaryHistory =
        #__temper = 
        #__attitude =
        #__clutch = 
        #__leadership =
        #__morale =
        #__happiness =

    

        #Pitcher Stats
        self.__totKs = 0
        self.__totWalks = 0
        self.__totOutsPitched = 0
        self.__totEarnedRuns = 0
        
        #Abilities as pitcher 0-10
        #__stamina = 0
        #__control = 0
        #__power = 0

        #Batting stats
        self.__totAtBats = 0
        self.__totHits = 0
        self.__tot1b = 0
        self.__tot2b = 0
        self.__tot3b = 0
        self.__totHR = 0
        self.__totWalks = 0
    
        #Abilities as batter 0-10
        #__power = 0
        #__contact = 0

        #Abilities as runner

        #Abilities as fielder
        return

    def __getstate__(self):
        fmt =  "{'playerGUID':%d,'position':'%s','franchiseGUID':%d,'totKs':%d," + \
            "'totWalks':%d,'totOutsPitched':%d,'totEarnedRuns':%d," + \
            "'totAtBats':%d,'totHits':%d,'tot1b':%d,'tot2b':%d," + \
            "'tot3b':%d,'totHR':%d,'totWalks':%d}"

        return fmt % (self.__playerGUID, self.__position, self.__franchiseGUID,
                      self.__totKs, self.__totWalks, self.__totOutsPitched,
                      self.__totEarnedRuns, self.__totAtBats, self.__totHits, 
                      self.__tot1b, self.__tot2b, self.__tot3b, self.__totHR,
                      self.__totWalks)



    def __setstate__(self, dictstr):
        d = eval(dictstr)
        self.__playerGUID = d['playerGUID']
        self.__franchiseGUID = d['franchiseGUID']
        self.__position = d['position']
        self.__totKs = d['totKs']
        self.__totWalks = d['totWalks']
        self.__totOutsPitched = d['totOutsPitched']
        self.__totEarnedRuns = d['totEarnedRuns']
        
        #abilities as pitcher 0-10
        #__stamina = 0
        #__control = 0
        #__power = 0

        #batting stats
        self.__totAtBats = d['totAtBats']
        self.__totHits = d['totHits']
        self.__tot1b = d['tot1b']
        self.__tot2b = d['tot2b']
        self.__tot3b = d['tot3b']
        self.__totHR = d['totHR']
        self.__totWalks = d['totWalks']

    def __str__(self):
        return "PlayerGUID: %d Position:'%s'" % (self.__playerGUID, self.__position)

    def isPitcher(self):
        return self.__position == 'P'

    def guid(self):
        return self.__playerGUID

    def incTotKs(self, n=1):
        self.__totKs += n
        return self.__totKs

    def incTotWalks(self, n=1):
        self.__totWalks += n
        return self.__totWalks

    def setPlayerFranchise(self, franchiseGUID):
        self.__franchiseGUID = franchiseGUID

    def savePlayerUpdates(self):
        return PlayerDB.gsPlayerDB.write(self.__playerGUID)

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

    def getBattersFaced(self):
        return self.__battersFaced

    def getAtBats(self):
        return self.__atBats

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
        
        return


##########
#
#
#
##########
def testSerialization():
    guid = Globals.globalState.nextPlayerGUID()

    playerObj = Player(guid,"P")

    PlayerDB.gsPlayerDB.addPlayer(guid, playerObj)
    
    handle = PlayerDB.gsPlayerDB.getPlayerHandle(guid)
    
    if handle == playerObj:
        print "PASS"

    return

def main():
    testSerialization()
    
if __name__ == "__main__":
    main()


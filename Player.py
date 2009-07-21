import Globals
#import PlayerDB
import cPickle


class PlayerAbilities:

    def __init__(self):
        #batter abilities
        self.__powerZones = []
        self.__zoneMastery = []
        self.__pitchMastery = []
        self.__patience = 0
        self.__prestige = 0
        self.__speed = 0
        self.__defense = 0

        #pitcher abilities
        self.__zoneMastery = []
        self.__pitchMastery = []
class PlayerStats:
    def __init__(self):



        
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
        #__firstName = "Moonbeam"
        #__lastName = "McFly"
        #__experience = None
        #__playerHomeTown =
        #__playerSalaryHistory =
        #__temper = 
        #__attitude =
        #__clutch = 
        #__leadership =
        #__morale =
        #__happiness =

    
        #expereince
        #age
        #gamesPlayed
        self.__games = 0

        #Pitcher Stats
        self.__totBattersFaced = 0
        self.__totKs = 0
        self.__totWalksThrown = 0
        self.__totOutsPitched = 0
        self.__totEarnedRuns = 0
        self.__totStrikesThrown = 0
        self.__totPitchesThrown = 0
        self.__totHitsAllowed = 0
        self.__totHRAllowed = 0

        self.__wins = 0
        self.__losses = 0
        self.__starts = 0
    
        
        #Abilities as pitcher 0-10
        #__stamina = 0
        #__control = 0
        #__power = 0

        #Batting stats
        self.__totAtBats = 0
        self.__totHits = 0
        self.__tot1Bs = 0
        self.__tot2Bs = 0
        self.__tot3Bs = 0
        self.__totHRs = 0
        self.__totRBIs = 0
        self.__totRuns = 0
        self.__timesKd = 0
        self.__totWalks = 0
        self.__cyclesHit = 0
        self.__grandSlams = 0

        #Abilities as batter 0-10
        #__power = 0
        #__contact = 0

        #Abilities as runner

        #Abilities as fielder
        return

    def __getstate__(self):
        fmt =  "{'playerGUID':%d,'position':'%s','franchiseGUID':%d,'totKs':%d," + \
            "'totWalksThrown':%d,'totOutsPitched':%d,'totEarnedRuns':%d," + \
            "'wins':%d,'losses':%d,'starts':%d," +\
            "'totAtBats':%d,'totHits':%d,'tot1Bs':%d,'tot2Bs':%d," + \
            "'tot3Bs':%d,'totHR':%d,'totWalks':%d,'grandSlams':%d,'cyclesHit':%d,'games':%d," +\
            "'totRBIs':%d,'totRuns':%d,'timesKd':%d}"

        return fmt % (self.__playerGUID, self.__position, self.__franchiseGUID,
                      self.__totKs, self.__totWalksThrown, self.__totOutsPitched,
                      self.__totEarnedRuns, self.__wins, self.__losses, self.__starts,
                      self.__totAtBats, self.__totHits, 
                      self.__tot1Bs, self.__tot2Bs, self.__tot3Bs, self.__totHRs,
                      self.__totWalks, self.__grandSlams, self.__cyclesHit, self.__games,
                      self.__totRBIs, self.__totRuns, self.__timesKd)



    def __setstate__(self, dictstr):

        print "TODO: check for eval errors!!!"

        d = eval(dictstr)
        self.__playerGUID = d['playerGUID']
        self.__franchiseGUID = d['franchiseGUID']
        self.__position = d['position']
        self.__totKs = d['totKs']
        self.__totWalksThrown = d['totWalksThrown']
        self.__totOutsPitched = d['totOutsPitched']
        self.__totEarnedRuns = d['totEarnedRuns']
        self.__wins = d['wins']
        self.__losses = d['losses']
        self.__starts = d['starts']

        #abilities as pitcher 0-10
        #__stamina = 0
        #__control = 0
        #__power = 0

        #batting stats
        self.__totAtBats = d['totAtBats']
        self.__totHits = d['totHits']
        self.__tot1Bs = d['tot1Bs']
        self.__tot2Bs = d['tot2Bs']
        self.__tot3Bs = d['tot3Bs']
        self.__totHRs = d['totHR']
        self.__totWalks = d['totWalks']
        self.__grandSlams = d['grandSlams']
        self.__cyclesHit = d['cyclesHit']
        self.__games = d['games']

        self.__totRBIs = d['totRBIs']
        self.__totRuns = d['totRuns']
        self.__timesKd = d['timesKd']

    def __str__(self):
        return "PlayerGUID: %d Position:'%s'" % (self.__playerGUID, self.__position)

    #we should generate events when we update stats because
    #it is a change in the player state
    #here is where a player will gain ablities when their stats are updated
    def updatePlayerStats(self, playerGameState):

        if playerGameState.played():
            self.__games += 1

        #Batting Stats
        self.__totAtBats += playerGameState.atBatCount()
        self.__totHits += playerGameState.Hits()
        self.__totWalks += playerGameState.Walks()
        self.__tot1Bs += playerGameState.Singles()
        self.__tot2Bs += playerGameState.Doubles()
        self.__tot3Bs += playerGameState.Triples()
        self.__totHRs += playerGameState.HomeRuns()
        self.__grandSlams += playerGameState.GrandSlams()
        self.__totRBIs += playerGameState.RBIs()
        self.__totRuns += playerGameState.Runs()
        self.__timesKd += playerGameState.timesKd()
    
        self.__cyclesHit += playerGameState.checkHitCycle()


        #Pitching Stats
        #self.__starts += playerGameState.gotStart()
        #self.__battersKd += playerGameState.BattersKd()
        #self.__walksThrown += playerGameState.WalksThrown()
        #self.__hitsAllowed += playerGameState.HitsAllowed()
        #self.__HRsAllowed += playerGameState.HRsAllowed()
        

        
        #self._updateBatAvg()
        #self._updateSlgPct()
        #need helper function to compute stats so we dno't repete the logic
        return ['+1 EXP']

    #def isPitcher(self):
    #    return self.__position == 'P'

    def getPosition(self):
        return self.__position

    def guid(self):
        return self.__playerGUID

    #def incTotKs(self, n=1):
    #    self.__totKs += n
        return self.__totKs

    #def incTotWalks(self, n=1):
    #    self.__totWalks += n
        return self.__totWalks

    #def incTotWalksThrown(self, n=1):
    #    self.__totWalksThrown += n
    #    return self.__totWalksThrown

    def setPlayerFranchise(self, franchiseGUID):
        self.__franchiseGUID = franchiseGUID

    #def handlePlayerPlayedGame(self)

    #def generatePlayerEvents(self, state):
    #    return


class PlayerGameState:

    def __init__(self, playerGUID):
        
        self.__playerGUID = playerGUID

        #hitting 
        self.__atBatResults = [] #(pitcher playerGUID, AtBatResultStr)
        self.__atBatCount = 0
        self.__hits = 0
        self.__HRs = 0
        self.__1Bs = 0
        self.__2Bs = 0
        self.__3Bs = 0
        self.__rbis = 0
        self.__runs = 0
        self.__walks = 0
        self.__Kd = 0
        self.__hbps = 0
        self.__grandSlams = 0
        
        #pitching
        self.__started = 0
        self.__battersFaced = [] #(batter playerGUID, AtBatResultStr)
        self.__Ks = 0
        self.__walksThrown = 0
        self.__hitsAllowed = 0
        self.__HRsAllowed = 0
        self.__grandSlamsAllowed = 0
        self.__1BsAllowed = 0
        self.__2BsAllowed = 0
        self.__3BsAllowed = 0
        self.__earnedRuns = 0
        self.__hbpsThrown = 0
        self.__totPitchesThrown = 0
        self.__totBallsThrown = 0
        self.__totStrikesThrown = 0 #strikes + fouls
        self.__outsPitched = 0
        
        #calculated stats
        #self.__gamePitchedRank = 0
        
        #fielding stats
        return

    def __str__(self):

        s = "Player: %s\n" % str(self.__playerGUID)
        if self.__atBatCount > 0:

            s += "--- HITTING ---\n"
            s += "\tAt Bats: %s\n" % str(self.__atBatResults)
            s += "\tKd: %d\n" % self.__Kd
            s += "\tNum At Bats: %d\n" % self.__atBatCount
            s += "\tRBIs: %d\n" % self.__rbis
            s += "\tRuns: %d\n" % self.__runs
            s += "\tHits: %d\n" % self.__hits
            s += "\tWalks: %d\n" % self.__walks
            s += "\tHBPs: %d\n" % self.__hbps
            s += "\tHRs: %d\n" % self.__HRs
            s += "\t1Bs: %d\n" % self.__1Bs
            s += "\t2Bs: %d\n" % self.__2Bs
            s += "\t3Bs: %d\n" % self.__3Bs

            if self.__atBatCount > 0:
                s += "\tBatAvg: %.3f\n" % (float(self.__hits) / float(self.__atBatCount))
                s += "\tSlgPct: %.3f\n" % ((float(self.__HRs)*4 + float(self.__3Bs)*3 + float(self.__2Bs)*2 + float(self.__1Bs)) / float(self.__atBatCount))

        if len(self.__battersFaced) > 0:
            
            s += "--- PITCHING ---\n"
            s += "Batter Results: %s\n" % str(self.__battersFaced)
            s += "\tKs: %d\n" % self.__Ks
            s += "\tWalks: %d\n" % self.__walksThrown
            s += "\tHits: %d\n" % self.__hitsAllowed
            s += "\tRuns: %d\n" % self.__earnedRuns
            s += "\tOuts Pitched: %d\n" % self.__outsPitched
            s += "\tTot Pitches: %d\n" % self.__totPitchesThrown
            s += "\tTot Strikes: %d\n" % self.__totStrikesThrown
            s += "\tTot Balls: %d\n" % self.__totBallsThrown
            s += "\tHBPs: %d\n" % self.__hbpsThrown
            s += "\t1Bs: %d\n" % self.__1BsAllowed
            s += "\t2Bs: %d\n" % self.__2BsAllowed
            s += "\t3Bs: %d\n" % self.__3BsAllowed
            s += "\tHRs: %d\n" % self.__HRsAllowed
            s += "\tGRandSlamsAllowed: %d\n" % self.__grandSlamsAllowed
        
            if self.__outsPitched == 0:
                s += "\tgame ERA: INF\n"
            
            elif self.__outsPitched > 0:
                gamesPitched = float(self.__outsPitched) / (3.0*9.0) #outs per game
                if gamesPitched > 0.0:
                    s += "\tgame ERA: %.2f\n" % (float(self.__earnedRuns) / float(gamesPitched))
                    
        return s

    def updatePlayerGameState(self, atBatEvent, isBatter):
        if isBatter:
            self.__atBatResults += [(atBatEvent.getPitcherGUID(), atBatEvent.getResultCode())]
            
            if atBatEvent.countsAsAtBat():
                self.__atBatCount += 1
            
            if atBatEvent.StrikeOut():
                self.__Kd += 1
            
            if atBatEvent.Walk():
                self.__walks += 1
            
            if atBatEvent.HitByPitch():
                self.__hbps += 1
            
            if atBatEvent.isHit():
                self.__hits += 1
            
            if atBatEvent.HomeRun():
                if atBatEvent.runsScored() == 4:
                    self.__grandSlams += 1

                self.__HRs += 1
            
            if atBatEvent.Single():
                self.__1Bs += 1
            
            if atBatEvent.Double():
                self.__2Bs += 1
            
            if atBatEvent.Triple():
                self.__3Bs += 1

            self.__rbis += atBatEvent.runsScored()
            

        else:
            self.__battersFaced += [(atBatEvent.getBatterGUID(), atBatEvent.getResultCode())]

            (pitchesThrown, strikesThrown, ballsThrown) = atBatEvent.getPitchCounts()
            self.__totPitchesThrown += pitchesThrown
            self.__totStrikesThrown += strikesThrown
            self.__totBallsThrown += ballsThrown
            if atBatEvent.StrikeOut():
                self.__Ks += 1
            
            if atBatEvent.Walk():
                self.__walksThrown += 1
            
            if atBatEvent.isHit():
                self.__hitsAllowed += 1
            
            if atBatEvent.HitByPitch():
                self.__hbpsThrown += 1
            
            if atBatEvent.HomeRun():
                if atBatEvent.runsScored() == 4:
                    self.__grandSlamsAllowed += 1
                
                   
                self.__HRsAllowed += 1
            
            if atBatEvent.Single():
                self.__1BsAllowed += 1
            
            if atBatEvent.Double():
                self.__2BsAllowed += 1
            
            if atBatEvent.Triple():
                self.__3BsAllowed += 1

            self.__earnedRuns += atBatEvent.runsScored()
            
            self.__outsPitched += atBatEvent.outsMade()

    def played(self):
        if self.__atBatCount > 0:
            return True
        
        if self.__totPitchesThrown > 0:
            return True
        
        if self.Walks() > 0:
            return True

        return False

    def RBIs(self):
        return self.__rbis

    def Runs(self):
        return self.__runs

    def timesKd(self):
        return self.__Kd

    def atBatCount(self):
        return self.__atBatCount

    def Hits(self):
        return self.__hits

    def Singles(self):
        return self.__1Bs

    def Doubles(self):
        return self.__2Bs

    def Triples(self):
        return self.__3Bs

    def HomeRuns(self):
        return self.__HRs

    def Walks(self):
        return self.__walks

    def GrandSlams(self):
        return self.__grandSlams

    def checkHitCycle(self):
        if self.__1Bs > 0 and self.__2Bs > 0 and self.__3Bs > 0 and self.__HRs > 0:
            return 1
            
        return 0

    #def getBattersFaced(self):
    #    return self.__battersFaced

    #def getAtBats(self):
    #    return self.__atBats

    #def incAtBats(self):
    #    self.__atBats += 1
    #    return self.__atBats

    #For Hitters
    """def incRunsScored(self):
        self.__runs += 1
        return self.__runs

    def incRBIs(self, n=1):
        self.__rbis += n
        return self.__rbis
        
    def incHits(self):
        self.__hits += 1
        return self.__hits

    def incWalks(self):
        self.__walks += 1
        return self.__walks

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

    def incWalksThrown(self):
        self.__walksThrown += 1
        return self.__walksThrown

    def addBattingResult(self, atBatResult):
        self.__atBatResult += [(atBatResult.getPitcherGUID(), atBatResult.getResultCode())]
        if atBatResult.getResultCode() not in Globals.gsNOTATBAT:
            self.__atBats += 1
            
        return

    def addPitchingResult(self, atBatResult):
        self.__battersFaced += [(atBatResult.getBatterGUID(), atBatResult.getResultCode())]
        (totPitches, totStrikesThrown, totBalls) = atBatResult.getPitchCounts()
        self.__totPitches += totPitches
        self.__totStrikesThrown += totStrikesThrown
        self.__totBalls += totBalls
        
        return"""


##########
#
#
#
##########
def testSerialization():
    #guid = Globals.globalState.nextPlayerGUID()
    #playerObj = Player(guid,"P")

    #PlayerDB.gsPlayerDB.addPlayer(guid, playerObj)
    
    #handle = PlayerDB.gsPlayerDB.getPlayerHandle(guid)
    
    #if handle == playerObj:
    #    print "PASS"
    return

def main():
    #testSerialization()
    return
    
if __name__ == "__main__":
    main()


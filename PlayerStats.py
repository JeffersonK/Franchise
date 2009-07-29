import cPickle
from Globals import *
from Experience import *

gsSTATTYPE_PITCHER_STATS = 'PITS'
gsSTATTYPE_BATTER_STATS = 'BATS'
gsSTATSUBTYPE_ENDGAMESTATS = 'GAME'
gsSTATSUBTYPE_SINGLEPLAYSTATS = 'PLAY'

#statSubType is used by the += operator to know which values should be added from the 'other' object
#in InGameStats are one kind because we will accumlate per batter during a game, the other kind will accumulate
#at the end of the game and be added to the persistant player stats
#GAMESTAT is the stat we total at the end of the game
#SINGLESTAT is the stat we total during the game


###############################
#
#
#
#
#
#
###############################

#class PerZoneStat:
#    def __init__(self, initValue=0):
#        self.__statZones = [gsNUMBERZONES]
#        for i in gsNUMBERZONES:
#            self.__statZones += [(initValue,initValue)


#
# Functions we can reuse to compute stats
#
def computeBattingAvg(numAtBats, numHits):
    if numAtBats <= 0:
        return None
    avg = float(numHits) / float(numAtBats)
    #avg = "%.3f" % avg
    #return avg
    return formatFloatStr(avg, 3)

def computeSluggingPct(singles, doubles, triples, homeruns, atBats):
    if atBats <= 0:
        return None
    
    num = float(singles) + 2*float(doubles) + 3*float(triples) + 4*float(homeruns)
    slgpct = num / float(atBats)
    #slgpct = "%.3f" % slgpct
    #return slgpct
    #print slgpct
    return formatFloatStr(slgpct, 3)


def computeWinPct(wins, losses):
    if wins + losses <= 0:
        return None

    winPct = float(wins) / float(wins + losses)
    #winPct = "%.3f" % winPct
    #return winPct
    return formatFloatStr(winPct, 3)

def computeOnBasePct2(hits, walks, hbps, atBats):
    if atBats <= 0:
        return None

    obp = float(hits + walks + hbps) / float(atBats)
    #obp = "%.3f" % obp
    #return obp
    return formatFloatStr(obp, 3)

###############################
#
#
#
#
#
#
###############################
class PitcherStats:
    def __init__(self, statSubType, initValue=0):#should optionally take an atBatResult parse it and set values
        self.__statType = gsSTATTYPE_PITCHER_STATS
        self.__statSubType = statSubType #this doesn't persist
        self.__batterResults = []#list of lists where inner list is a game
        self.__starts = initValue #set once per game
        self.__wins = initValue #set once per game
        self.__currentWinStreak = initValue 
        self.__longestWinStreak = initValue
        self.__losses = initValue
        self.__currentLosingStreak = initValue
        self.__longestLosingStreak = initValue
        self.__saves = initValue
        self.__shutouts = initValue
        self.__noHitters = initValue
        self.__perfectGames = initValue
        self.__totBattersFaced = initValue
        self.__totKs = initValue
        self.__mostKsGame = initValue
        self.__totWalksThrown = initValue
        self.__totOutsThrown = initValue
        self.__totDPsThrown = initValue
        self.__totTPsThrown = initValue
        self.__totEarnedRuns = initValue
        self.__totPitchesThrown = initValue

        self.__fastestPitchThrown = initValue
        self.__totFastballsThrown = initValue
        self.__totCurveballsThrown = initValue
        self.__totSlidersThrown = initValue
        self.__totKnuckleballsThrown = initValue
        self.__totChangeupsThrown = initValue
        self.__totSinkersThrown = initValue
        self.__totForkballsThrown = initValue
        self.__totSpitballsThrown = initValue        


        self.__totStrikesThrown = initValue
        self.__totBallsThrown = initValue
        self.__totHitsAllowed = initValue
        self.__totBattersHBP = initValue
        self.__totHRsAllowed = initValue
        self.__totGrandSlamsAllowed = initValue
        self.__longestHRAllowed = initValue
        self.__tot1BsAllowed = initValue
        self.__tot2BsAllowed = initValue
        self.__tot3BsAllowed = initValue
        
        #TODO: while we update stats put achievements in here
        #self.__statUpdateEvents = []
        return
     
    def __iadd__(self, other):
        if self.statType() != other.statType():
            print "Cannot add stat type %s and %s\n" % (self.statType(), other.statType())

        if other.statSubType() == gsSTATSUBTYPE_ENDGAMESTATS:
            self.__starts += other.__starts
            self.__saves += other.__saves
        
            #Throw Event when a new record is set
            if other.__totKs > self.__mostKsGame:
                self.__mostKsGame = other.__totKs
                
            if other.__totEarnedRuns == 0:
                self.__shutouts += 1#other.__shutouts
            if other.__totHitsAllowed == 0:
                self.__noHitters += 1#self.__noHitters += other.__noHitters
            if other.__totBattersFaced == (gsOUTSPERINNING*gsMAXGAMEINNINGS):
                self.__perfectGames += other.__perfectGames

            if other.__wins and other.__losses:
                print "DEBUG: Inconsistency Wins and Losses both Non-Zero in stats from game!"
            
            if other.__wins > 0:
                self.__wins += other.__wins
                self.__currentWinStreak += other.__wins#other.__currentWinStreak
                if self.__currentWinStreak > self.__longestWinStreak:
                    self.__longestWinStreak = self.__currentWinStreak
                    
                self.__currentLosingStreak = 0
      
            elif other.__losses > 0:
                self.__losses += other.__losses
                self.__currentLosingStreak += other.__losses#currentLosingStreak
                if self.__currentLosingStreak > self.__longestLosingStreak:
                    self.__longestLosingStreak = self.__currentLosingStreak
            
                self.__currentWinStreak = 0

            #save a game's results as a sub-list
            self.__batterResults += [other.__batterResults]
        else:
            #save each batter
            self.__batterResults += [other.__batterResults]

        self.__totBattersFaced += other.__totBattersFaced
        self.__totKs += other.__totKs
        self.__totWalksThrown += other.__totWalksThrown
        self.__totOutsThrown += other.__totOutsThrown
        self.__totDPsThrown += other.__totDPsThrown
        self.__totTPsThrown += other.__totTPsThrown
        self.__totEarnedRuns += other.__totEarnedRuns
        self.__totPitchesThrown += other.__totPitchesThrown

        if other.__fastestPitchThrown > self.__fastestPitchThrown:
            self.__fastestPitchThrown = other.__fastestPitchThrown

        self.__totFastballsThrown += other.__totFastballsThrown
        self.__totCurveballsThrown += other.__totCurveballsThrown
        self.__totSlidersThrown += other.__totSlidersThrown
        self.__totKnuckleballsThrown +=  other.__totKnuckleballsThrown
        self.__totChangeupsThrown += other.__totChangeupsThrown
        self.__totSinkersThrown += other.__totSinkersThrown
        self.__totForkballsThrown +=  other.__totForkballsThrown
        self.__totSpitballsThrown += other.__totSpitballsThrown


        self.__totStrikesThrown += other.__totStrikesThrown
        self.__totBallsThrown += other.__totBallsThrown
        
        self.__totHitsAllowed += other.__totHitsAllowed
        
        self.__totBattersHBP += other.__totBattersHBP
        self.__totHRsAllowed += other.__totHRsAllowed
        self.__totGrandSlamsAllowed += other.__totGrandSlamsAllowed
        
        if other.__longestHRAllowed > self.__longestHRAllowed:
            self.__longestHRAllowed = other.__longestHRAllowed
        
        self.__tot1BsAllowed += other.__tot1BsAllowed
        self.__tot2BsAllowed += other.__tot2BsAllowed
        self.__tot3BsAllowed += other.__tot3BsAllowed
        return self

    def __getstate__(self):
        dictStr = "{'statType':'%s'," +\
            "'batterResults':%s," + \
            "'starts':%d," + \
            "'wins':%d," + \
            "'currentWinStreak':%d," +\
            "'longestWinStreak':%d," +\
            "'losses':%d," + \
            "'currentLosingStreak':%d," +\
            "'longestLosingStreak':%d," +\
            "'saves':%d," + \
            "'shutouts':%d," +\
            "'noHitters':%d," +\
            "'perfectGames':%d," +\
            "'totBattersFaced':%d," + \
            "'totKs':%d," + \
            "'mostKsGame':%d," +\
            "'totWalksThrown':%d," + \
            "'totOutsThrown':%d," + \
            "'totDPsThrown':%d," + \
            "'totTPsThrown':%d," + \
            "'totEarnedRuns':%d," + \
            "'totPitchesThrown':%d," + \
            "'fastestPitchThrown':%d," +\
            "'totFastballsThrown':%d," +\
            "'totCurveballsThrown':%d," +\
            "'totSlidersThrown':%d," +\
            "'totChangeupsThrown':%d," +\
            "'totKnuckleballsThrown':%d," +\
            "'totSinkersThrown':%d," +\
            "'totForkballsThrown':%d," +\
            "'totSpitballsThrown':%d," +\
            "'totStrikesThrown':%d," + \
            "'totBallsThrown':%d," + \
            "'totHitsAllowed':%d," + \
            "'totBattersHBP':%d," + \
            "'totHRsAllowed':%d," + \
            "'totGrandSlamsAllowed':%d," + \
            "'longestHRAllowed':%d," + \
            "'tot1BsAllowed':%d," + \
            "'tot2BsAllowed':%d," + \
            "'tot3BsAllowed':%d}"
            
        
        return dictStr % (self.__statType,
                          self.__batterResults, self.__starts, self.__wins,
                          self.__currentWinStreak, self.__longestWinStreak, 
                          self.__losses, self.__currentLosingStreak, 
                          self.__longestLosingStreak, self.__saves, 
                          self.__shutouts, self.__noHitters, self.__perfectGames,
                          self.__totBattersFaced, self.__totKs, self.__mostKsGame, self.__totWalksThrown, 
                          self.__totOutsThrown, self.__totDPsThrown, self.__totTPsThrown, 
                          self.__totEarnedRuns, self.__totPitchesThrown, 
                          self.__fastestPitchThrown, self.__totFastballsThrown,
                          self.__totCurveballsThrown, self.__totSlidersThrown,
                          self.__totChangeupsThrown, self.__totKnuckleballsThrown,
                          self.__totSinkersThrown,
                          self.__totForkballsThrown, self.__totSpitballsThrown,
                          self.__totStrikesThrown, self.__totBallsThrown, 
                          self.__totHitsAllowed, self.__totBattersHBP, 
                          self.__totHRsAllowed, self.__totGrandSlamsAllowed, 
                          self.__longestHRAllowed, self.__tot1BsAllowed, 
                          self.__tot2BsAllowed, self.__tot3BsAllowed)


    def safe_setstatevar(self, key, dict, defaultVal):
        val = None
        try:
            val = dict[key]
            setattr(self, "__"+key, val)
        except KeyError:
            setattr(self, "__"+key, defaultVal)

    def __setstate__(self, dictStr):
        #print dictStr
        #d = eval(dictStr)
        d = dictStr
        self.safe_setstatevar('statType', d, gsSTATTYPE_PITCHER_STATS)
        #self.__statType = d['statType']
        self.__batterResults = d['batterResults']
        self.__starts = d['starts']
        self.__wins = d['wins']
        self.__currentWinStreak = d['currentWinStreak']
        self.__longestWinStreak = d['longestWinStreak']
        self.__losses = d['losses']
        self.__currentLosingStreak = d['currentLosingStreak']
        self.__longestLosingStreak = d['longestLosingStreak']
        self.__saves = d['saves']
        self.__shutouts = d['shutouts']
        self.__noHitters = d['noHitters']
        self.__perfectGames = d['perfectGames']
        self.__totBattersFaced = d['totBattersFaced']
        self.__totKs = d['totKs']
        self.__mostKsGame = d['mostKsGame']
        self.__totWalksThrown = d['totWalksThrown']
        self.__totOutsThrown = d['totOutsThrown']
        self.__totDPsThrown = d['totDPsThrown']
        self.__totTPsThrown = d['totTPsThrown']
        self.__totEarnedRuns = d['totEarnedRuns']
        self.__totPitchesThrown = d['totPitchesThrown']

        self.__fastestPitchThrown = d['fastestPitchThrown']
        self.__totFastballsThrown = d['totFastballsThrown']
        self.__totCurveballsThrown = d['totCurveballsThrown']
        self.__totKnuckleballsThrown = d['totKnuckleballsThrown']
        self.__totSlidersThrown = d['totSlidersThrown']
        self.__totChangeupsThrown = d['totChangeupsThrown']
        self.__totSinkersThrown = d['totSinkersThrown']
        self.__totForkballsThrown = d['totSinkersThrown']
        self.__totSpitballsThrown = d['totSpitballsThrown']


        self.__totStrikesThrown = d['totStrikesThrown']
        self.__totBallsThrown = d['totBallsThrown']
        self.__totHitsAllowed = d['totHitsAllowed']
        self.__totBattersHBP = d['totBattersHBP']
        self.__totHRsAllowed = d['totHRsAllowed']
        self.__totGrandSlamsAllowed = d['totGrandSlamsAllowed']
        self.__longestHRAllowed = d['longestHRAllowed']
        self.__tot1BsAllowed = d['tot1BsAllowed']
        self.__tot2BsAllowed = d['tot2BsAllowed']
        self.__tot3BsAllowed = d['tot3BsAllowed']
        return self


    def __str__(self):
        return self.__getstate__()

    def statType(self):
        return self.__statType

    def isPitcherStats(self):
        return self.__statType == gsSTATTYPE_PITCHER_STATS

    def isBatterStats(self):
        return self.__statType == gsSTATTYPE_BATTER_STATS

    #can't call this on stat objects read 
    #from disk because it doesn't persist
    def statSubType(self):
        return self.__statSubType

    def addBatterFaced(self):
        self.__totBattersFaced += 1

    #START GAME FUNCTIONS
    # should only be called at the start of the game
    # by the PlayerGameState object when the stats object
    # is initialized
    def incStarts(self):
        self.__starts += 1

    #END OF GAME FUNCTIONS 
    # these are functions that should only be called
    # at the end of the game by the TeamGameState wrapper 
    def incLosses(self):
        self.__losses += 1

    def incWins(self):
        self.__wins += 1

    #def addEarnedRuns(self, n=1):
    #    self.__totEarnedRuns += n
  


    #
    #
    #
    #
    def getStarts(self):
        return self.__starts

    def getWins(self):
        return self.__wins
    
    def getLosses(self):
        return self.__losses

    #def getSaves(self):
    #    return self.__saves

    def getBatterResults(self):
        return self.__batterResults

    def getTotBattersFaced(self):
        return self.__totBattersFaced

    def getCurrentWinStreak(self):
        return self.__currentWinStreak

    def getLongestWinStreak(self):
        return self.__longestWinStreak
    
    def getCurrentLosingStreak(self):
        return self.__currentLosingStreak

    def getLongestLosingStreak(self):
        return self.__longestLosingStreak

    def getShutouts(self):
        return self.__shutouts

    def getNoHitters(self):
        return self.__noHitters

    def getPerfectGames(self):
        return self.__perfectGames
    
    def getTotStrikeouts(self):
        return self.__totKs

    def getMostStrikeoutsGame(self):
        return self.__mostKsGame

    def getTotWalks(self):
        return self.__totWalksThrown

    def getTotOuts(self):
        return self.__totOutsThrown

    #def getTotDPs(self):
    #    return self.__totDPsThrown

    #def getTotTPs(self):
    #    return self.__totTPsThrown

    def getTotEarnedRuns(self):
        return self.__totEarnedRuns

    def getTotPitchesThrown(self):
        return self.__totPitchesThrown

    def getTotFastballsThrown(self):
        return self.__totFastballsThrown

    def getTotCurveballsThrown(self):
        return self.__totCurveballsThrown

    def getTotKnuckleballsThrown(self):
        return self.__totKnuckleballsThrown

    def getTotSlidersThrown(self):
        return self.__totSlidersThrown

    def getTotChangeupsThrown(self):
        return self.__totChangeupsThrown

    def getTotSinkersThrown(self):
        return self.__totSinkersThrown

    def getTotForkballsThrown(self):
        return self.__totForkballsThrown
    
    def getTotSpitballsThrown(self):
        return self.__totSpitballsThrown

    def getStrikes(self):
        return self.__totStrikesThrown

    def getBalls(self):
        return self.__totBallsThrown
    
    def getTotHitsAllowed(self):
        return self.__totHitsAllowed

    def getTotSinglesAllowed(self):
        return self.__tot1BsAllowed

    def getTotDoublesAllowed(self):
        return self.__tot2BsAllowed

    def getTotTriplesAllowed(self):
        return self.__tot3BsAllowed

    def getTotHRsAllowed(self):
        return self.__totHRsAllowed
        
    def getTotGrandSlamsAllowed(self):
        return self.__totGrandSlamsAllowed

    def getLongestHRAllowed(self):
        return self.__longestHRAllowed
    
    def computeWinPct(self):
        return computeWinPct(self.getWins(), self.getLosses())

    def computeERA(self):
        if self.getTotOuts() <= 0:
            return None
        era = (float(self.getTotEarnedRuns()) / (float(self.getTotOuts())/float(gsOUTSPERGAME)))
        #era = "%.2f" % era
        #return era
        return formatFloatStr(era, 2)
    
    def computeOpposingOBP(self):#TODO: add HBP later
        return computeOnBasePct2(self.getTotBattersFaced(), self.getTotHitsAllowed()+self.getTotWalks())
        
    def computeBattersSlgPct(self):
        return computeSluggingPct(self.getTotSinglesAllowed(),
                                  self.getTotDoublesAllowed(),
                                  self.getTotTriplesAllowed(),
                                  self.getTotHRsAllowed(),
                                  self.getTotBattersFaced())

    def computeStrikeBallRatio(self):
        if self.__totBallsThrown == 0:
            return 'INF'
        num = float(self.__totStrikesThrown)/float(self.__totBallsThrown)
        return formatFloatStr(num, 2)


    #Algorithm as defined at www.baseball-almanac.cmo/stats2.shtml
    def getPitcherScore(self):
        score = gsXP_PITCHER_START

        score += self.__totOutsThrown * gsXP_PITCHER_OUT
        score += self.__totKs * gsXP_PITCHER_K
        score += 2*5#each inning completed after fourth * 2 - min( (self.__totOutsThrown-(gsOUTSPERINNING*4))/3 )

        #the following add negative values
        score += self.__totHitsAllowed * gsXP_PITCHER_HITALLOWED
        score += self.__totEarnedRuns * gsXP_PITCHER_EARNEDRUN

        score += self.__totWalksThrown * gsXP_PITCHER_WALKSTHROWN
        return score

    def countXP(self):
        return self.getPitcherScore()
        XP = 0
        XP += self.__totKs * gsXP_PITCHER_K
        XP += self.__shutouts * gsXP_PITCHER_SHUTOUT
        XP += self.__noHitters * gsXP_PITCHER_NOHITTER
        XP += self.__wins * gsXP_PITCHER_WIN
        XP += self.__totOutsThrown * gsXP_PITCHER_OUT
        return XP


    #pitchType: fastball, curveball, etc...
    #pitchCall: ball/strike/contact
    #pitchSpeed: velocity
    def addPitchThrown(self, pitchType, pitchZone, pitchSpeed, pitchCall, playObj=None):
        if playObj != None:
            #Tally Play Stats
            self.__batterResults += [str(playObj)]
            
            if playObj.isSingle():#Single
                self.__totHitsAllowed += 1
                self.__tot1BsAllowed += 1
                self.__totStrikesThrown += 1
            elif playObj.isDouble():#Double
                self.__totHitsAllowed += 1
                self.__tot2BsAllowed += 1
                self.__totStrikesThrown += 1
            elif playObj.isTriple():#Triple
                self.__totHitsAllowed += 1
                self.__tot3BsAllowed += 1
                self.__totStrikesThrown += 1
            elif playObj.isHomeRun():#Homer
                self.__totHitsAllowed += 1
                self.__totHRsAllowed += 1
                self.__totStrikesThrown += 1
                self.__longestHRAllowed = playObj.getHitDistance()
                if playObj.isGrandSlam():
                    self.__totGrandSlamsAllowed += 1
            elif playObj.isOut():#Out
                self.__totOutsThrown += 1
                if not playObj.isStrikeOut(): 
                    self.__totStrikesThrown += 1
            elif playObj.isDoublePlay():#double play
                self.__totDPsThrown += 1
                self.__totStrikesThrown += 1
            elif playObj.isTriplePlay():#triple play
                self.__totTPsThrown += 1
                self.__totStrikesThrown += 1

            #always check to see if a play generated earned runs
            self.__totEarnedRuns += playObj.runsScoredOnPlay()

        #Tally Pitch Stats
        self.__totPitchesThrown += 1

        if pitchType == gsCURVEBALL:
            self.__totCurveballsThrown += 1
        elif pitchType == gsFASTBALL:
            self.__totFastballsThrown += 1
        elif pitchType == gsSLIDER:
            self.__totSlidersThrown += 1
        elif pitchType == gsCHANGEUP:
            self.__totChangeupsThrown += 1
        elif pitchType == gsKNUCKLEBALL:
            self.__totKnuckleballsThrown += 1
        elif pitchType == gsSINKER:
            self.__totSinkersThrown += 1
        elif pitchType == gsSPITBALL:
            self.__totSpitballsThrown += 1
        elif pitchType == gsFORKBALL:
            self.__totForkballsThrown += 1
    
        if self.__fastestPitchThrown < pitchSpeed:
            self.__fastestPitchThrown = pitchSpeed
        
        if pitchCall == None:# and playObj != None:
            None
        elif pitchCall == gsPITCHCALL_STRIKE:
            self.__totStrikesThrown += 1
        elif pitchCall == gsPITCHCALL_BALL:
            self.__totBallsThrown += 1
        elif pitchCall == gsPITCHCALL_FOUL:
            if self.__totStrikesThrown < gsMAXSTRIKECOUNT-1:
                self.__totStrikesThrown += 1
        elif pitchCall == gsPITCHCALL_STRIKEOUT:
            self.__totStrikesThrown += 1
            self.__totKs += 1
        elif pitchCall == gsPITCHCALL_WALK:
            self.__totBallsThrown += 1
            self.__totWalksThrown += 1
        else: #we missed a case
            print "DEBUG: MISSED CASE in addPitchThrown(%s, %d, %d, %s, %s)" % (pitchType, 
                                                                                pitchZone, 
                                                                                pitchSpeed, 
                                                                                str(pitchCall),#last 2 args could be None 
                                                                                str(pitchResult))

            
        #TODO: track the zone the pitch was thrown to
        
###############################
#
#
#
#
#
#
###############################
class BatterStats:

    def __init__(self, statSubType, initValue=0):#should optionally take an atBatResult parse it and set values
        self.__statType = gsSTATTYPE_BATTER_STATS
        self.__statSubType = statSubType

        self.__atBatResults = []
        self.__gamesPlayed = initValue
        self.__wins = initValue
        self.__losses = initValue
        self.__totAtBats = initValue

        self.__totHits = initValue #perZone
        self.__currentHitStreak = initValue
        self.__longestHitStreak = initValue
        self.__totCycles = initValue

        self.__totHRs = initValue
        self.__longestHR = initValue
        self.__totGrandSlams = initValue

        self.__tot1Bs = initValue
        self.__tot2Bs = initValue
        self.__tot3Bs = initValue

        self.__totKd = initValue
        self.__totDPHitInto = initValue
        self.__totTPHitInto = initValue

        self.__totWalks = initValue
        self.__totHBP = initValue
        self.__totIBB = initValue
        self.__totRuns = initValue

        self.__totRBIs = initValue
        self.__totAtBatsWithRunnersInScoringPos = initValue
        self.__totHitsWithRunnersInScoringPos = initValue
        self.__totRBIsWithRunnersInScoringPos = initValue
        self.__totRunnersLeftInScoringPos = initValue
        return


    def statType(self):
        return self.__statType

    def isPitcherStats(self):
        return self.__statType == gsSTATTYPE_PITCHER_STATS

    def isBatterStats(self):
        return self.__statType == gsSTATTYPE_BATTER_STATS

    #can't call this on objects read from disk because it doesn't persist
    def statSubType(self):
        return self.__statSubType

    def incRunsScored(self):
        self.__totRuns += 1

    def countXP(self):
        XP = 0
        XP += gsXP_BATTER_WIN * self.__wins
        XP += gsXP_BATTER_ATBAT * self.__totAtBats
        XP += gsXP_BATTER_GAMEPLAYED * self.__gamesPlayed
        XP += gsXP_BATTER_SINGLE * self.__tot1Bs
        XP += gsXP_BATTER_DOUBLE * self.__tot2Bs
        XP += gsXP_BATTER_TRIPLE * self.__tot3Bs
        XP += gsXP_BATTER_HOMERUN * self.__totHRs
        XP += gsXP_BATTER_RBI * self.__totRBIs
        XP += gsXP_BATTER_RUN * self.__totRuns
        XP += gsXP_BATTER_WALK * self.__totWalks
        XP += gsXP_BATTER_GRANDSLAM * self.__totGrandSlams
        XP += gsXP_BATTER_GRANDSLAM * self.__totCycles
        return XP

    def __iadd__(self, other):
        if self.statType() != other.statType():
            print "Cannot add stat type %s and %s\n" % (self.statType(), other.statType())

        self.__gamesPlayed += other.__gamesPlayed
        self.__totAtBats += other.__totAtBats
        self.__totHits += other.__totHits
       
        if other.statSubType() == gsSTATSUBTYPE_ENDGAMESTATS:
            self.__wins += other.__wins
            self.__losses += other.__losses

            #check for cycles
            if other.__totHits >= 4 and \
                    other.__totHRs > 0 and \
                    other.__tot1Bs > 0 and \
                    other.__tot2Bs > 0 and \
                    other.__tot3Bs > 0:
                other.__totCycles += 1
                #TODO: make sure we checked for cycles first
                self.__totCycles += other.__totCycles


            if other.__totHits > 0:
                self.__currentHitStreak += 1
            else:
                self.__currentHitStreak = 0

            if self.__currentHitStreak > self.__longestHitStreak:
                self.__longestHitStreak = self.__currentHitStreak

            #to make this a list of lists add [] then each game is a sub list
            #we probably need to limit how much history we keep here
            #but it is good to save until the end of the game for post processing
            #as well as testing purposes
            self.__atBatResults += [other.__atBatResults]
        else:
            self.__atBatResults += [other.__atBatResults]            

        self.__totHRs += other.__totHRs
        if other.__longestHR > self.__longestHR:
            self.__longestHR = other.__longestHR
        self.__totGrandSlams += other.__totGrandSlams
        self.__tot1Bs += other.__tot1Bs
        self.__tot2Bs += other.__tot2Bs
        self.__tot3Bs += other.__tot3Bs
        self.__totKd += other.__totKd
        self.__totDPHitInto += other.__totDPHitInto
        self.__totTPHitInto += other.__totTPHitInto
        self.__totWalks += other.__totWalks
        self.__totHBP += other.__totHBP
        self.__totIBB += other.__totIBB
        self.__totRuns += other.__totRuns
        self.__totRBIs += other.__totRBIs
        self.__totAtBatsWithRunnersInScoringPos += other.__totAtBatsWithRunnersInScoringPos
        self.__totHitsWithRunnersInScoringPos += other.__totHitsWithRunnersInScoringPos
        self.__totRBIsWithRunnersInScoringPos += other.__totRBIsWithRunnersInScoringPos
        self.__totRunnersLeftInScoringPos += other.__totRunnersLeftInScoringPos
        return self

    def __getstate__(self):
        dictStr = "{'statType':'%s'," +\
            "'atBatResults':%s," + \
            "'totAtBats':%d," + \
            "'gamesPlayed':%d," + \
            "'wins':%d," +\
            "'losses':%d," +\
            "'totHits':%d," + \
            "'currentHitStreak':%d," + \
            "'longestHitStreak':%d," + \
            "'totCycles':%d," + \
            "'totHRs':%d," + \
            "'longestHR':%d," + \
            "'totGrandSlams':%d," + \
            "'tot1Bs':%d," + \
            "'tot2Bs':%d," + \
            "'tot3Bs':%d," + \
            "'totKd':%d," + \
            "'totDPHitInto':%d," + \
            "'totTPHitInto':%d," + \
            "'totWalks':%d," + \
            "'totHBP':%d," + \
            "'totIBB':%d," + \
            "'totRuns':%d," + \
            "'totRBIs':%d," + \
            "'totAtBatsWithRunnersInScoringPos':%d," + \
            "'totHitsWithRunnersInScoringPos':%d," + \
            "'totRBIsWithRunnersInScoringPos':%d," + \
            "'totRunnersLeftInScoringPos':%d}"

        return dictStr % (self.__statType, self.__atBatResults, self.__totAtBats, 
                          self.__gamesPlayed, self.__wins, self.__losses, self.__totHits,
                          self.__currentHitStreak, self.__longestHitStreak,
                          self.__totCycles, self.__totHRs, 
                          self.__longestHR, self.__totGrandSlams, self.__tot1Bs, 
                          self.__tot2Bs, self.__tot3Bs, self.__totKd, self.__totDPHitInto, 
                          self.__totTPHitInto, self.__totWalks, self.__totHBP, 
                          self.__totIBB, self.__totRuns, self.__totRBIs, 
                          self.__totAtBatsWithRunnersInScoringPos, 
                          self.__totHitsWithRunnersInScoringPos, 
                          self.__totRBIsWithRunnersInScoringPos, 
                          self.__totRunnersLeftInScoringPos)

    def safe_setstatevar(self, key, dict, defaultVal):
        val = None
        try:
            val = dict[key]
            setattr(self, "__"+key, val)
        except KeyError:
            setattr(self, "__"+key, defaultVal)
            

    def __setstate__(self, dictStr):
        #print type(dictStr)
        #print dictStr
        #d = eval(dictStr)
        d = dictStr
        #self.__statType = d['statType']
        self.safe_setstatevar('statType', d, gsSTATTYPE_BATTER_STATS)
        self.__atBatResults = d['atBatResults']
        self.__totAtBats = d['totAtBats']
        self.__gamesPlayed = d['gamesPlayed']
        self.__wins = d['wins']
        self.__losses = d['losses']
        self.__totHits = d['totHits']
        self.__currentHitStreak = d['currentHitStreak']
        self.__longestHitStreak = d['longestHitStreak']
        self.__totCycles = d['totCycles']

        self.__totHRs = d['totHRs']
        self.__longestHR = d['longestHR']
        self.__totGrandSlams = d['totGrandSlams']

        self.__tot1Bs = d['tot1Bs']
        self.__tot2Bs = d['tot2Bs']
        self.__tot3Bs = d['tot3Bs']

        self.__totKd = d['totKd']
        self.__totDPHitInto = d['totDPHitInto']
        self.__totTPHitInto = d['totTPHitInto']

        self.__totWalks = d['totWalks']
        self.__totHBP = d['totHBP']
        self.__totIBB = d['totIBB']
        self.__totRuns = d['totRuns']

        self.__totRBIs = d['totRBIs']
        self.__totAtBatsWithRunnersInScoringPos = d['totAtBatsWithRunnersInScoringPos']
        self.__totHitsWithRunnersInScoringPos = d['totHitsWithRunnersInScoringPos']
        self.__totRBIsWithRunnersInScoringPos = d['totRBIsWithRunnersInScoringPos']
        self.__totRunnersLeftInScoringPos = d['totRunnersLeftInScoringPos']
        return self


    #
    #
    #
    #Used For Generating League Leaders
    #
    def _hasAtBats(self):
        return self.__totAtBats != 0

    def computeBattingAvg(self):
        return computeBattingAvg(self.__totAtBats, self.__totHits)
    
    def computeSluggingPct(self):
        return computeSluggingPct(self.__tot1Bs, self.__tot2Bs, self.__tot3Bs, self.__totHRs, self.__totAtBats)

    def computeOnBasePct(self):
        return computeOnBasePct2(self.__totHits, self.__totWalks, self.__totHBP, self.__totAtBats)

    def computeWinPct(self):
        return computeWinPct(self.__wins, self.__losses)

    def getGamesPlayed(self):
        return self.__gamesPlayed

    def getTotAtBats(self):
        return self.__totAtBats

    def getWins(self):
        if self.__gamesPlayed == 0:
            return None
        return self.__wins

    def getLosses(self):
        if self.__gamesPlayed == 0:
            return None
        return self.__losses        

    def getRBIs(self):
        if not self._hasAtBats():
            return None
        return self.__totRBIs

    def getAtBatsWithRunnersInScoringPos(self):
        return self.__totAtBatsWithRunnersInScoringPos

    def getTotHitsWithRunnersInScoringPos(self):
        return self.__totHitsWithRunnersInScoringPos

    def getTotRBIsWithRunnersInScoringPos(self):
        return self.__totRBIsWithRunnersInScoringPos

    def getTotRunnersLeftInScoringPos(self):
        return self.__totRunnersLeftInScoringPos

    def getHRs(self):
        if not self._hasAtBats():
            return None
        return self.__totHRs

    def getLngstHR(self):
        if not self._hasAtBats():
            return None
        return self.__longestHR

    def getGrandSlams(self):
        return self.__totGrandSlams

    def getCycles(self):
        return self.__totCycles

    def getRuns(self):
        if not self._hasAtBats():
            return None
        return self.__totRuns

    def getCurrentHitStreak(self):
        return self.__currentHitStreak

    def getLngstHitStreak(self):
        if not self._hasAtBats():
            return None
        return self.__longestHitStreak

    def getTotalHits(self):
        return self.__totHits

    def getSingles(self):
        if not self._hasAtBats():
            return None
        return self.__tot1Bs

    def getDoubles(self):
        if not self._hasAtBats():
            return None
        return self.__tot2Bs

    def getTriples(self):
        if not self._hasAtBats():
            return None
        return self.__tot3Bs

    def getWalks(self):
        if not self._hasAtBats():
            return None
        return self.__totWalks

    ###

    def __str__(self):
        return self.__getstate__()

    #
    #
    #This shold only be called on the initialization 
    # of the stats in the PlayerGameState object
    def setGamesPlayed(self, n):
        self.__gamesPlayed = n


    def incWins(self):
        self.__wins += 1

    def incLosses(self):
        self.__losses += 1

    #
    #
    #need this because this is
    #the only stat we currently track
    #that can be updated 
    def incRuns(self):
        self.__totRuns += 1
    #
    #
    #called in init of AtBatResult()
    def addAtBat(self):
        self.__totAtBats += 1

    def addPitchReceived(self, pitchType, pitchZone, pitchSpeed, pitchCall, 
                         runnersInScoringPos, playObj=None):
        if playObj != None:

            self.__atBatResults += [str(playObj)]

            #Check for runners in scoring position
            if runnersInScoringPos > 0:
                self.__totAtBatsWithRunnersInScoringPos += 1
                if playObj.isHit():#if its a hit
                    self.__totHitsWithRunnersInScoringPos += 1
                    self.__totRBIsWithRunnersInScoringPos += playObj.runsScoredOnPlay()
                #elif playObj.isOut() and \
                if playObj.runsScoredOnPlay() < runnersInScoringPos:
                    self.__totRunnersLeftInScoringPos += \
                        runnersInScoringPos - playObj.runsScoredOnPlay()

            #inc total hits
            if playObj.isHit():
                self.__totHits += 1

            if playObj.isOut():#Out
                None
            elif playObj.isSingle():
                self.__tot1Bs += 1
            elif playObj.isDouble():#Double
                self.__tot2Bs += 1
            elif playObj.isTriple():#Triple
                self.__tot3Bs += 1
            elif playObj.isHomeRun():#Homer
                self.__totHRs += 1
                self.__totRuns += 1
                self.__longestHR = playObj.getHitDistance()
            elif playObj.isDoublePlay():#double play
                self.__totDPHitInto += 1
            elif playObj.isTriplePlay():#triple play
                self.__totTPHitInto += 1
            
            self.__totRBIs += playObj.runsScoredOnPlay()
            if playObj.isGrandSlam():
                self.__totGrandSlams += 1
        
        elif runnersInScoringPos > 0:
            #playObj == None
            self.__totRunnersLeftInScoringPos += runnersInScoringPos
            self.__totAtBatsWithRunnersInScoringPos += 1
        
        if pitchCall == gsPITCHCALL_WALK:
            self.__totWalks += 1
            self.__totAtBats -= 1 #doesn't count as at bat
        elif pitchCall == gsPITCHCALL_STRIKEOUT:
            self.__totKd += 1

            
#TODO: Class FielderStats

x = """class PlayerStats:

    def __init__(self, BatterStats=None, PitcherStats=None):
        if BatterStats == None:
            self.__batterStats = BatterStats()
        else:
            self.__batterStats = BatterStats
        if PitcherStats == None:
            self.__pitcherStats = PitcherStats()
        else:
            self.__pitcherStats = PitcherStats

        #TODO: class FielderStats
        return

    def __iadd__(statsA, statsB):
        return
"""


def main():
    import json

    p1 = PitcherStats(gsSTATSUBTYPE_SINGLEPLAYSTATS,2)
    print p1
    print
    p2 = PitcherStats(gsSTATSUBTYPE_SINGLEPLAYSTATS, 1)
    print p2
    print
    p1 += p2
    print p1

    print
    b1 = BatterStats(gsSTATSUBTYPE_SINGLEPLAYSTATS, 2)
    print b1
    b2 = BatterStats(gsSTATSUBTYPE_SINGLEPLAYSTATS, 1)
    print b2
    print 
    b1 += b2

    print b1

    b2.__setstate__(b1.__getstate__())

    print
    print b2

    eval(b2.__getstate__())
    eval(p1.__getstate__())

    ps = PitcherStats(gsSTATSUBTYPE_SINGLEPLAYSTATS).__setstate__(p1.__getstate__())
    print ps
    #file = open("pitcher.stats", "w+")
    #cPickle.dump(file, "

    js = json.dumps(PitcherStats(gsSTATSUBTYPE_SINGLEPLAYSTATS).__getstate__())
    print "JSON: %s\n" % js


    p1 = PitcherStats(gsSTATSUBTYPE_SINGLEPLAYSTATS)
    p2 = PitcherStats(gsSTATSUBTYPE_ENDGAMESTATS, 1) 
    p1 += p2
    print p1
    
    b1 = BatterStats(gsSTATSUBTYPE_SINGLEPLAYSTATS)
    b2 = BatterStats(gsSTATSUBTYPE_ENDGAMESTATS, 1) 
    b1 += b2
    print b1

if __name__ == "__main__":
    main()

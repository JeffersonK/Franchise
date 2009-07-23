import cPickle


#class PerZoneStat:
#    def __init__(self, initValue=0):
#        self.__statZones = [gsNUMBERZONES]
#        for i in gsNUMBERZONES:
#            self.__statZones += [(initValue,initValue)

    
class PitcherStats:
    def __init__(self, initValue=0):#should optionally take an atBatResult parse it and set values
        self.__batterResults = []#list of lists where inner list is a game
        self.__starts = initValue
        self.__wins = initValue
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
        self.__totWalksThrown = initValue
        self.__totOutsThrown = initValue
        self.__totDPsThrown = initValue
        self.__totTPsThrown = initValue
        self.__totEarnedRuns = initValue
        self.__totPitchesThrown = initValue
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
        return
        
    def __iadd__(self, other):
        self.__batterResults += other.__batterResults
        self.__starts += other.__starts
        
        if other.__wins > 0:
            self.__wins += other.__wins
            self.__currentWinStreak += other.__currentWinStreak
            if self.__currentWinStreak > self.__longestWinStreak:
                self.__longestWinStreak = self.__currentWinStreak
                
            self.__currentLosingStreak = 0
        
        if other.__losses > 0:
            self.__losses += other.__losses
            self.__currentLosingStreak += other.__currentLosingStreak
            if self.__currentLosingStreak > self.__longestLosingStreak:
                self.__longestLosingStreak = self.__currentLosingStreak
            
            self.__currentWinStreak = 0

        self.__saves += other.__saves
        self.__shutouts += other.__shutouts
        self.__noHitters += other.__noHitters
        self.__perfectGames += other.__perfectGames
        self.__totBattersFaced += other.__totBattersFaced
        self.__totKs += other.__totKs
        self.__totWalksThrown += other.__totWalksThrown
        self.__totOutsThrown += other.__totOutsThrown
        self.__totDPsThrown += other.__totDPsThrown
        self.__totTPsThrown += other.__totTPsThrown
        self.__totEarnedRuns += other.__totEarnedRuns
        self.__totPitchesThrown += other.__totPitchesThrown
        self.__totStrikesThrown += other.__totStrikesThrown
        self.__totBallsThrown += other.__totBallsThrown
        self.__totHitsAllowed += other.__totHitsAllowed
        self.__totBattersHBP += other.__totBattersHBP
        self.__totHRsAllowed += other.__totHRsAllowed
        self.__totGrandSlamsAllowed += other.__totGrandSlamsAllowed
        self.__longestHRAllowed += other.__longestHRAllowed
        self.__tot1BsAllowed += other.__tot1BsAllowed
        self.__tot2BsAllowed += other.__tot2BsAllowed
        self.__tot3BsAllowed += other.__tot3BsAllowed
        return self

    def __getstate__(self):
        dictStr = "{'batterResults':%s," + \
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
            "'totWalksThrown':%d," + \
            "'totOutsThrown':%d," + \
            "'totDPsThrown':%d," + \
            "'totTPsThrown':%d," + \
            "'totEarnedRuns':%d," + \
            "'totPitchesThrown':%d," + \
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
            
        
        return dictStr % (self.__batterResults, self.__starts, self.__wins,
                          self.__currentWinStreak, self.__longestWinStreak, 
                          self.__losses, self.__currentLosingStreak, 
                          self.__longestLosingStreak, self.__saves, 
                          self.__shutouts, self.__noHitters, self.__perfectGames,
                          self.__totBattersFaced, self.__totKs, self.__totWalksThrown, 
                          self.__totOutsThrown, self.__totDPsThrown, self.__totTPsThrown, 
                          self.__totEarnedRuns, self.__totPitchesThrown, 
                          self.__totStrikesThrown, self.__totBallsThrown, 
                          self.__totHitsAllowed, self.__totBattersHBP, 
                          self.__totHRsAllowed, self.__totGrandSlamsAllowed, 
                          self.__longestHRAllowed, self.__tot1BsAllowed, 
                          self.__tot2BsAllowed, self.__tot3BsAllowed)


    def __setstate__(self, dictStr):
        d = eval(dictStr)
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
        self.__totWalksThrown = d['totWalksThrown']
        self.__totOutsThrown = d['totOutsThrown']
        self.__totDPsThrown = d['totDPsThrown']
        self.__totTPsThrown = d['totTPsThrown']
        self.__totEarnedRuns = d['totEarnedRuns']
        self.__totPitchesThrown = d['totPitchesThrown']
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

class BatterStats:

    def __init__(self, initValue=0):#should optionally take an atBatResult parse it and set values
        self.__atBatResults = []
        self.__totAtBats = initValue

        self.__totHits = initValue
        self.__currentHitStreak = initValue
        self.__totCycles = initValue

        self.__totHRs = initValue
        self.__longestHR = initValue
        self.__totGrandSlams = initValue

        self.__tot1Bs = initValue
        self.__tot2Bs = initValue
        self.__tot3Bs = initValue

        self.__totKd = initValue
        self.__totDBHitInto = initValue
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


    def __iadd__(self, other):
        self.__atBatResults += other.__atBatResults
        self.__totAtBats += other.__totAtBats
        self.__totHits += other.__totHits
        if self.__totHits > 0:
            self.__currentHitStreak += 1
        self.__totCycles += other.__totCycles
        self.__totHRs += other.__totHRs
        if other.__longestHR > self.__longestHR:
            self.__longestHR = other.__longestHR
        self.__totGrandSlams += other.__totGrandSlams
        self.__tot1Bs += other.__tot1Bs
        self.__tot2Bs += other.__tot2Bs
        self.__tot3Bs += other.__tot3Bs
        self.__totKd += other.__totKd
        self.__totDBHitInto += other.__totDBHitInto
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
        dictStr = "{'atBatResults':%s," + \
            "'totAtBats':%d," + \
            "'totHits':%d," + \
            "'currentHitStreak':%d," + \
            "'totCycles':%d," + \
            "'totHRs':%d," + \
            "'longestHR':%d," + \
            "'totGrandSlams':%d," + \
            "'tot1Bs':%d," + \
            "'tot2Bs':%d," + \
            "'tot3Bs':%d," + \
            "'totKd':%d," + \
            "'totDBHitInto':%d," + \
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

        return dictStr % (self.__atBatResults, self.__totAtBats,self.__totHits,
                          self.__currentHitStreak, self.__totCycles, self.__totHRs, 
                          self.__longestHR, self.__totGrandSlams, self.__tot1Bs, 
                          self.__tot2Bs, self.__tot3Bs, self.__totKd, self.__totDBHitInto, 
                          self.__totTPHitInto, self.__totWalks, self.__totHBP, 
                          self.__totIBB, self.__totRuns, self.__totRBIs, 
                          self.__totAtBatsWithRunnersInScoringPos, 
                          self.__totHitsWithRunnersInScoringPos, 
                          self.__totRBIsWithRunnersInScoringPos, 
                          self.__totRunnersLeftInScoringPos)

    def __setstate__(self, dictStr):
        d = eval(dictStr)
        self.__atBatResults = d['atBatResults']
        self.__totAtBats = d['totAtBats']

        self.__totHits = d['totHits']
        self.__currentHitStreak = d['currentHitStreak']
        self.__totCycles = d['totCycles']

        self.__totHRs = d['totHRs']
        self.__longestHR = d['longestHR']
        self.__totGrandSlams = d['totGrandSlams']

        self.__tot1Bs = d['tot1Bs']
        self.__tot2Bs = d['tot2Bs']
        self.__tot3Bs = d['tot3Bs']

        self.__totKd = d['totKd']
        self.__totDBHitInto = d['totDBHitInto']
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


    def __str__(self):
        return self.__getstate__()

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

import json
def main():

    p1 = PitcherStats(2)
    print p1
    print
    p2 = PitcherStats(1)
    print p2
    print
    p1 += p2
    print p1

    print
    b1 = BatterStats(2)
    print b1
    b2 = BatterStats(1)
    print b2
    print 
    b1 += b2

    print b1

    b2.__setstate__(b1.__getstate__())

    print
    print b2

    eval(b2.__getstate__())
    eval(p1.__getstate__())

    ps = PitcherStats().__setstate__(p1.__getstate__())
    print ps
    #file = open("pitcher.stats", "w+")
    #cPickle.dump(file, "


    js = json.dumps(PitcherStats().__getstate__())
    print "JSON: %s\n" % js

if __name__ == "__main__":
    main()

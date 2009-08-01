import ObjectDB
import os
from pprint import *

def addLeader(list, playerName, stat):
    if stat != None:
        list += [(playerName, stat)]
    
#def addLeaderBoard(leaderboard, list, statGroup, statName):
#    list.sort(cmp)
    

def leagueleaders(dbLoc, objFileExt, outfile=None):
    gsPlayerDB = ObjectDB.ObjectDB(dbLoc,objFileExt)
    l = gsPlayerDB.iteritems(dbLoc, objFileExt)
    avgs = []
    HRs = []
    RBIs = []
    slg = []
    obp = []
    hitStreak = []
    runs = []
    
    #gamesPlayed = []
    bwins = []
    bwinPct = []
    LngstHRs = []
    XP = []
    Level = []

    Ks = []
    WalksThrown = []
    ERA = []
    pWinPct = []
    #bestPitcherScore = []
    #worstPitcherScore = []
    Loot = []

    bXPScores = []
    pBestXPScores = []
    pWorstXPScores = []
    pOverallScore = []

    leaderboard = {'batting':{},'record':{},'character':{},'pitching':{}}

    for (guid, plyr) in l:
        addLeader(XP, plyr.getName(), plyr.getExperience())
        addLeader(avgs, plyr.getName(), plyr.getBatterStats().computeBattingAvg())
        addLeader(HRs,plyr.getName(), plyr.getBatterStats().getHRs())
        addLeader(LngstHRs,plyr.getName(), plyr.getBatterStats().getLngstHR())
        addLeader(RBIs, plyr.getName(), plyr.getBatterStats().getRBIs())
        addLeader(slg, plyr.getName(), plyr.getBatterStats().computeSluggingPct())
        addLeader(obp, plyr.getName(), plyr.getBatterStats().computeOnBasePct())
        addLeader(hitStreak, plyr.getName(), plyr.getBatterStats().getLngstHitStreak()) 
        addLeader(runs,plyr.getName(), plyr.getBatterStats().getRuns())
        addLeader(bwins,plyr.getName(), plyr.getBatterStats().getWins())
        addLeader(bwinPct, plyr.getName(), plyr.getBatterStats().computeWinPct())
        addLeader(Ks, plyr.getName(), plyr.getPitcherStats().getTotStrikeouts())
        addLeader(pWinPct,plyr.getName(), plyr.getPitcherStats().computeWinPct())
        addLeader(WalksThrown, plyr.getName(), plyr.getPitcherStats().getTotWalks()) 
        addLeader(ERA, plyr.getName(), plyr.getPitcherStats().computeERA())  
        addLeader(Level, plyr.getName(), plyr.getLevel())
        addLeader(Loot, plyr.getName(), plyr.getMoney())
        addLeader(bXPScores, plyr.getName(), plyr.getBatterStats().getHighXPScore())
        addLeader(pBestXPScores, plyr.getName(), plyr.getPitcherStats().getBestPitcherScore())
        addLeader(pWorstXPScores, plyr.getName(), plyr.getPitcherStats().getWorstPitcherScore())
        addLeader(pOverallScore, plyr.getName(), plyr.getPitcherStats().computeAvgPitcherScore())

    pOverallScore.sort(cmp)
    leaderboard['pitching']['PITCHER_AVG_SCORE'] = pOverallScore
    bXPScores.sort(cmp)
    leaderboard['batting']['BATTER_XP_SCORES'] = bXPScores
    pBestXPScores.sort(cmp)
    leaderboard['pitching']['PITCHER_HIGH_SCORES'] = pBestXPScores
    pWorstXPScores.sort(cmp)
    pWorstXPScores.reverse()
    leaderboard['pitching']['PITCHER_WORST_SCORES'] = pWorstXPScores
    Loot.sort(cmp)
    leaderboard['character']['MONEY'] = Loot
    ERA.sort(cmp)
    leaderboard['pitching']['ERA'] = ERA
    WalksThrown.sort(cmp)
    leaderboard['pitching']['WALKS_THROWN'] = WalksThrown
    pWinPct.sort(cmp)
    leaderboard['pitching']['PITCHER_WINPCT'] = pWinPct
    Ks.sort(cmp)
    leaderboard['pitching']['STRIKEOUTS'] = Ks
    XP.sort(cmp)
    leaderboard['character']['XP'] = XP
    Level.sort(cmp)
    leaderboard['character']['LEVEL'] = Level
    avgs.sort(cmp)
    leaderboard['batting']['AVG'] = avgs
    HRs.sort(cmp)
    leaderboard['batting']['HRs'] = HRs
    LngstHRs.sort(cmp)
    leaderboard['batting']['longestHR'] = LngstHRs
    RBIs.sort(cmp)
    leaderboard['batting']['RBIs'] = RBIs
    slg.sort(cmp)
    leaderboard['batting']['SLG'] = slg
    obp.sort(cmp)
    leaderboard['batting']['OBP'] = obp
    hitStreak.sort(cmp)
    leaderboard['batting']['HITSTRK'] = hitStreak
    runs.sort(cmp)
    leaderboard['batting']['RUNS'] = runs
    bwins.sort(cmp)
    leaderboard['record']['WINS'] = bwins
    bwinPct.sort(cmp)
    leaderboard['record']['BATTER_WINPCT'] = bwinPct
    if outfile != None:
        file = open(os.path.join(dbLoc,outfile), 'w+')
        if file == None:
            print "Could Not open file %s." % outfile
        file.write(str(leaderboard))
        file.close()

    return leaderboard

    
def cmp(x,y):
    if x[1] < y[1]:
        return 1
    elif x[1] == y[1]:
        return 0
    else:
        return -1

def printll(statName, stats):
    print "\n-- League Leaders (%s) ---" % statName
    pprint(stats)

def main():

    ll = leagueleaders("playersdb","plr", "leagueleaders.txt")
    pprint(ll)
    return

if __name__ == "__main__":
    main()

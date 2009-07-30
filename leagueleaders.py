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

    leaderboard = {'batting':{},'record':{},'character':{},'pitching':{}}

    for (guid, plyr) in l:
        #XP += [(plyr.getName(), plyr.getExperience())]
        addLeader(XP, plyr.getName(), plyr.getExperience())

        #avgs += [(plyr.getName(), plyr.getBatterStats().computeBattingAvg())]
        addLeader(avgs, plyr.getName(), plyr.getBatterStats().computeBattingAvg())
 
        #HRs += [(plyr.getName(), plyr.getBatterStats().getHRs())]
        addLeader(HRs,plyr.getName(), plyr.getBatterStats().getHRs())
 
        #LngstHRs += [(plyr.getName(), plyr.getBatterStats().getLngstHR())]
        addLeader(LngstHRs,plyr.getName(), plyr.getBatterStats().getLngstHR())
        
        #RBIs += [(plyr.getName(), plyr.getBatterStats().getRBIs())]
        addLeader(RBIs, plyr.getName(), plyr.getBatterStats().getRBIs())
 
        #slg += [(plyr.getName(), plyr.getBatterStats().computeSluggingPct())]
        addLeader(slg, plyr.getName(), plyr.getBatterStats().computeSluggingPct())

        #obp += [(plyr.getName(), plyr.getBatterStats().computeOnBasePct())]
        addLeader(obp, plyr.getName(), plyr.getBatterStats().computeOnBasePct())
    
        #hitStreak += [(plyr.getName(), plyr.getBatterStats().getLngstHitStreak())]
        addLeader(hitStreak, plyr.getName(), plyr.getBatterStats().getLngstHitStreak()) 
        
        #runs += [(plyr.getName(), plyr.getBatterStats().getRuns())]
        addLeader(runs,plyr.getName(), plyr.getBatterStats().getRuns())
 
        #gamesPlayed += [(plyr.getName(), plyr.getBatterStats().getGamesPlayed())]

        #bwins += [(plyr.getName(), plyr.getBatterStats().getWins())]
        addLeader(bwins,plyr.getName(), plyr.getBatterStats().getWins())
 
        #bwinPct += [(plyr.getName(), plyr.getBatterStats().computeWinPct())] 
        addLeader(bwinPct, plyr.getName(), plyr.getBatterStats().computeWinPct())
        #"%s - %s" % (str(plyr.getBatterStats().getWins()),str(plyr.getBatterStats().getLosses())) )]
        
        #Ks += [(plyr.getName(), plyr.getPitcherStats().getTotStrikeouts())]
        addLeader(Ks, plyr.getName(), plyr.getPitcherStats().getTotStrikeouts())
        
        addLeader(pWinPct,plyr.getName(), plyr.getPitcherStats().computeWinPct())

        addLeader(WalksThrown, plyr.getName(), plyr.getPitcherStats().getTotWalks()) 
        
        addLeader(ERA, plyr.getName(), plyr.getPitcherStats().computeERA())  

        #addLeader(bestPitcherScores, plyr.getName(), plyr.getPitcherStats().getBestPitcherScore())

        #addLeader(wostPitcherScores, plyr.getName(), plyr.getPitcherStats().getWorstPitcherScore())
        addLeader(Level, plyr.getName(), plyr.getLevel())

        addLeader(Loot, plyr.getName(), plyr.getMoney())

    Loot.sort(cmp)
    leaderboard['character']['MONEY'] = Loot

    ERA.sort(cmp)
    leaderboard['pitching']['ERA'] = ERA

    WalksThrown.sort(cmp)
    leaderboard['pitching']['WALKS THROWN'] = WalksThrown
    
    pWinPct.sort(cmp)
    leaderboard['pitching']['PITCHER WINPCT'] = pWinPct

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
    leaderboard['record']['BATTER WINPCT'] = bwinPct

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

    ll = leagueleaders("players","plr", "leagueleaders.txt")
    pprint(ll)
    return

if __name__ == "__main__":
    main()

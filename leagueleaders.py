import ObjectDB
import os
from pprint import *

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
    wins = []
    winPct = []
    LngstHRs = []
    XP = []
    leaderboard = {'batting':{},'record':{},'character':{}}

    for (guid, plyr) in l:
        XP += [(plyr.getName(), plyr.getExperience())]
        avgs += [(plyr.getName(), plyr.getBatterStats().computeBattingAvg())]
        HRs += [(plyr.getName(), plyr.getBatterStats().getHRs())]
        LngstHRs += [(plyr.getName(), plyr.getBatterStats().getLngstHR())]
        RBIs += [(plyr.getName(), plyr.getBatterStats().getRBIs())]
        slg += [(plyr.getName(), plyr.getBatterStats().computeSluggingPct())]
        obp += [(plyr.getName(), plyr.getBatterStats().computeOnBasePct())]
        hitStreak += [(plyr.getName(), plyr.getBatterStats().getLngstHitStreak())]
        runs += [(plyr.getName(), plyr.getBatterStats().getRuns())]
        #gamesPlayed += [(plyr.getName(), plyr.getBatterStats().getGamesPlayed())]
        wins += [(plyr.getName(), plyr.getBatterStats().getWins())]
        winPct += [(plyr.getName(), plyr.getBatterStats().computeWinPct(), 
                    "%s - %s" % (str(plyr.getBatterStats().getWins()),str(plyr.getBatterStats().getLosses())) )]

        
    XP.sort(cmp)
    leaderboard['character']['XP'] = XP

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

    wins.sort(cmp)
    leaderboard['record']['WINS'] = wins
    
    winPct.sort(cmp)
    leaderboard['record']['WINPCT'] = winPct

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

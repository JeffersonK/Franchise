import ObjectDB
from pprint import *


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

    gsPlayerDB = ObjectDB.ObjectDB("players","plr")
    l = gsPlayerDB.iteritems("players", "plr")
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

    for (guid, plyr) in l:
        avgs += [(plyr.getName(), plyr.getBatterStats().getBattingAvg())]
        HRs += [(plyr.getName(), plyr.getBatterStats().getHRs())]
        LngstHRs += [(plyr.getName(), plyr.getBatterStats().getLngstHR())]
        RBIs += [(plyr.getName(), plyr.getBatterStats().getRBIs())]
        slg += [(plyr.getName(), plyr.getBatterStats().getSluggingPct())]
        obp += [(plyr.getName(), plyr.getBatterStats().getOnBasePct())]
        hitStreak += [(plyr.getName(), plyr.getBatterStats().getLngstHitStreak())]
        runs += [(plyr.getName(), plyr.getBatterStats().getRuns())]
        #gamesPlayed += [(plyr.getName(), plyr.getBatterStats().getGamesPlayed())]
        wins += [(plyr.getName(), plyr.getBatterStats().getWins())]
        winPct += [(plyr.getName(), plyr.getBatterStats().getWinPct(), 
                    "%s - %s" % (str(plyr.getBatterStats().getWins()),str(plyr.getBatterStats().getLosses())) )]

        
    avgs.sort(cmp)
    HRs.sort(cmp)
    LngstHRs.sort(cmp)
    RBIs.sort(cmp)
    slg.sort(cmp)
    obp.sort(cmp)
    hitStreak.sort(cmp)
    runs.sort(cmp)
    wins.sort(cmp)
    winPct.sort(cmp)
    
    printll('AVG',avgs)
    printll('HRs', HRs)
    printll('Longest HRs', LngstHRs)
    printll('RBIs', RBIs)
    printll('SLG', slg)
    printll('OBP', obp)
    printll('Lngst Hit Streak', hitStreak)
    printll('Runs', runs)
    printll('Wins', wins)
    printll('Winning Pct', winPct)

    return

if __name__ == "__main__":
    main()
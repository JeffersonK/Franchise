import ObjectDB
from pprint import *

def main():

    gsPlayerDB = ObjectDB.ObjectDB("players","plr")
    l = gsPlayerDB.iteritems("players", "plr")
    x = []
    for (guid, plyr) in l:
        x += [(guid, plyr.getBatterStats().getBattingAvg())]

    def cmp(x,y):
        if x[1] < y[1]:
            return 1
        elif x[1] == y[1]:
            return 0
        else:
            return -1

    x.sort(cmp)
    pprint(x)

if __name__ == "__main__":
    main()

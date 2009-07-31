
import ObjectDB

gsPlayerDB = None

def initPlayerDB():
    #global gsPlayerDB
    gsPlayerDB = ObjectDB.ObjectDB("players", "plr")



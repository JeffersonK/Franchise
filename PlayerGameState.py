from Globals import *
from PlayerStats import *

class PlayerGameState:

    def __init__(self, playerGUID, position):
        
        self.__playerGUID = playerGUID
        self.__position = position
        self.__playerGameStats = None
        if position == gsPOSITION_POSSTR[gsPITCHER_POSCODE]:
            self.__playerGameStats = PitcherStats(gsSTATSUBTYPE_ENDGAMESTATS)            
        else:
            self.__playerGameStats = BatterStats(gsSTATSUBTYPE_ENDGAMESTATS)

        return

    def __str__(self):
        s = "PlayerGameState Object(%d):" % id(self)
        s += self.__getstate__()
        return s

    def __getstate__(self):
        s = "{'playerGUID':%d," +\
            "'position':%s," +\
            "'playerGameStats':%s}"
    
        return s % (self.__playerGUID, 
                    self.__position, 
                    str(self.__playerGameStats))



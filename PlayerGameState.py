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
            #so that it gets added at the end of the game
            self.__playerGameStats.setGamesPlayed(1)
        
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

    def getPlayerGameStateStats(self):
        return self.__playerGameStats
 
    def updatePlayerGameState(self, atBatEvent, isBatter):
        
        if isBatter:
            self.__playerGameStats += atBatEvent.getBatterStats()
        else:
            self.__playerGameStats += atBatEvent.getPitcherStats()

    def incWins(self):
        self.__playerGameStats.incWins()

    def incLosses(self):
        self.__playerGameStats.incLosses()

    def incPitcherStarts(self):
        self.__playerGameStats.incStarts()

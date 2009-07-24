import PlayerGameState
from Globals import *
########
#
#
########
class TeamGameState:
    
    def __init__(self, franchise):

        self.__franchiseGUID = franchise.guid()

        #last pitcher in this list is the current pitcher
        #list of tuples (number of outs, pitcher object)
        self.__pitchers = [] 

        self.__nextBatterIndex = 0
        self.__playerStates = {}
        self.__lineup = []

        self.__runs = 0
              
        nextPitcherGUID = franchise.nextPitcherInRotation()
        self.__pitchers = [(0, nextPitcherGUID)] #list of pitchers who pitched in the game (!!!Not sure what the tuple is for!!!)

        self.__lineup = franchise.getLineup()

        for (playerGUID, pos) in self.__lineup:
            self.__playerStates[playerGUID] = PlayerGameState.PlayerGameState(playerGUID, pos)
            
        self.__playerStates[self.__pitchers[0][1]] = PlayerGameState.PlayerGameState(self.__pitchers[0][1], gsPOSITION_POSSTR[gsPITCHER_POSCODE])

    def __str__(self):
        s = "TeamGameState Object(%s):" % id(self)
        s += self.__getstate__()

    def __getstate__(self):
        s = "{'franchiseGUID':%d," +\
            "'nextBatterIndex':%d," +\
            "'playerStates':%s," +\
            "'pitchers':%s," +\
            "'lineup':%s," +\
            "'runs':%s}"

        return s % (self.__franchiseGUID, self.__nextBatterIndex,
                    str(self.__playerStates), str(self.__pitchers),                    
                    str(self.__lineup), self.__runs)
                    
                    
    def incRunsScored(self, n=1):
        self.__runs += n
        return self.__runs

    def getRunsScored(self):
        return self.__runs

    def getPlayerGameStates(self):
        return self.__playerStates

    def updateTeamGameState(self, atBatEvent, isBatter):
        #will update team stats and find appropriate playerGameState 
        #and call its update function
        
        if isBatter:
            playerGUID = atBatEvent.getBatterGUID()
        else:
            playerGUID = atBatEvent.getPitcherGUID()

            
        if playerGUID not in self.__playerStates:
            print "!!!!!!!!!!!! shit is whack !!!!!!!!!!!!!!!"
            return -1
        
        #print "playerGUID:%d isBatter:%s" % (playerGUID, isBatter)
        playerObj = self.__playerStates[playerGUID]

        playerObj.updatePlayerGameState(atBatEvent, isBatter)
        return 0

    #FOR DEBUGGING
    #def printPlayerGameState(self, playerGUID):
    #    print self.__playerStates[playerGUID]

    def getCurrentPitcherGUID(self):
        return self.__pitchers[-1][1]

    def getNextBatterGUID(self):
        return self.__lineup[self.__nextBatterIndex][0] #lineup is tuples (guid, pos)

    def advanceBattingLineup(self):
        self.__nextBatterIndex = (self.__nextBatterIndex + 1) % len(self.__lineup)
        

import PlayerGameState

########
#
#
########
class TeamGameState:
    
    def __init__(self, franchise):
        #last pitcher in this list is the current pitcher
        #list of tuples (number of outs, pitcher object)
        self.__franchiseGUID = franchise#franchise.getFranchiseGUID()

        self.__pitchers = [] 

        self.__nextBatterIndex = 0
        self.__playerStates = {}
        self.__lineup = []

        self.__runs = 0
        self.__hits = 0
              
        nextPitcher = franchise.nextPitcherInRotation()
        self.__pitchers = [(0, nextPitcher)]

        for playerGUID in franchise.getPlayerGUIDs():
            self.__playerStates[playerGUID] = PlayerGameState.PlayerGameState(playerGUID)
            
        self.__lineup = franchise.getLineup()

    def __str__(self):
        s = ""
        return s

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
        
        print "TODO: update TeamGameStats"
        if isBatter:
            playerGUID = atBatEvent.getBatterGUID()
        else:
            playerGUID = atBatEvent.getPitcherGUID()

        if playerGUID not in self.__playerStates:
            print "shit is whack"
            return -1
        
        playerObj = self.__playerStates[playerGUID]
        playerObj.updatePlayerGameState(atBatEvent, isBatter)

        return 0

    #FOR DEBUGGING
    def printPlayerGameState(self, playerGUID):
        print self.__playerStates[playerGUID]

    
    def getCurrentPitcherGUID(self):
        return self.__pitchers[-1][1]

    def getNextBatterGUID(self):
        return self.__lineup[self.__nextBatterIndex]

    def advanceBattingLineup(self):
        self.__nextBatterIndex = (self.__nextBatterIndex + 1) % len(self.__lineup)
        

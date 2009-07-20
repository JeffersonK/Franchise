import random
#from Globals import *
import Globals
import Player
#import PlayerDB
#from Player import *

class FranchiseDB:
    def __init__(self):
        return

    def addFranchise(self, franchise):
        if franchise == None:
            return

        self.__franchises.append(franchise)
        return

class Franchise:
    

    def __init__(self, owner, teamName, franchiseGUID):
         #General Info
        self.__franchiseGUID = franchiseGUID
        self.__owner = owner
        self.__teamName = teamName
 
        self.__stadium = None 
        self.__farmTeam = None
        self.__trainingFacility = None

        #Financials
        self.__salaryCap = 0

        #Team
        self.__players = {}
        self.__lineup = []
        self.__rotation = []

        #Record
        self.__wins = 0
        self.__losses = 0

        return
    
    def guid(self):
        return self.__franchiseGUID

    def addPlayers(self, playerDict):
        self.__players.update(playerDict)
        return 0
    
    def setLineup(self, playerGUIDList=None):
        if playerGUIDList == None:
            if self.__players == None:
                return -1
            elif len(self.__players) >= Globals.gsBATTING_LINEUP_LENGTH:
                self.__lineup = self.__players.keys()[0:Globals.gsBATTING_LINEUP_LENGTH]
                return 0
            else:
                print "Lineup has less than %d players" % Globals.gsBATTING_LINEUP_LENGTH
                return -1

        if len(playerGUIDList) != Globals.gsBATTINGLINEUPLENGTH:
            return -1

        #make sure the players in the lineup are on the team
        for player in playerGUIDList:
            if player not in self.__players:
                return -1

        self.__lineup = playerGUIDList
        return 

    def getLineup(self):
        return self.__lineup

    def setRotation(self, playerGUIDList=None):
        if playerGUIDList == None:
            pitchers = self.getPosGUIDs('P')
            if len(pitchers) == 0:
                return -1

            self.__rotation = pitchers
            return 0

        for player in playerGUIDList:
            if player not in self.__players:
                return -1

        self.__rotation = playerGUIDList
        return 0

    def getPosGUIDs(self, position):
        playerGUIDList = []
        for (playerGUID,pos) in self.__players.items():
            if pos == position:
                playerGUIDList += [playerGUID]

        return playerGUIDList

    def getPlayerGUIDs(self):
        return self.__players.keys()

    def nextPitcherInRotation(self):
        return self.__rotation[0]

    def __str__(self):
        s = "Owner: " + self.__owner + "\n"
        s += "Team Name: " + self.__teamName + "\n"

        s += "Players: \n" 
        for p in self.__players:
            s += "\t" + p.__str__() + "\n"

        s += "Lineup: \n" 
        for p in self.__lineup:
            s += "\t" + str(p) + "\n"

        s += "Rotation: \n" 
        for p in self.__rotation:
            s += "\t" + str(p) + "\n"

        return s

    def __getstate__(self):
        fmt = "{'owner':'%s','teamName':'%s','franchiseGUID':%d," + \
            "'players':%s,'lineup':%s,'rotation':%s,'wins':%d,'losses':%d}"
        
        return fmt % (self.__owner, self.__teamName, self.__franchiseGUID,
                      str(self.__players), str(self.__lineup), str(self.__rotation),
                      self.__wins, self.__losses)

    def __setstate__(self, dictStr):
        
        print "TODO: check for eval errors!!!"
        d = eval(dictStr)
        self.__owner = d['owner']
        self.__teamName = d['teamName']
        self.__franchiseGUID = d['franchiseGUID']

        #TODO: check for errors loading this !!!        
        self.__players = d['players']#eval(d['players'])
        self.__lineup = d['lineup']#eval(d['lineup'])
        self.__rotation = d['rotation']#eval(d['rotation'])

        self.__wins = d['wins']
        self.__losses = d['losses']
    

    #def teamName(self):
    #    return self.__teamName

    #def owner(self):
    #    return self.__owner

    #update franchise specific stats
    #return events
    def updateFranchiseStats(self, franchiseGameState, isWin):

        updateFranchiseStatsEvents = []

        if isWin:
            self.__wins += 1
            updateFranchiseStatsEvents += ['Win']
        else:
            self.__losses += 1
            updateFranchiseStatsEvents += ['Loss']

        return updateFranchiseStatsEvents

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
            self.__playerStates[playerGUID] = Player.PlayerGameState(playerGUID)
            
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
        
#import pickle
def main():
    f1 = Franchise("frza", "frzaites", globalState.nextFranchiseGUID())
    #f1.create("frza", "frzaites")
    #print f1
    
    #f2 = Franchise()
    #f2.create("jza", "jzites")
    #print f2

    #sim = GameRunner(f1, f2)
    #sim.run(-1)

    #pickle.dump(f1, "f1.txt")
    
if __name__ == "__main__":
    main()

import random
from Globals import *
from Player import *

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
    
    def getFranchiseGUID(self):
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

    def teamName(self):
        return self.__teamName

    def owner(self):
        return self.__owner


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

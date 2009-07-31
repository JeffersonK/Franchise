import Globals
import cPickle
import PlayerAbilities
from PlayerStats import *

class Player:

    def __init__(self, playerGUID):#, type):

        #Book Keeping
        self.__playerGUID = playerGUID

        #TODO: change this to an integer
        #self.__position = position.upper()
        
        self.__franchiseGUID = Globals.gsPLAYERFREEAGENT
        #self.__franchiseGUIDHistory = [(franchiseGUID, datefrom, dateto)]
        
        self.__playerAbilities = PlayerAbilities.PlayerAbilities()

        self.__pitcherStats = PitcherStats(gsSTATSUBTYPE_ENDGAMESTATS)
        self.__batterStats = BatterStats(gsSTATSUBTYPE_ENDGAMESTATS)

        #Player Personality/Character
        self.__name = "Player%d" % playerGUID
        self.__experiencePoints = 0
        self.__energy = gsPLAYERENERGY_MAXINITIAL
        self.__maxPlayerEnergy = gsPLAYERENERGY_MAXINITIAL
        self.__level = 0
        #self.__items = PlayerItems()
        #self.__achievements = PlayerAchievements()


        return

    def __getstate__(self):
        fmt =  "{'playerGUID':%d,'name':'%s'," +\
            "'maxPlayerEnergy':%d,'energy':%d," +\
            "'experiencePoints':%d,'level':%d," +\
            "'position':'%s','franchiseGUID':%d," +\
            "'playerAbilities':%s,'batterStats':%s,'pitcherStats':%s}"

        return fmt % (self.__playerGUID, self.__name,
                      self.__maxPlayerEnergy, self.__energy,
                      self.__experiencePoints,self.__level, 
                      self.__position, self.__franchiseGUID,
                      self.__playerAbilities.__getstate__(),
                      self.__batterStats.__getstate__(), self.__pitcherStats.__getstate__())



    def __setstate__(self, dictstr):

        print "TODO: check for eval errors!!!"
        d = eval(dictstr)

        self.__franchiseGUID = d['franchiseGUID']

        self.__playerGUID = d['playerGUID']

        self.__position = d['position']
        
        #player
        self.__level = d['level']
        self.__energy = d['energy']
        self.__maxPlayerEnergy = d['maxPlayerEnergy']
        self.__name = d['name']
        #self.__lastName = d['lastName']
        self.__experiencePoints = d['experiencePoints']
        

        abilities = d['playerAbilities']
        self.__playerAbilities = PlayerAbilities.PlayerAbilities(abilities['batting'],
                                                                 abilities['pitching'],
                                                                 abilities['running'],
                                                                 abilities['fielding'],
                                                                 abilities['character'])

        batterStatsStr = d['batterStats']
        self.__batterStats = BatterStats(gsSTATSUBTYPE_ENDGAMESTATS).__setstate__(batterStatsStr)
        
        pitcherStatsStr = d['pitcherStats']
        self.__pitcherStats = PitcherStats(gsSTATSUBTYPE_ENDGAMESTATS).__setstate__(pitcherStatsStr)


    def __str__(self):
        return self.__getstate__()
    
        #return "PlayerGUID: %d Position:'%s'" % (self.__playerGUID, self.__position)

    #we should generate events when we update stats because
    #it is a change in the player state
    #here is where a player will gain ablities when their stats are updated
    def getPlayerAbilities(self):
        return self.__playerAbilities

    def getName(self):
        return self.__name

    def getBatterStats(self):
        return self.__batterStats

    #
    #
    #
    def updatePlayerStats(self, playerGameState):

        playerGameStats = playerGameState.getPlayerGameStateStats()

        if self.__position == gsPOSITION_POSSTR[gsPITCHER_POSCODE] and \
                playerGameStats.isPitcherStats():

            #TODO: look in the playerGamStats and compare to the existing stats for achievements
            self.__pitcherStats += playerGameStats
            #print self
        elif self.__position != gsPOSITION_POSSTR[gsPITCHER_POSCODE] and \
                playerGameStats.isBatterStats():
            #TODO: look in the playerGamStats and compare to the existing stats for achievements
            self.__batterStats += playerGameStats
            #print self

        updatePlayerStatsEvents = ['+1 EXP']
        return updatePlayerStatsEvents

    def setPosition(self, pos):
        if pos.upper() not in Globals.gsPOSITION_POSSTR.values():
            return -1

        self.__position = pos
        return 0

    def incRunsScored(self):
        self.__batterStats.incRunsScored()

    def getEnergy(self):
        return self.__energy

    def decreaseEnergy(self, numEnergyUnits):
        self.__energy = max(0, self.__energy-numEnergyUnits)

    def increaseEnergy(self, numEnergyUnits):
        self.__energy = min(self.__maxPlayerEnergy, self.__energy + numEnergyUnits)

    def getPosition(self):
        return self.__position

    def guid(self):
        return self.__playerGUID

    def setPlayerFranchise(self, franchiseGUID):
        self.__franchiseGUID = franchiseGUID

    #def generatePlayerEvents(self, state):
    #    return


##########
#
#
#
##########
def testSerialization():
    #guid = Globals.globalState.nextPlayerGUID()
    #playerObj = Player(guid,"P")

    #PlayerDB.gsPlayerDB.addPlayer(guid, playerObj)
    
    #handle = PlayerDB.gsPlayerDB.getPlayerHandle(guid)
    
    #if handle == playerObj:
    #    print "PASS"
    return

def main():
    #testSerialization()
    return
    
if __name__ == "__main__":
    main()

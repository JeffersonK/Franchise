import Globals
import cPickle
import PlayerAbilities
from PlayerStats import *

class Player:

    def __init__(self, playerGUID, position):

        #Book Keeping
        self.__playerGUID = playerGUID

        if position.upper() not in Globals.gsPOSITION_POSSTR.values():
            return None
        
        #TODO: change this to an integer
        self.__position = position.upper()
        
        self.__franchiseGUID = Globals.gsPLAYERFREEAGENT
        #self.__franchiseGUIDHistory = [(franchiseGUID, datefrom, dateto)]
        
        self.__playerAbilities = PlayerAbilities.PlayerAbilities()

        self.__pitcherStats = PitcherStats(gsSTATSUBTYPE_ENDGAMESTATS)
        self.__batterStats = BatterStats(gsSTATSUBTYPE_ENDGAMESTATS)

        #Player Personality/Character
        self.__firstName = "Moonbeam"
        self.__lastName = "McFly"
        self.__experiencePoints = 0
        self.__level = 0
        #__playerHomeTown =
    
        #expereince
        #age
        #gamesPlayed
        #self.__games = 0

        #Pitcher Stats
        #self.__totBattersFaced = 0
        #self.__totKs = 0
        #self.__totWalksThrown = 0
        #self.__totOutsPitched = 0
        #self.__totEarnedRuns = 0
        #self.__totStrikesThrown = 0
        #self.__totPitchesThrown = 0
        #self.__totHitsAllowed = 0
        #self.__totHRAllowed = 0

        #self.__wins = 0
        #self.__losses = 0
        #self.__starts = 0
            
        #Batting stats
        #self.__totAtBats = 0
        #self.__totHits = 0
        #self.__tot1Bs = 0
        #self.__tot2Bs = 0
        #self.__tot3Bs = 0
        #self.__totHRs = 0
        #self.__totRBIs = 0
        #self.__totRuns = 0
        #self.__timesKd = 0
        #self.__totWalks = 0
        #self.__cyclesHit = 0
        #self.__grandSlams = 0

        return

    def __getstate__(self):
        fmt =  "{'playerGUID':%d,'firstName':'%s','lastName':'%s','experiencePoints':%d,'level':%d," +\
            "'position':'%s','franchiseGUID':%d," +\
            "'playerAbilities':%s,'batterStats':%s,'pitcherStats':%s}"
#'totKs':%d," + \
            #"'totWalksThrown':%d,'totOutsPitched':%d,'totEarnedRuns':%d," + \
            #"'wins':%d,'losses':%d,'starts':%d," +\
            #"'totAtBats':%d,'totHits':%d,'tot1Bs':%d,'tot2Bs':%d," + \
            #"'tot3Bs':%d,'totHR':%d,'totWalks':%d,'grandSlams':%d,'cyclesHit':%d,'games':%d," +\
            #"'totRBIs':%d,'totRuns':%d,'timesKd':%d," +\


        return fmt % (self.__playerGUID, self.__firstName, self.__lastName, 
                      self.__experiencePoints,self.__level,
                      self.__position, self.__franchiseGUID,
                      #self.__totKs, self.__totWalksThrown, self.__totOutsPitched,
                      #self.__totEarnedRuns, self.__wins, self.__losses, self.__starts,
                      #self.__totAtBats, self.__totHits, 
                      #self.__tot1Bs, self.__tot2Bs, self.__tot3Bs, self.__totHRs,
                      #self.__totWalks, self.__grandSlams, self.__cyclesHit, self.__games,
                      #self.__totRBIs, self.__totRuns, self.__timesKd, 
                      self.__playerAbilities.__getstate__(),
                      self.__batterStats.__getstate__(), self.__pitcherStats.__getstate__())



    def __setstate__(self, dictstr):

        print "TODO: check for eval errors!!!"

        d = eval(dictstr)
        self.__playerGUID = d['playerGUID']
        self.__franchiseGUID = d['franchiseGUID']
        self.__position = d['position']
        
        #self.__totKs = d['totKs']
        #self.__totWalksThrown = d['totWalksThrown']
        #self.__totOutsPitched = d['totOutsPitched']
        #self.__totEarnedRuns = d['totEarnedRuns']
        #self.__wins = d['wins']
        #self.__losses = d['losses']
        #self.__starts = d['starts']

        #batting stats
        #self.__totAtBats = d['totAtBats']
        #self.__totHits = d['totHits']
        #self.__tot1Bs = d['tot1Bs']
        #self.__tot2Bs = d['tot2Bs']
        #self.__tot3Bs = d['tot3Bs']
        #self.__totHRs = d['totHR']
        #self.__totWalks = d['totWalks']
        #self.__grandSlams = d['grandSlams']
        #self.__cyclesHit = d['cyclesHit']
        #self.__games = d['games']

        #self.__totRBIs = d['totRBIs']
        #self.__totRuns = d['totRuns']
        #self.__timesKd = d['timesKd']

        #player abilities
        self.__level = d['level']
        self.__firstName = d['firstName']
        self.__lastName = d['lastName']
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

    def updatePlayerStats(self, playerGameState):

        playerGameStats = playerGameState.getPlayerGameStateStats()

        if self.__position == gsPOSITION_POSSTR[gsPITCHER_POSCODE] and \
                playerGameStats.isPitcherStats():

            #TODO: look in the playerGamStats and compare to the existing stats for achievements
            self.__pitcherStats += playerGameStats
            print self.__pitcherStats
        elif self.__position != gsPOSITION_POSSTR[gsPITCHER_POSCODE] and \
                playerGameStats.isBatterStats():
            #TODO: look in the playerGamStats and compare to the existing stats for achievements
            self.__batterStats += playerGameStats
            print self.__batterStats

        updatePlayerStatsEvents = ['+1 EXP']
        return updatePlayerStatsEvents

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


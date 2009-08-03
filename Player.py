import Globals
import cPickle
import PlayerAbilities
from PlayerStats import *
import time
from Levels import *
from PlayerSkills import *

class Player:

    def __init__(self, playerGUID):
        #Book Keeping
        self.__playerGUID = playerGUID
        #self.__position = position.upper()
        self.__position = ''
        #self.__handedness
        self.__franchiseGUID = gsPLAYERFREEAGENT
        self.__playerAbilities = PlayerAbilities.PlayerAbilities()
        self.__pitcherSkills = PitcherPlayerSkills()
        self.__batterSkills = BatterPlayerSkills()
        self.__pitcherStats = PitcherStats(gsSTATSUBTYPE_ENDGAMESTATS)
        self.__batterStats = BatterStats(gsSTATSUBTYPE_ENDGAMESTATS)
        #Player Personality/Character
        self.__name = "Player%d" % playerGUID
        self.__XP = 0
        self.__energy = gsPLAYERENERGY_MAXINITIAL
        self.__level = 1
        self.__lastPlayerRecharge = getTime()
        self.__money = gsINITIAL_MONEY_ALLOC
        self.__lastTimePaid = getTime()
        self.__unusedStatPoints = gsINITIAL_STATPOINT_ALLOC
        self.__maxChallengePoints = gsPLAYERCHALLENGE_MAXINITIAL#maximumNumber of games that can be played per unit time
        self.__challengePoints = gsPLAYERCHALLENGE_MAXINITIAL
        self.__maxPlayerEnergy = gsPLAYERENERGY_MAXINITIAL#determines how much training/jobs can be done/unit time
        self.__recoveryTime = gsPLAYERRECOVERYTIME_INITIAL#seconds until energy/challenge points are regained
        #self.__items = PlayerItems()
        #self.__achievements = PlayerAchievements()
        self.__defaultLineup = []
        self.__defaultRotation = []
        return

    def __getstate__(self):
        fmt =  "{'playerGUID':%d,'name':'%s','energy':%d, 'maxChallengePoints':%d," +\
            "'challengePoints':%d,'maxPlayerEnergy':%d,'recoveryTime':%d," +\
            "'lastPlayerRecharge':%d,'money':%d,'lastTimePaid':%d," +\
            "'XP':%d,'level':%d,'unusedStatPoints':%d," +\
            "'position':'%s','franchiseGUID':%d," +\
            "'%s':%s,'batterStats':%s,'pitcherStats':%s," +\
            "'defaultLineup':%s, 'defaultRotation':%s," +\
            "'%s':%s, '%s':%s}"

        return fmt % (self.__playerGUID, 
                      self.__name, 
                      self.__energy, 
                      self.__maxChallengePoints, 
                      self.__challengePoints, 
                      self.__maxPlayerEnergy, 
                      self.__recoveryTime,
                      self.__lastPlayerRecharge, 
                      self.__money, 
                      self.__lastTimePaid, 
                      self.__XP, 
                      self.__level, 
                      self.__unusedStatPoints,
                      self.__position, 
                      self.__franchiseGUID, 
                      PLAYERABILITIES,
                      self.__playerAbilities.__getstate__(),
                      self.__batterStats.__getstate__(), 
                      self.__pitcherStats.__getstate__(),
                      self.__defaultLineup, 
                      self.__defaultRotation,
                      PLAYERSKILLS_BATTERSKILLS,
                      self.__batterSkills.__getstate__(), 
                      PLAYERSKILLS_PITCHERSKILLS,
                      self.__pitcherSkills.__getstate__())

    def __setstate__(self, dictstr):

        print "TODO: check for eval errors!!!"
        d = None
        try:
            d = eval(dictstr)
        except:
            print "could not load player object file corrupt."
            return

        self.__franchiseGUID = d['franchiseGUID']
        self.__playerGUID = d['playerGUID']
        self.__position = d['position']
        
        #player
        self.__level = d['level']
        self.__energy = d['energy']
        self.__challengePoints = 10
        self.__name = d['name']
        self.__XP = d['XP']
        self.__maxChallengePoints = d['maxChallengePoints']
        self.__challengePoints = d['challengePoints']
        self.__maxPlayerEnergy = d['maxPlayerEnergy']
        self.__recoveryTime = d['recoveryTime']
        self.__lastPlayerRecharge = d['lastPlayerRecharge']
        self.__money = d['money']
        self.__lastTimePaid = d['lastTimePaid']
        self.__unusedStatPoints = d['unusedStatPoints']
        #self.__achievements = {}
        #self.__items = {}
        self.__defaultLineup = d['defaultLineup']
        self.__defaultRotation = d['defaultRotation']
        abilities = d[PLAYERABILITIES]
        self.__playerAbilities = PlayerAbilities.PlayerAbilities(abilities[PLAYERABILITIES_BATTING],
                                                                 abilities[PLAYERABILITIES_PITCHING],
                                                                 abilities['running'],
                                                                 abilities[PLAYERABILITIES_FIELDING],
                                                                 abilities[PLAYERABILITIES_CHARACTER])
        batterStatsStr = d['batterStats']
        self.__batterStats = BatterStats(gsSTATSUBTYPE_ENDGAMESTATS).__setstate__(batterStatsStr)
        pitcherStatsStr = d['pitcherStats']
        self.__pitcherStats = PitcherStats(gsSTATSUBTYPE_ENDGAMESTATS).__setstate__(pitcherStatsStr)
        self.__batterSkills = BatterPlayerSkills().__setstate__(d[PLAYERSKILLS_BATTERSKILLS])
        self.__pitcherSkills = PitcherPlayerSkills().__setstate__(d[PLAYERSKILLS_PITCHERSKILLS])
        return self

    def __str__(self):
        return self.__getstate__()
    
        #return "PlayerGUID: %d Position:'%s'" % (self.__playerGUID, self.__position)

    #we should generate events when we update stats because
    #it is a change in the player state
    #here is where a player will gain ablities when their stats are updated
    def getPlayerAbilities(self):
        return self.__playerAbilities

    def getPlayerBatterSkills(self):
        return self.__batterSkills

    def getPlayerPitcherSkills(self):
        return self.__pitcherSkills

    def getBatterStats(self):
        return self.__batterStats

    def getPitcherStats(self):
        return self.__pitcherStats

    #
    #
    #
    def updatePlayerStats(self, playerGameState):

        playerGameStats = playerGameState.getPlayerGameStateStats()
        moneyInc = self.__playerAbilities.getPrestige()*Globals.gsLEVEL_CASH_PERPRESTIGE_PERGAME

        if self.__position == gsPOSITION_POSSTR[gsPITCHER_POSCODE] and \
                playerGameStats.isPitcherStats():

            self.__XP += playerGameState.countXP()
            #TODO: look in the playerGamStats and compare 
            #to the existing stats for achievements
            self.__pitcherStats += playerGameStats
            #print self
            self._checkLevelUp()
            #print playerGameState.getPitcherScore()

            #increment money
            if playerGameStats.getWins() > 0:
               
                self.__money += moneyInc
            else:
                self.__money += int(0.5*moneyInc)

        elif self.__position != gsPOSITION_POSSTR[gsPITCHER_POSCODE] and \
                playerGameStats.isBatterStats():
            
            #count here because they are end game stats
            self.__XP += playerGameState.countXP()
            #TODO: look in the playerGamStats and compare to the existing stats for achievements
            self.__batterStats += playerGameStats
            self._checkLevelUp()
            #print self

            #increment money
            if playerGameStats.getWins() > 0:   
                self.__money += moneyInc
            else:
                self.__money += int(0.5*moneyInc)

        #updatePlayerStatsEvents = ['+1 EXP']
        return #updatePlayerStatsEvents

    def incRunsScored(self):
        self.__batterStats.incRunsScored()

    def getName(self):
        return self.__name

    def setName(self, name):
        if type(name) != type(''):
            return -1

        self.__name = name
        return 0

    def _handleLevelUp(self):
        self.__level += 1
        self.__unusedStatPoints += gsLEVEL_STATPOINTS_PERLVL
        self.__energy = self.__maxPlayerEnergy
        self.__challengePoints = self.__maxChallengePoints
        #print "%s PLAYER LEVEL UP %d => %d" % (self.getName(), self.__level-1, self.__level)

    def _checkLevelUp(self):
        if self.__XP > gsXP_LEVELS[self.__level]:
            self._handleLevelUp()

    def getNextLevelExperience(self):
        return gsXP_LEVELS[self.__level]

    def getExperience(self):
        return self.__XP

    def setExperience(self, XP):
        val = safeConvertToInt(XP)
        if val == None:
            return -1
        if val < 0:
            return -2
        self.__XP = XP
        return 0

    def getMoney(self):
        return self.__money

    def decreaseMoney(self, num):
        self.__money -= num

    def getUnusedStatPoints(self):
        return self.__unusedStatPoints
    
    def incStatPoint(self, abilityName):
        if self.__unusedStatPoints == 0:
            return -1

        if abilityName == PLAYERABILITY_MAXENERGYPOINTS:
            self.__maxPlayerEnergy += 1
        elif abilityName == PLAYERABILITY_MAXCHALLENGEPOINTS:
            self.__maxChallengePoints += 1
        elif abilityName == PLAYERABILITY_DEFENSE:
            self.__playerAbilities.incDefense()
        elif abilityName == PLAYERABILITY_PRESTIGE:
            self.__playerAbilities.incPrestige()
        elif abilityName  == PLAYERABILITY_LEADERSHIP:
            self.__playerAbilities.incLeadership()

        elif abilityName == PLAYERABILITY_BATTER_POWER: 
            self.__playerAbilities.incBatterPower()
        elif abilityName == PLAYERABILITY_BATTER_PATIENCE:
            self.__playerAbilities.incBatterPatience()
        elif abilityName == PLAYERABILITY_PITCHER_CONTROL:
            self.__playerAbilities.incPitcherControl()
        elif abilityName == PLAYERABILITY_PITCHER_STAMINA:
            self.__playerAbilities.incPitcherStamina()
        else:
            "Print Uknown Ability %s" % abilityName
            return -2

        self.__unusedStatPoints -= 1            
        return 0

    def getTrainingOptions(self):
        trainingDB = ObjectDB("trainingdb", "trn")
        trainingJobs = []
        for (guid, trainingJob) in trainingDB.iteritems():
            if self.__position == gsPOSITION_POSSTR[gsPITCHER_POSCODE]:
                if trainingJob.getSkillType() in PITCHERSKILLS: 
                    trainingJobs += [trainingJob.__getstate__()]
            else:
                if trainingJob.getSkillType() in BATTERSKILLS:
                    trainingJobs += [trainingJob.__getstate__()]

        del(trainingDB)
        trainingDB = None
        return trainingJobs

    def train(self, trainingGUID):
        trainingDB = ObjectDB("trainingdb", "trn")
        trainObj = trainingDB.getObjectHandle(trainingGUID)
        (energy, money) = trainObj.cost()
        if self.__energy < energy:
            del trainingDB
            trainObj = None
            return -1

        if self.__money < money:
            del trainingDB
            trainObj = None
            return -2
        
        skillTrained = trainObj.getSkillType()
        if skillTrained in BATTERSKILLS:
            self.__batterSkills.trainSkills(trainObj)
        else:
            self.__pitcherSkills.trainSkills(trainObj)

        self.decreaseEnergy(energy)
        self.decreaseMoney(money)
        del trainingDB
        trainObj = None
        return 0
        
    def getLevel(self):
        return self.__level

    def getChallengePoints(self):
        return self.__challengePoints

    def getMaxChallengePoints(self):
        return self.__maxChallengePoints

    def getEnergy(self):
        return self.__energy

    def decreaseEnergy(self, numEnergyUnits):
        self.__energy = max(0, self.__energy-numEnergyUnits)

    def increaseEnergy(self, numEnergyUnits):
        self.__energy = min(self.__maxPlayerEnergy, self.__energy + numEnergyUnits)

    def getMaxEnergy(self):
        return self.__maxPlayerEnergy

    def getPosition(self):
        return self.__position

    def setPosition(self, pos):
        if type(pos) != type(''):
            return -1

        if pos.upper() not in Globals.gsPOSITION_POSSTR.values():
            return -1

        self.__position = pos
        return 0

    def guid(self):
        return self.__playerGUID

    def setPlayerFranchise(self, franchiseGUID):
        f = -1
        try:
            f = int(franchiseGUID)
        except:
            return -1
        if f < 0:
            return -1

        self.__franchiseGUID = franchiseGUID
        return 0
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


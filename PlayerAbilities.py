from Globals import *
from ProbabilityEngine import *

OLD = """
#Chi => Zone
#mu => pitch

######
#
# Chi2
######
gsChi2Normal = 1.0
gsChi2PrimeMin = 0.01768 #90%
gsChi2PrimeMax = 3.862 #10% Chi2Normal - Chi2PrimMin
#0.0324 #50% Chi2Normal - Chi2PrimMin


gsChi2BatterMax = gsChi2Normal - gsChi2PrimeMin #0.982
gsChi2PitcherMax = gsChi2PrimeMax - gsChi2Normal

gsChi2BatterMin = 0.0
gsChi2PitcherMin = 0.0

Chi2b0 = gsChi2BatterMin#gsChi2BatterMin #+ .25
Chi2p0 = gsChi2PitcherMin #+ 2.862

gsPITCHERCHI2FIXED = 1.0
gsBATTERMUFIXED = 0.0

######
#
# Mu
######

gsMuPrimeMax = 3.65# 1%

gsMuBatterMin = 0.0
gsMuPitcherMin = 0.0# 28%

gsMuBatterMax = gsMuPrimeMax
gsMuPitcherMax = gsMuPrimeMax"""

Chi2b0 = 0.0
Chi2p0 = 0.0

minPower = 1
batterPowerZones = [minPower, minPower, minPower,
                    minPower, minPower, minPower,
                    minPower, minPower, minPower]
                    

batterZoneMastery = [Chi2b0, Chi2b0, Chi2b0,
                     Chi2b0, Chi2b0, Chi2b0,
                     Chi2b0, Chi2b0, Chi2b0]


pitcherZoneMastery = [Chi2p0, Chi2p0, Chi2p0,
                      Chi2p0, Chi2p0, Chi2p0,
                      Chi2p0, Chi2p0, Chi2p0]


batterPitchMastery = {}
pitcherPitchMastery = {}
for pitchType in gsPITCHTYPES:
    batterPitchMastery[pitchType] = Chi2b0
    pitcherPitchMastery[pitchType] = Chi2p0

gsMAX_PITCHMASTERY_LEVEL = gsNUM_PITCHMASTERY_LEVELS
gsMIN_PITCHMASTERY_LEVEL = 0
gsMAX_ZONEMASTERY_LEVEL = gsNUM_ZONEMASTERY_LEVELS
gsMIN_ZONEMASTERY_LEVEL = 0


#PITCHING
defaultpitcherAbil = {'zoneMastery':pitcherZoneMastery, #pitchers effectiveness at throwing pitches by zone
                      'pitchMastery':pitcherPitchMastery,#how good a pitcher is at throwing various pitches
                      'strength':0,#affects the speed of the pitches thrown
                      'control':0, #affects if a whether a pitch is a ball or not
                      'stamina':0,   #affects how many pitches they can throw before their accuracy and speed are temporarily affected
                      }

#BATTER abilities
defaultbatterAbil = {'zoneMastery':batterZoneMastery,#how good a batter is at making contact with a pitch in a given location
                     'pitchMastery':batterPitchMastery,#how good a batter is at making contact with a certain kind of pitch
                     'powerZones':batterPowerZones, #effects the zones where hitters have power
                     'patience':0, #effects how often the batter chances balls/bad pitches
                     }

#FIELDING
defaultfieldingAbil = {'defense':0, #effects the range/radius of the player on defense
                       }
 
#RUNNING   
defaultrunningAbil = {'speed':0, #effects whether extra bases can be squeezed out on hits
                      }

#CHARACTER
defaultcharacterAbil = {'leadership':0, #makes everyone on the team a little better
                        'prestige':0, #affects how much money the player draws per game and unit time
                        }


class PlayerAbilities:

    def __init__(self, batting=None, pitching=None, running=None, fielding=None, character=None):

        if fielding == None:
            self.__fielding = defaultfieldingAbil
        else:
            self.__fielding = fielding
        if batting == None:
            self.__batting = defaultbatterAbil
        else:
            self.__batting = batting
        if pitching == None:
            self.__pitching = defaultpitcherAbil
        else:
            self.__pitching = pitching
        if running == None:
            self.__running = defaultrunningAbil
        else:
            self.__running = running
        if character == None:
            self.__character = defaultcharacterAbil
        else:
            self.__character = character
        
        return

    def __str__(self):
        return self.__getstate__()

    def __getstate__(self):
        fmt = "{'fielding':%s,'batting':%s,'pitching':%s,'running':%s,'character':%s}"
        return fmt % (str(self.__fielding), 
                      str(self.__batting),
                      str(self.__pitching),
                      str(self.__running),
                      str(self.__character))

    
    def __setstate__(self, dictStr):
        print "TODO: check for eval errors in PlayerAbility __setstate__"
        d = eval(dictStr)
        self.__fielding = d['fielding']
        self.__batting = d['batting']
        self.__pitching = d['pitching']
        self.__running = d['running']
        self.__character = d['character']
        return self

    #PITCHING SPECIFIC
    def getPitchingPitchMasteryMatrix(self):
        return self.__pitching['pitchMastery']

    def getPitchingZoneMasteryMatrix(self):
        return self.__pitching['zoneMastery']

    def setPitchingPitchMasteryMatrix(self, matrix):
        if type(matrix) != type({}):
            return -1
        if len(matrix) == 0 or len(matrix) > len(gsPITCHTYPES):
            return -2
        newMatrix = {}
        for pitchtype,val in matrix.iteritems():
            if pitchtype not in gsPITCHTYPES:
                return -3
            ret = safeConvertToFloat(val)
            if ret == None:
                return -4
            if ret > gsMAX_PITCHMASTERY_LEVEL or\
                    ret < gsMIN_PITCHMASTERY_LEVEL:
                return -5
            newMatrix[pitchtype] = ret
        self.__pitching['pitchMastery'].update(newMatrix)
        return 0

    def setPitchingZoneMasteryMatrix(self, matrix):
        
        if type(matrix) != type([]):
            return -1
        if len(matrix) != len(gsSTRIKEZONE):
            return -2
        newMatrix = []
        for pm in matrix:
            ret = safeConvertToFloat(pm)
            if ret == None:
                return -3
            if ret > gsMAX_ZONEMASTERY_LEVEL or\
                    ret < gsMIN_ZONEMASTERY_LEVEL:
                return -4
            newMatrix += [ret]
        self.__pitching['zoneMastery'] = newMatrix
        return 0
    

    def getPitcherStamina(self):
        return self.__pitching['stamina']

    def getPitcherStrength(self):
        return self.__pitching['strength']

    def getPitcherControl(self):
        return self.__pitching['control']

    #BATTING SPECIFIC
    def getBattingPitchMasteryMatrix(self):
        return self.__batting['pitchMastery']

    def setBattingPitchMasteryMatrix(self, matrix):
        if type(matrix) != type({}):
            return -1
        if len(matrix) == 0 or len(matrix) > len(gsPITCHTYPES):
            return -2
        newMatrix = {}
        for pitchtype,val in matrix.iteritems():
            if pitchtype not in gsPITCHTYPES:
                return -3
            ret = safeConvertToFloat(val)
            if ret == None:
                return -4
            if ret > gsMAX_PITCHMASTERY_LEVEL or\
                    ret < gsMIN_PITCHMASTERY_LEVEL:
                return -5
            newMatrix[pitchtype] = ret
            
        self.__batting['pitchMastery'].update(newMatrix)
        return 0


    def getBattingZoneMasteryMatrix(self):
        return self.__batting['zoneMastery']

    def setBattingZoneMasteryMatrix(self, matrix):
        if type(matrix) != type([]):
            return -1
        if len(matrix) != len(gsSTRIKEZONE):
            return -2
        newMatrix = []
        for pm in matrix:
            ret = safeConvertToFloat(pm)
            if ret == None:
                return -3
            if ret > gsMAX_ZONEMASTERY_LEVEL or\
                    ret < gsMIN_ZONEMASTERY_LEVEL:
                return -4
            newMatrix += [ret]
        self.__batting['zoneMastery'] = newMatrix
        return 0

    def getSpeed(self):
        return self.__running['speed']

    def getDefense(self):
        return self.__fielding['defense']

    def getLeadership(self):
        return self.__character['leadership']

    def setLeadership(self, newVal):
        val = safeConvertToInt(newVal)
        if val == None:
            return -1
        self.__character['leadership'] = val
        return 0

    def getPrestige(self):
        return self.__character['prestige']

    def setPrestige(self, newVal):
        val = safeConvertToInt(newVal)
        if val == None:
            return -1
        self.__character['prestige'] = val
        return 0

    def getPatience(self):
        return self.__batting['patience']

    def setPatience(self, newVal):
        val = safeConvertToInt(newVal)
        if val == None:
            return -1
        self.__batting['patience'] = val
        return 0

def main():

    pa = PlayerAbilities()
    print pa

    print pa.getBattingZoneMasteryMatrix()
    print pa.setBattingZoneMasteryMatrix(['2.1']*9)
    print pa.getBattingZoneMasteryMatrix()

    print pa.getPitchingZoneMasteryMatrix()
    print pa.setPitchingZoneMasteryMatrix(['2.1']*9)
    print pa.getPitchingZoneMasteryMatrix()
    
    pitchMastery = {}
    for pitchType in gsPITCHTYPES:
        pitchMastery[pitchType] = '2'
        
    print pa.getBattingPitchMasteryMatrix()
    print pa.setBattingPitchMasteryMatrix(pitchMastery)
    print pa.getBattingPitchMasteryMatrix()

    print pa.getPitchingPitchMasteryMatrix()
    print pa.setPitchingPitchMasteryMatrix(pitchMastery)
    print pa.getPitchingPitchMasteryMatrix()

    return
if __name__ == "__main__":
    main()

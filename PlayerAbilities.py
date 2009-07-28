from Globals import *

#Chi => Zone
#mu => pitch

######
#
# Chi2
######
gsChi2Normal = 1.0
gsChi2PrimeMin = 0.018
gsChi2PrimeMax = 3.862#Chi2Normal - Chi2PrimMin

gsChi2BatterMax = gsChi2Normal - gsChi2PrimeMin #0.982
gsChi2PitcherMax = gsChi2PrimeMax - gsChi2Normal

gsChi2BatterMin = 0.0
gsChi2PitcherMin = 0.0

Chi2b0 = gsChi2BatterMin #+ .25
Chi2p0 = gsChi2PitcherMin #+ 2.862

gsPITCHERCHI2FIXED = 1.0
gsBATTERMUFIXED = 0.0

######
#
# Mu
######


gsMuPrimeMax = 3.65

gsMuBatterMin = 0.0
gsMuPitcherMin = 0.0#2.5

gsMuBatterMax = gsMuPrimeMax
gsMuPitcherMax = gsMuPrimeMax

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
    batterPitchMastery[pitchType] = gsMuBatterMin
    pitcherPitchMastery[pitchType] = gsMuPitcherMin

#{'curveball':gsMuBatterMin, 
#                      'fastball':gsMuBatterMin,
#                       'slider':gsMuBatterMin,
#                       'changeup':gsMuBatterMin,
#                       'knuckleball':gsMuBatterMin}

#pitcherPitchMastery = {'curveball':gsMuPitcherMin, 
#                       'fastball':gsMuPitcherMin,
#                       'slider':gsMuPitcherMin,
#                      'changeup':gsMuPitcherMin,
#                       'knuckleball':gsMuPitcherMin}




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
                        'prestige':0, #affects how much money the player draws per game
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
        return


    #PITCHING SPECIFIC
    def getPitchingPitchMasteryMatrix(self):
        return self.__pitching['pitchMastery']

    #def _getPitchingPitchMastery(self, pitchtype):
    #    return self.__pitching['pitchMastery']

    def _setPitchingPitchMastery(self, pitchtype, newVal):
        try:
            newVal = float(newVal)
        except:
            return -1
        
        if newVal < gsMuPitcherMin or \
                newVal > gsMuPitcherMax:
            return -1

        self.__batting['pitchMastery'][pitchtype] = newVal
        return 0

    def getPitchingPitchMasteryFastball(self):
        return self.__pitching['pitchMastery'][gsFASTBALL]

    def setPitchingPitchMasteryFastball(self, newVal):
        return self._setPitchingPitchMastery(gsFASTBALL, newVal)

    def getPitchingPitchMasteryCurveball(self):
        return self.__pitching['pitchMastery'][gsCURVEBALL]

    def setPitchingPitchMasteryCurveball(self, newVal):
        return self._setPitchingPitchMastery(gsCURVEBALL, newVal)

    def getPitchingPitchMasterySlider(self):
        return self.__pitching['pitchMastery'][gsSLIDER]

    def setPitchingPitchMasterySlider(self, newVal):
        return self._setPitchingPitchMastery(gsSLIDER, newVal)
    
    def getPitchingPitchMasteryChangeup(self):
        return self.__pitching['pitchMastery'][gsCHANGEUP]

    def setPitchingPitchMasteryChangeup(self, newVal):
        return self._setPitchingPitchMastery(gsCHANGEUP, newVal)

    def getPitchingPitchMasteryKnuckleball(self):
        return self.__pitching['pitchMastery'][gsKNUCKLEBALL]

    def setPitchingPitchMasteryKnuckleball(self, newVal):
        return self._setPitchingPitchMastery(gsKNUCKLEBALL, newVal)

    def getPitchingPitchMasterySinker(self):
        return self.__pitching['pitchMastery'][gsSINKER]

    def setPitchingPitchMasterySinker(self, newVal):
        return self._setPitchingPitchMastery(gsSINKER, newVal)

    def getPitchingPitchMasterySpitball(self):
        return self.__pitching['pitchMastery'][gsSPITBALL]

    def setPitchingPitchMasterySpitball(self, newVal):
        return self._setPitchingPitchMastery(gsSPITBALL, newVal)

    def getPitchingPitchMasteryForkball(self):
        return self.__pitching['pitchMastery'][gsFORKBALL]

    def setPitchingPitchMasteryForkball(self, newVal):
        return self._setPitchingPitchMastery(gsFORKBALL, newVal)

    def getPitchingZoneMasteryMatrix(self):
        return self.__pitching['zoneMastery']

    def getPitcherStamina(self):
        return self.__pitching['stamina']

    def getPitcherStrength(self):
        return self.__pitching['strength']

    def getPitcherControl(self):
        return self.__pitching['control']


    #BATTING SPECIFIC
    def getBattingPitchMasteryMatrix(self):
        return self.__batting['pitchMastery']

    ######
    def _setBattingPitchMastery(self, pitchtype, newVal):
        try:
            newVal = float(newVal)
        except:
            return -1

        if newVal < gsMuBatterMin or \
                newVal > gsMuBatterMax:
            return -1

        self.__batting['pitchMastery'][pitchtype] = newVal
        return 0

    def getBattingPitchMasteryFastball(self):
        return self.__batting['pitchMastery'][gsFASTBALL]
    
    def setBattingPitchMasteryFastball(self, newVal):
        return self._setBattingPitchMastery(gsFASTBALL, newVal)

    def getBattingPitchMasteryCurveball(self):
        return self.__batting['pitchMastery'][gsCURVEBALL]

    def setBattingPitchMasteryCurveball(self, newVal):
        return self._setBattingPitchMastery(gsCURVEBALL, newVal)

    def getBattingPitchMasterySlider(self):
        return self.__batting['pitchMastery'][gsSLIDER]

    def setBattingPitchMasterySlider(self, newVal):
        return self._setBattingPitchMastery(gsSLIDER, newVal)

    def getBattingPitchMasteryChangeup(self):
        return self.__batting['pitchMastery'][gsCHANGEUP]

    def setBattingPitchMasteryChangeup(self, newVal):
        return self._setBattingPitchMastery(gsCHANGEUP, newVal)

    def getBattingPitchMasteryKnuckleball(self):
        return self.__batting['pitchMastery'][gsKNUCKLEBALL]

    def setBattingPitchMasteryKnuckleball(self, newVal):
        return self._setBattingPitchMastery(gsKNUCKLEBALL, newVal)

    def getBattingPitchMasterySinker(self):
        return self.__batting['pitchMastery'][gsSINKER]

    def setBattingPitchMasterySinker(self, newVal):
        return self._setBattingPitchMastery(gsSINKER, newVal)

    def getBattingPitchMasterySpitball(self):
        return self.__batting['pitchMastery'][gsSPITBALL]

    def setBattingPitchMasterySpitball(self, newVal):
        return self._setBattingPitchMastery(gsSPITBALL, newVal)

    def getBattingPitchMasteryForkball(self):
        return self.__batting['pitchMastery'][gsFORKBALL]

    def setBattingPitchMasteryForkball(self, newVal):
        return self._setBattingPitchMastery(gsFORKBALL, newVal)

    ##############


    def getBattingZoneMasteryMatrix(self):
        return self.__batting['zoneMastery']

    def getSpeed(self):
        return self.__running['speed']

    def getDefense(self):
        return self.__fielding['defense']

    def getLeadership(self):
        return self.__character['leadership']

    def setLeadership(self, newVal):
        if type(newVal) != type(0):
            return -1
        self.__character['leadership'] = newVal
        return 0

    def getPrestige(self):
        return self.__character['prestige']

    def setPrestige(self, newVal):
        if type(newVal) != type(0):
            return -1

        self.__character['prestige'] = newVal
        return 0

    def getPatience(self):
        return self.__batting['patience']

    def setPatience(self, newVal):
        if type(newVal) != type(0):
            return -1
        self.__batting['patience'] = newVal
        return 0


def main():

    pa = PlayerAbilities()
    print pa
    pa.setBattingPitchMasteryFastball(1.1)
    print pa
    pa.setBattingPitchMasteryFastball('2.1')
    print pa

    pa.setPitchingPitchMasteryFastball(1.1)
    print pa
    pa.setPitchingPitchMasteryFastball('2.1')
    print pa


if __name__ == "__main__":
    main()

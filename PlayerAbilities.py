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

Chi2b0 = gsChi2BatterMin + .25
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

batterPitchMastery = {'curveball':gsMuBatterMin, 
                       'fastball':gsMuBatterMin,
                       'slider':gsMuBatterMin,
                       'changeup':gsMuBatterMin,
                       'knuckleball':gsMuBatterMin}

pitcherZoneMastery = [Chi2p0, Chi2p0, Chi2p0,
                      Chi2p0, Chi2p0, Chi2p0,
                      Chi2p0, Chi2p0, Chi2p0]


pitcherPitchMastery = {'curveball':gsMuPitcherMin, 
                       'fastball':gsMuPitcherMin,
                       'slider':gsMuPitcherMin,
                       'changeup':gsMuPitcherMin,
                       'knuckleball':gsMuPitcherMin}



#PITCHING
pitcherAbil = {'zoneMastery':pitcherZoneMastery, #pitchers effectiveness at throwing pitches by zone
               'pitchMastery':pitcherPitchMastery,#how good a pitcher is at throwing various pitches
               'strength':0,#affects the speed of the pitches thrown
               'control':0, #affects if a whether a pitch is a ball or not
               'stamina':0,   #affects how many pitches they can throw before their accuracy and speed are temporarily affected
               }

#BATTER abilities
batterAbil = {'zoneMastery':batterZoneMastery,#how good a batter is at making contact with a pitch in a given location
              'pitchMastery':batterPitchMastery,#how good a batter is at making contact with a certain kind of pitch
              'powerZones':batterPowerZones, #effects the zones where hitters have power
              'patience':0, #effects how often the batter chances balls/bad pitches
              }

#FIELDING
fieldingAbil = {'defense':0, #effects the range/radius of the player on defense
                }
 
#RUNNING   
runningAbil = {'speed':0, #effects whether extra bases can be squeezed out on hits
               }

#CHARACTER
characterAbil = {'leadership':0, #makes everyone on the team a little better
                 'prestige':0, #affects how much money the player draws per game
                 }

class PlayerAbilities:

    def __init__(self):

        self.__fielding = fieldingAbil
        self.__batting = batterAbil
        self.__pitching = pitcherAbil
        self.__running = runningAbil
        self.__character = characterAbil
        
        return

    def __getstate__(self):
        fmt = "{'fielding':%s,'batting':%s,'pitching':%s,'running':%s,'character':%s}"
        return fmt % (str(self.__fielding), 
                      str(self.__batting),
                      str(self.__pitching),
                      str(self.__running),
                      str(self.__character))

    
    def __setstate__(self, dictStr):
        print "TODO: check for eval errors"
        d = eval(dictStr)
        self.__fielding = d['fielding']
        self.__batting = d['batting']
        self.__pitching = d['pitching']
        self.__running = d['running']
        self.__character = d['character']
        return


    def getPitchingPitchMasteryMatrix(self):
        return self.__pitching['pitchMastery']

    def getPitchingZoneMasteryMatrix(self):
        return self.__pitching['zoneMastery']

    def getBattingPitchMasteryMatrix(self):
        return self.__batting['pitchMastery']

    def getBattingZoneMasteryMatrix(self):
        return self.__batting['zoneMastery']


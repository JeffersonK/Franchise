#############
#
#
#
# PlayerSkillTraining.py
#
#
#############
from ObjectDB import *
from Globals import *

class PlayerSkillTraining:

    def __init__(self, guid, moneyCost, energyCost, textDesc,
                 type, skillIncList):
        
        self.__guid = guid
        self.__moneyCost = moneyCost
        self.__energyCost = energyCost
        self.__textDesc = textDesc
        self.__skillType = type 
        self.__skillsInc = skillIncList #[(skillID, skillpoints),...]
        return


    def __str__(self):
        return self.__getstate__()

    def __getstate__(self):
        fmt = "{'%s':%d," + \
            "'%s':%d," + \
            "'%s':%d," + \
            "'%s':'%s'," + \
            "'%s':'%s'," + \
            "'%s':%s}"
        
        stateStr = fmt % (PLAYERSKILLTRAINING_GUID, self.__guid, 
                          PLAYERSKILLTRAINING_MONEYCOST, self.__moneyCost, 
                          PLAYERSKILLTRAINING_ENERGYCOST, self.__energyCost, 
                          PLAYERSKILLTRAINING_TEXTDESC, self.__textDesc,
                          PLAYERSKILLTRAINING_SKILLTYPE, self.__skillType,
                          PLAYERSKILLTRAINING_SKILLSINC, str(self.__skillsInc))
        return stateStr


    def __setstate__(self, dictStr):
        d = eval(dictStr)
        self.__guid = d[PLAYERSKILLTRAINING_GUID] 
        self.__moneyCost = d[PLAYERSKILLTRAINING_MONEYCOST]
        self.__energyCost = d[PLAYERSKILLTRAINING_ENERGYCOST]
        self.__textDesc = d[PLAYERSKILLTRAINING_TEXTDESC]
        self.__skillType = d[PLAYERSKILLTRAINING_SKILLTYPE]
        self.__skillsInc = d[PLAYERSKILLTRAINING_SKILLSINC]
        return self

    def guid(self):
        return self.__guid

    def cost(self):
        return (self.__energyCost, self.__moneyCost)

    def getSkillType(self):
        return self.__skillType

    def getSkillName(self):
        return (self.__skillsInc[0])[0]

    def getSkillIncrease(self):
        return (self.__skillsInc[0])[1]

from ProbabilityEngine import *


Chi2b0 = 0.0
Chi2p0 = 0.0
                    
gsMAX_PITCHMASTERY_LEVEL = gsNUM_PITCHMASTERY_LEVELS
gsMIN_PITCHMASTERY_LEVEL = 0
gsMAX_ZONEMASTERY_LEVEL = gsNUM_ZONEMASTERY_LEVELS
gsMIN_ZONEMASTERY_LEVEL = 0


class PitcherPlayerSkills:
    
    def __init__(self):
        
        #Pitcher Skills
        self.__skills = {PLAYERSKILLTRAINING_PITCHERPITCHTYPE:{PLAYERSKILLID_PITCHER_PITCH_FASTBALL:Chi2p0,
                                                               PLAYERSKILLID_PITCHER_PITCH_CURVEBALL:Chi2p0,
                                                               PLAYERSKILLID_PITCHER_PITCH_SLIDER:Chi2p0,
                                                               PLAYERSKILLID_PITCHER_PITCH_CHANGEUP:Chi2p0,
                                                               PLAYERSKILLID_PITCHER_PITCH_FORKBALL:Chi2p0,
                                                               PLAYERSKILLID_PITCHER_PITCH_SINKER:Chi2p0,
                                                               PLAYERSKILLID_PITCHER_PITCH_SPITBALL:Chi2p0,
                                                               PLAYERSKILLID_PITCHER_PITCH_KNUCKLEBALL:Chi2p0},
                         PLAYERSKILLTRAINING_PITCHERZONETYPE:{PLAYERSKILLID_PITCHER_ZONE_0:Chi2p0,
                                                              PLAYERSKILLID_PITCHER_ZONE_1:Chi2p0,
                                                              PLAYERSKILLID_PITCHER_ZONE_2:Chi2p0,
                                                              PLAYERSKILLID_PITCHER_ZONE_3:Chi2p0,
                                                              PLAYERSKILLID_PITCHER_ZONE_4:Chi2p0,
                                                              PLAYERSKILLID_PITCHER_ZONE_5:Chi2p0,
                                                              PLAYERSKILLID_PITCHER_ZONE_6:Chi2p0,
                                                              PLAYERSKILLID_PITCHER_ZONE_7:Chi2p0,
                                                              PLAYERSKILLID_PITCHER_ZONE_8:Chi2p0}
                         }
        
    def __str__(self):
        return self.__getstate__()
    
    def __getstate__(self):
        return str(self.__skills)

    def __setstate__(self, dict):
        #self.__skills = eval(dictStr) 
        self.__skills = dict
        return self

    def getPitchingZoneMasteryMatrix(self):
        return self.__skills[PLAYERSKILLTRAINING_PITCHERZONETYPE]

    def getPitchingPitchMasteryMatrix(self):
         return self.__skills[PLAYERSKILLTRAINING_PITCHERPITCHTYPE]

    def trainSkills(self, trainObj):
        skillType = trainObj.getSkillType()
        skill = trainObj.getSkillName()
        increase = trainObj.getSkillIncrease()
        self.__skills[skillType][skill] += increase
        return 0

class BatterPlayerSkills:

    def __init__(self):
                
        self.__skills = {PLAYERSKILLTRAINING_BATTERPITCHTYPE:{PLAYERSKILLID_BATTER_PITCH_FASTBALL:Chi2b0,
                                                              PLAYERSKILLID_BATTER_PITCH_CURVEBALL:Chi2b0,
                                                              PLAYERSKILLID_BATTER_PITCH_SLIDER:Chi2b0,
                                                              PLAYERSKILLID_BATTER_PITCH_CHANGEUP:Chi2b0,
                                                              PLAYERSKILLID_BATTER_PITCH_FORKBALL:Chi2b0,
                                                              PLAYERSKILLID_BATTER_PITCH_SINKER:Chi2b0,
                                                              PLAYERSKILLID_BATTER_PITCH_SPITBALL:Chi2b0,
                                                              PLAYERSKILLID_BATTER_PITCH_KNUCKLEBALL:Chi2b0},
                         
                         PLAYERSKILLTRAINING_BATTERZONETYPE:{PLAYERSKILLID_BATTER_ZONE_0:Chi2b0,
                                                             PLAYERSKILLID_BATTER_ZONE_1:Chi2b0,
                                                             PLAYERSKILLID_BATTER_ZONE_2:Chi2b0,
                                                             PLAYERSKILLID_BATTER_ZONE_3:Chi2b0,
                                                             PLAYERSKILLID_BATTER_ZONE_4:Chi2b0,
                                                             PLAYERSKILLID_BATTER_ZONE_5:Chi2b0,
                                                             PLAYERSKILLID_BATTER_ZONE_6:Chi2b0,
                                                             PLAYERSKILLID_BATTER_ZONE_7:Chi2b0,
                                                             PLAYERSKILLID_BATTER_ZONE_8:Chi2b0}
                         }
        
        
    def __str__(self):
        return self.__getstate__()

    def __getstate__(self):
        #fmt = "{'%s':\"%s\"" +\
        #    "'%s':\"%s\"}"
        
        #state = fmt % (PLAYERSKILLTRAINING_BATTERZONETYPE, 
        #               str(self.__batterZoneMastery),
        #               PLAYERSKILLTRAINING_BATTERPITCHTYPE, 
        #               str(self.__batterPitchMastery))
        #return state
        return str(self.__skills)

    def __setstate__(self, dict):
        self.__skills = dict
        return self

    def getBattingZoneMasteryMatrix(self):
        return self.__skills[PLAYERSKILLTRAINING_BATTERZONETYPE]

    def getBattingPitchMasteryMatrix(self):
         return self.__skills[PLAYERSKILLTRAINING_BATTERPITCHTYPE]

    def trainSkills(self, trainObj):
        skillType = trainObj.getSkillType()
        skill = trainObj.getSkillName()
        increase = trainObj.getSkillIncrease()
        self.__skills[skillType][skill] += increase
        return 0
        
def main():
    trainingDB = ObjectDB("trainingdb", "trn")
    trainingObj = PlayerSkillTraining(trainingDB.getNextObjectGuid(),
                                      100, 2, "Improve Pitcher Curveball",
                                      PLAYERSKILLTRAINING_PITCHERPITCHTYPE,
                                      [(PLAYERSKILLID_PITCHER_PITCH_CURVEBALL, 1)])
                                      
    trainingDB.addObject(trainingObj.guid(), trainingObj)

    trainingObj = PlayerSkillTraining(trainingDB.getNextObjectGuid(),
                                      100, 3, "Improve Pitcher Fastball",
                                      PLAYERSKILLTRAINING_PITCHERPITCHTYPE,
                                      [(PLAYERSKILLID_PITCHER_PITCH_FASTBALL, 1)])
                                      
    trainingDB.addObject(trainingObj.guid(), trainingObj)


    trainingObj = PlayerSkillTraining(trainingDB.getNextObjectGuid(),
                                      100, 3, "Improve Pitcher Changeup",
                                      PLAYERSKILLTRAINING_PITCHERPITCHTYPE,
                                      [(PLAYERSKILLID_PITCHER_PITCH_CHANGEUP, 1)])
                                      
    trainingDB.addObject(trainingObj.guid(), trainingObj)

    trainingObj = PlayerSkillTraining(trainingDB.getNextObjectGuid(),
                                      100, 3, "Improve Pitcher Slider",
                                      PLAYERSKILLTRAINING_PITCHERPITCHTYPE,
                                      [(PLAYERSKILLID_PITCHER_PITCH_SLIDER, 1)])
                                      
    trainingDB.addObject(trainingObj.guid(), trainingObj)

    trainingDB.writeAll()
    del(trainingDB)
    return


if __name__ == "__main__":
    main()

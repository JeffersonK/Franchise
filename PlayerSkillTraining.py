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
            "'%s':\"%s\"}"
        
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

def main():
    trainingDB = ObjectDB("trainingdb", "trn")
    trainingObj = PlayerSkillTraining(trainingDB.getNextObjectGuid(),
                                      100, 2, "Improve Pitcher Curveball",
                                      PLAYERSKILLTRAINING_PITCHERTYPE,
                                      [(PLAYERSKILLID_PITCHER_PITCH_CURVEBALL, 1)])
                                      
    trainingDB.addObject(trainingObj.guid(), trainingObj)

    trainingDB.writeAll()
    del(trainingDB)
    return


if __name__ == "__main__":
    main()

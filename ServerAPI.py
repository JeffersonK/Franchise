#############
#
#
#
# serverAPI.py
#
#
#############
import time
import json
from ObjectDB import *
import Player
import leagueleaders
from PlayerSkills import *
from Globals import *

############
#
# SERVERAPI CONSTANTS - in Globals.py
#
############


############
#
# INTERNAL HELPER FUNCTIONS 
# DONT CALL THESE
#
############
def _openPlayerDB():
    PlayerDB = ObjectDB("playersdb","plr")
    return PlayerDB

def _closePlayerDB(playerDB):
    playerDB.writeAll()
    del(playerDB)
    playerDB = None
    return

#############
#
#
#
#############
def ServerAPIGetLeaderboard(playerGUID):
    return

#############
#
# Returns a JSON serialized Player Object
# or None if it doesn't exist
#############
def ServerAPIGetPlayerState(playerGUID):
    plyrDB = _openPlayerDB()
    plyr =  plyrDB.getObjectHandle(playerGUID)
    if plyr == None:
        return None
    jsonPlyr = json.dumps(plyr.__getstate__())
    _closePlayerDB(plyrDB)
    return jsonPlyr

#############
#
# Returns a JSON serialized set of Events
# or an empty list
# the events are deleted as they are read
#############
def ServerAPIGetPlayerEvents(playerGUID):
    return []

#############
#
# Returns a serialzed JSON List Object
# of type [(playerGUID, playerName, Position),...]
#
# If a person doesn't have enough friend to fill slots computer generated
# characters are offered
#############
def ServerAPIGetLineupCandidates(playerGUID):
    guidList = []
    plyrDB = _openPlayerDB()
    plyrObj =  plyrDB.getObjectHandle(playerGUID)
    if plyrObj == None:
        return None
    
    for (guid, plyr) in plyrDB.iteritems():
        if guid != playerGUID:
            guidList += [(guid, plyr.getName(), plyr.getPosition())]
    jsonList = json.dumps(guidList)
    _closePlayerDB(plyrDB)
    return jsonList

#############
#
# battingLineup: [playerGUID, ...] where  1 <= len() <= 9
# pitchingRotation [playerGUID, ...] where len() <= 3 
#
#############
def ServerAPISetDefaultGameState(playerGUID, battingLineup, pitchingRotation):
    return


#############
#
# Common Abilities:
# Batter Abilities:
# Pitcher Abilities:
#         (All Defined at top of this file)
#
#############
def ServerAPIUseStatPoint(playerGUID, abilityName):
    plyrDB = _openPlayerDB()
    plyr =  plyrDB.getObjectHandle(playerGUID)
    if plyr == None:
        return -1 #PLAYER DOESNT EXIST
    if plyr.incStatPoint(abilityName) < 0:
        return -2 #UKNOWN ABILITY or NO UNUSED STAT POINTS
    _closePlayerDB(plyrDB)
    plyrDB = None
    return 0

#############
#
# return a list of training  
#   [(trainingGUID, description, moneyCost, energyCost)]
#
#############
def ServerAPIGetTrainingJobs(playerGUID):
    plyrDB = _openPlayerDB()
    plyr =  plyrDB.getObjectHandle(playerGUID)
    if plyr == None:
        return -1 #PLAYER DOESNT EXIST
    trainingJobs = plyr.getTrainingOptions()
    jsonstr = json.dumps(trainingJobs)
    _closePlayerDB(plyrDB)
    plyrDB = None
    return jsonstr

#############
#
#
#
#############
def ServerAPITrainSkills(playerGUID, trainingGUID):
    plyrDB = _openPlayerDB()
    plyr =  plyrDB.getObjectHandle(playerGUID)
    if plyr == None:
        return -1 #PLAYER DOESNT EXIST
    ret = plyr.train(trainingGUID)
    _closePlayerDB(plyrDB)
    plyrDB = None
    return ret

#############
#
#
#
#############
def ServerAPIGetCandidateChallenges(playerGUID):
    return

#############
#
#
#
#############
def ServerAPIPlayGame(playerGUID, challengedPlayerGUID):
    return



#############
#
#
#
#############
def ServerAdminAPISetPlayerState(playerGUID, JSONplayerState):
    
    plyrDB = _openPlayerDB()
    #jsonPlyr = ServerAPIGetPlayerState(playerGUID)
    plyrDictStr = json.loads(JSONplayerState)
    plyrobj = Player.Player(-1).__setstate__(plyrDictStr)
    plyrDB.updateObject(playerGUID, plyrobj)
    #print p
    #print pobj
    _closePlayerDB(plyrDB)
    return




#############
#
# For Testing
#
#############
def main():


    plyr0 = ServerAPIGetPlayerState(0)
    print plyr0

    jp = json.loads(plyr0)
    print type(jp)

    lc = ServerAPIGetLineupCandidates(0)
    print lc

    ServerAdminAPISetPlayerState(0, plyr0)

    #print ServerAPIUseStatPoint(0,PLAYERABILITY_MAXENERGYPOINTS) 
    #print ServerAPIUseStatPoint(0,PLAYERABILITY_MAXCHALLENGEPOINTS)
    #print ServerAPIUseStatPoint(0,PLAYERABILITY_DEFENSE)
    #print ServerAPIUseStatPoint(0,PLAYERABILITY_PRESTIGE)
    #print ServerAPIUseStatPoint(0,PLAYERABILITY_LEADERSHIP)
    #print ServerAPIUseStatPoint(0,PLAYERABILITY_BATTER_POWER)
    #print ServerAPIUseStatPoint(0,PLAYERABILITY_BATTER_PATIENCE)
    #print ServerAPIUseStatPoint(0,PLAYERABILITY_PITCHER_CONTROL)
    #print ServerAPIUseStatPoint(0,PLAYERABILITY_PITCHER_STAMINA)

    print ServerAPIGetTrainingJobs(0)
    print ServerAPITrainSkills(0,0)

    print ServerAPIGetTrainingJobs(1)

if __name__ == "__main__":
    main()

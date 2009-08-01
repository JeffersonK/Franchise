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
    jsonPlyr = json.dumps(plyr.__getstate__())
    _closePlayerDB(plyrDB)
    return jsonPlyr

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
#
#
#############
def ServerAPIUseStatPoint(playerGUID, abilityName):
    return

#############
#
#
#
#############
def ServerAPIGetTrainingJobs(playerGUID):
    return

#############
#
#
#
#############
def ServerAPITrainSkills(playerGUID, trainingGUID):
    return

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


if __name__ == "__main__":
    main()

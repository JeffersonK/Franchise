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
import leagueleaders

def _openPlayerDB():
    PlayerDB = ObjectDB("players","plr")
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
    for (guid, plyr) in plyrDB.iteritems(players):
        if guid != playerGUID:
            guidList += [(guid, plyr.getName(), plyr.getPosition())]
    _closePlayerDB(plyrDB)
    return guidList

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
def ServerAdminAPISetPlayerState(playerGUID, playerState):
    return




#############
#
# For Testing
#
#############
def main():


    plyr0 = ServerAPIGetPlayerState(0)
    print plyr0

    lc = ServerAPIGetLineupCandidates(0)
    print lc

if __name__ == "__main__":
    main()
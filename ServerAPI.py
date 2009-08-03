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

############
#
# SERVERAPI CONSTANTS
#
############

#Common Abilities:
PLAYERABILITY_MAXENERGYPOINTS =    'PLYRABIL_MAXENG'
PLAYERABILITY_MAXCHALLENGEPOINTS = 'PLYRABIL_MAXCHL'
PLAYERABILITY_DEFENSE =            'PLYRABIL_DEFENSE'
PLAYERABILITY_PRESTIGE =           'PLYRABIL_PRSTIGE' 
PLAYERABILITY_LEADERSHIP =         'PLYRABIL_LDRSHIP'

#Batter Abilities:
PLAYERABILITY_BATTER_POWER =       'PLYRABIL_BATPOWR'
PLAYERABILITY_BATTER_PATIENCE =    'PLYRABIL_BATPATC'

#Pitcher Abilities:
PLAYERABILITY_PITCHER_CONTROL =    'PLYRABIL_PITCONT'
PLAYERABILITY_PITCHER_STAMINA =    'PLYRABIL_PITSTAM'

#Player Skills/Training Constants
PLAYERSKILLTRAINING_GUID       =  'guid'
PLAYERSKILLTRAINING_MONEYCOST  =  'moneyCost'
PLAYERSKILLTRAINING_ENERGYCOST =  'energyCost'
PLAYERSKILLTRAINING_TEXTDESC   =  'textDesc'
PLAYERSKILLTRAINING_SKILLTYPE =   'skillType'
PLAYERSKILLTRAINING_SKILLSINC =   'skillsInc'
PLAYERSKILLTRAINING_PITCHERTYPE = 'PITS'
PLAYERSKILLTRAINING_BATTERTYPE =  'BATS'

PLAYERSKILLID_PITCHER_PITCH_FASTBALL = 'PIT' + gsFASTBALL
PLAYERSKILLID_PITCHER_PITCH_CURVEBALL = 'PIT' + gsCURVEBALL
PLAYERSKILLID_PITCHER_PITCH_SLIDER = 'PIT' + gsSLIDER
PLAYERSKILLID_PITCHER_PITCH_CHANGEUP = 'PIT' + gsCHANGEUP
PLAYERSKILLID_PITCHER_PITCH_FORKBALL = 'PIT' + gsFORKBALL
PLAYERSKILLID_PITCHER_PITCH_SINKER = 'PIT' + gsSINKER
PLAYERSKILLID_PITCHER_PITCH_SPITBALL = 'PIT' + gsSPITBALL
PLAYERSKILLID_PITCHER_PITCH_KNUCKLEBALL = 'PIT' + gsKNUCKLEBALL

PLAYERSKILLID_PITCHER_ZONE_0 = 'PIT' + 'ZONE0'
PLAYERSKILLID_PITCHER_ZONE_1 = 'PIT' + 'ZONE1'
PLAYERSKILLID_PITCHER_ZONE_2 = 'PIT' + 'ZONE2'
PLAYERSKILLID_PITCHER_ZONE_3 = 'PIT' + 'ZONE3'
PLAYERSKILLID_PITCHER_ZONE_4 = 'PIT' + 'ZONE4'
PLAYERSKILLID_PITCHER_ZONE_5 = 'PIT' + 'ZONE5'
PLAYERSKILLID_PITCHER_ZONE_6 = 'PIT' + 'ZONE6'
PLAYERSKILLID_PITCHER_ZONE_7 = 'PIT' + 'ZONE7'
PLAYERSKILLID_PITCHER_ZONE_8 = 'PIT' + 'ZONE8'


PLAYERSKILLID_BATTER_PITCH_FASTBALL = 'HIT' + gsFASTBALL
PLAYERSKILLID_BATTER_PITCH_CURVEBALL ='HIT' + gsCURVEBALL
PLAYERSKILLID_BATTER_PITCH_SLIDER = 'HIT' +gsSLIDER
PLAYERSKILLID_BATTER_PITCH_CHANGEUP = 'HIT' + gsCHANGEUP
PLAYERSKILLID_BATTER_PITCH_FORKBALL = 'HIT' + gsFORKBALL
PLAYERSKILLID_BATTER_PITCH_SINKER = 'HIT' + gsSINKER
PLAYERSKILLID_BATTER_PITCH_SPITBALL = 'HIT' + gsSPITBALL
PLAYERSKILLID_BATTER_PITCH_KNUCKLEBALL = 'HIT' + gsKNUCKLEBALL


PLAYERSKILLID_BATTER_ZONE_0 = 'HIT' + 'ZONE0'
PLAYERSKILLID_BATTER_ZONE_1 = 'HIT' + 'ZONE1'
PLAYERSKILLID_BATTER_ZONE_2 = 'HIT' + 'ZONE2'
PLAYERSKILLID_BATTER_ZONE_3 = 'HIT' + 'ZONE3'
PLAYERSKILLID_BATTER_ZONE_4 = 'HIT' + 'ZONE4'
PLAYERSKILLID_BATTER_ZONE_5 = 'HIT' + 'ZONE5'
PLAYERSKILLID_BATTER_ZONE_6 = 'HIT' + 'ZONE6'
PLAYERSKILLID_BATTER_ZONE_7 = 'HIT' + 'ZONE7'
PLAYERSKILLID_BATTER_ZONE_8 = 'HIT' + 'ZONE8'

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

if __name__ == "__main__":
    main()

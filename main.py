import Globals
import Franchise
import Player
import GameState
#import PlayerDB
#import Stadium
import SimRunner
#import pprint
import ObjectDB

LOAD = 1
GENERATE = 0

PlayerDB = ObjectDB.ObjectDB("players", "plr")
FranchiseDB = ObjectDB.ObjectDB("franchises", "frn")

def generateTeam():
    team = {}
    for pos in Globals.gsPlayerPositions:
        p = Player.Player(Globals.globalState.nextPlayerGUID(), pos)
        PlayerDB.addObject(p.guid(), p)
        team[p.guid()] = pos
    return team

f1 = None
f2 = None

#GENERATE 1
if GENERATE:
    f1 = Franchise.Franchise("frza", "frzaites", Globals.globalState.nextFranchiseGUID())
    FranchiseDB.addObject(f1.guid(), f1)

    playerDict1 = generateTeam()
    for playerGUID in playerDict1.keys():
        handle = PlayerDB.getObjectHandle(playerGUID)
        handle.setPlayerFranchise(f1.guid())
    f1.addPlayers(playerDict1)

#LOAD 1
if LOAD:
    f1 = FranchiseDB.getObjectHandle(0)
    for playerGUID in range(0,9):#playerList1.keys():
        handle = PlayerDB.getObjectHandle(playerGUID)
        f1.addPlayers({playerGUID:handle.getPosition()})

    
f1.setLineup()
f1.setRotation()



# GENERATE 2
if GENERATE:
    f2 = Franchise.Franchise("jza", "jzites", Globals.globalState.nextFranchiseGUID())
    FranchiseDB.addObject(f2.guid(), f2)
    playerDict2 = generateTeam()
    for playerGUID in playerDict2.keys():
        handle = PlayerDB.getObjectHandle(playerGUID)
        handle.setPlayerFranchise(f2.guid())
    f2.addPlayers(playerDict2)

#LOAD 2
if LOAD:
    f2 = FranchiseDB.getObjectHandle(1)
    for playerGUID in range(9,18):#playerList2.keys():
        handle = PlayerDB.getObjectHandle(playerGUID)
        f2.addPlayers({playerGUID:handle.getPosition()})
    
f2.setLineup()
f2.setRotation()

tgs1 = Franchise.TeamGameState(f1)
tgs2 = Franchise.TeamGameState(f2)

gameState = GameState.GameState(tgs1,tgs2)

sim = SimRunner.SimRunner(gameState)
while 1:
    gameEvents = sim.step()
    print "Game Events: %s\n" % str(gameEvents)
    if "GAMEOVER" in gameEvents:#gameEvents[-1].gameOver():
        break

playerGameStates = tgs1.getPlayerGameStates()
updatePlayerStatsEvents = []
for (playerGUID, playerGameState) in playerGameStates.items():
    handle = PlayerDB.getObjectHandle(playerGUID)
    updaterPlaterStatsEvents = handle.updatePlayerStats(playerGameState)

playerGameStates = tgs2.getPlayerGameStates()
updatePlayerStatsEvents = []
for (playerGUID, playerGameState) in playerGameStates.items():
    handle = PlayerDB.getObjectHandle(playerGUID)
    updaterPlaterStatsEvents = handle.updatePlayerStats(playerGameState)

#call this after the sim to get relevent events like who won
gameEvents = gameState.getGameEvents()

endGameTeamEvents1 = f1.updateFranchiseStats(tgs1, True)
print endGameTeamEvents1

endGameTeamEvents2 = f2.updateFranchiseStats(tgs2, False)
print endGameTeamEvents1

PlayerDB.writeAll()
FranchiseDB.writeAll()

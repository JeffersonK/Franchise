import Globals
import Franchise
import Player
import GameState
#import PlayerDB
#import Stadium
import SimRunner
#import pprint
import ObjectDB


PlayerDB = ObjectDB.ObjectDB("players", "plr")

def generateTeam():
    team = {}
    for pos in Globals.gsPlayerPositions:
        p = Player(Globals.globalState.nextPlayerGUID(), pos)
        PlayerDB.addObject(p.guid(), p)
        team[p.guid()] = pos

    return team

f1 = Franchise.Franchise("frza", "frzaites", Globals.globalState.nextFranchiseGUID())

#GENERATE 1
#playerDict1 = Player.generateTeam()
#for playerGUID in playerDict1.keys():
#    handle = PlayerDB.gsPlayerDB.getPlayerHandle(playerGUID)
#    handle.setPlayerFranchise(f1.getFranchiseGUID())
#f1.addPlayers(playerDict1)

#LOAD 1
for playerGUID in range(0,9):#playerList1.keys():
    handle = PlayerDB.getObjectHandle(playerGUID)
    f1.addPlayers({playerGUID:handle.getPosition()})

f1.setLineup()
f1.setRotation()

f2 = Franchise.Franchise("jza", "jzites", Globals.globalState.nextFranchiseGUID())

# GENERATE 2
#playerDict2 = Player.generateTeam()
#for playerGUID in playerDict2.keys():
#    handle = PlayerDB.gsPlayerDB.getPlayerHandle(playerGUID)
#    handle.setPlayerFranchise(f2.getFranchiseGUID())
#f2.addPlayers(playerDict2)

#LOAD 2
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

#call this after the sim to get relevent events
gameEvents = gameState.getGameEvents()

endGameTeamEvents1 = f1.updateFranchiseStats(tgs1, True)
print endGameTeamEvents1

endGameTeamEvents2 = f2.updateFranchiseStats(tgs2, False)
print endGameTeamEvents1

PlayerDB.writeAll()

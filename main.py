import Globals
import Franchise
import Player
import GameState
import PlayerDB
#import Stadium
import SimRunner
#import pprint

f1 = Franchise.Franchise("frza", "frzaites", Globals.globalState.nextFranchiseGUID())
playerList1 = Player.generateTeam()
f1.addPlayers(playerList1)

#for playerGUID in range(0,9):#playerList1.keys():
#    handle = PlayerDB.gsPlayerDB.getPlayerHandle(playerGUID)
#    f1.addPlayers({playerGUID:handle.getPosition()})
#    handle.setPlayerFranchise(f1.getFranchiseGUID())

f1.setLineup()
f1.setRotation()

f2 = Franchise.Franchise("jza", "jzites", Globals.globalState.nextFranchiseGUID())
playerList2 = Player.generateTeam()

#for playerGUID in range(9,18):#playerList2.keys():
#    handle = PlayerDB.gsPlayerDB.getPlayerHandle(playerGUID)
#    f2.addPlayers({playerGUID:handle.getPosition()})
#    handle.setPlayerFranchise(f2.getFranchiseGUID())
    
f2.addPlayers(playerList2)
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

PlayerDB.gsPlayerDB.writeAll()

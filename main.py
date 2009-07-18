import Globals
import Franchise
import Player
import PlayerDB
import Stadium
import SimRunner
import pprint

f1 = Franchise.Franchise("frza", "frzaites", Globals.globalState.nextFranchiseGUID())
#playerList1 = Player.generateTeam()
#f1.addPlayers(playerList1)
for playerGUID in range(0,9):#playerList1.keys():
    handle = PlayerDB.gsPlayerDB.getPlayerHandle(playerGUID)
    f1.addPlayers({playerGUID:handle.getPosition()})
    handle.setPlayerFranchise(f1.getFranchiseGUID())

f1.setLineup()
f1.setRotation()

f2 = Franchise.Franchise("jza", "jzites", Globals.globalState.nextFranchiseGUID())
#playerList2 = Player.generateTeam()
for playerGUID in range(9,18):#playerList2.keys():
    handle = PlayerDB.gsPlayerDB.getPlayerHandle(playerGUID)
    f2.addPlayers({playerGUID:handle.getPosition()})
    handle.setPlayerFranchise(f2.getFranchiseGUID())
    
#f2.addPlayers(playerList2)
f2.setLineup()
f2.setRotation()

PlayerDB.gsPlayerDB.writeAll()

sim = SimRunner.GameRunner(f1,f2)
sim.run(-1)
pprint.pprint(sim.getGameEventLog())

import Globals
import Franchise
import Player
import PlayerDB
import Stadium
import SimRunner


f1 = Franchise.Franchise("frza", "frzaites", Globals.globalState.nextFranchiseGUID())

playerList1 = Player.generateTeam()
f1.addPlayers(playerList1)
f1.setLineup()
f1.setRotation()

f2 = Franchise.Franchise("jza", "jzites", Globals.globalState.nextFranchiseGUID())
playerList2 = Player.generateTeam()
f2.addPlayers(playerList2)
f2.setLineup()
f2.setRotation()

PlayerDB.gsPlayerDB.writeAll()

sim = SimRunner.GameRunner(f1,f2)
sim.run(-1)

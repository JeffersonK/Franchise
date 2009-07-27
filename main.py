import Globals
import Franchise
import Player
import GameState
import TeamGameState
import SimRunner
import ObjectDB

import sys
import getopt

def usage(errstr):

    helpstr = """\n\tTODO: fill in usage string"""

    print errstr + helpstr

    sys.exit(1)


#DEFAULS
PLAYERDBLOC = "players"
PLAYEROBJFILEEXT = "plr"

FRANCHISEDBLOC = "franchises"
FRANCHISEOBJFILEEXT = "frn"

GLOBALSDBLOC = "globals"
GLOBALSOBJFILEEXT = "gbl"

NRUNS = 1
GENERATETEAMS = False

gsPlayerDB = ObjectDB.ObjectDB(PLAYERDBLOC, PLAYEROBJFILEEXT)
gsFranchiseDB = ObjectDB.ObjectDB(FRANCHISEDBLOC, FRANCHISEOBJFILEEXT)
gsGlobalDB = ObjectDB.ObjectDB(GLOBALSOBJFILEEXT, GLOBALSDBLOC)

globalState = None

def generateTeam():#globalState):
    team = {}
    for pos in Globals.gsPOSITION_POSSTR.values():
        p = Player.Player(globalState.nextPlayerGUID())
        p.setPosition(pos)
        gsPlayerDB.addObject(p.guid(), p)
        team[p.guid()] = pos
    return team


def main():
    global globalState
    global NRUNS
    global GENERATETEAMS

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hgn:")
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    for o,a in opts:
        if o == '-g':
            GENERATETEAMS = True
        elif o == '-n':
            if GENERATETEAMS:
                usage("Can't do more than 1 run if generating teams.")
            NRUNS = int(a)
        elif o == '-h':
            usage()
        else:
            assert False, "unhandled option"
    

    #print GENERATETEAMS
    #print NRUNS
    #return
    runcnt = 0
    while runcnt < NRUNS:
        ### BEGIN LOOP ###
        if GENERATETEAMS:
            globalState = Globals.GlobalState()
            gsGlobalDB.addObject(0,globalState)
        else:
            globalState = gsGlobalDB.getObjectHandle(0)

        f1 = None
        f2 = None

        #GENERATE 1
        if GENERATETEAMS:
            f1 = Franchise.Franchise("frza", "frzaites", globalState.nextFranchiseGUID())
            gsFranchiseDB.addObject(f1.guid(), f1)

            playerDict1 = generateTeam()#globalState)
            for playerGUID in playerDict1.keys():
                handle = gsPlayerDB.getObjectHandle(playerGUID)
                handle.setPlayerFranchise(f1.guid())
            f1.addPlayers(playerDict1)

        #LOAD from disk
        else:
            f1 = gsFranchiseDB.getObjectHandle(0)
            for playerGUID in range(0,10):
                handle = gsPlayerDB.getObjectHandle(playerGUID)
                f1.addPlayers({playerGUID:handle.getPosition()})
    
        f1.setLineup()
        f1.setRotation()


        # GENERATE
        if GENERATETEAMS:
            f2 = Franchise.Franchise("jza", "jzites", globalState.nextFranchiseGUID())
            gsFranchiseDB.addObject(f2.guid(), f2)
            playerDict2 = generateTeam()#globalState)
            for playerGUID in playerDict2.keys():
                handle = gsPlayerDB.getObjectHandle(playerGUID)
                handle.setPlayerFranchise(f2.guid())
                f2.addPlayers(playerDict2)

        #LOAD from disk
        else:
            f2 = gsFranchiseDB.getObjectHandle(1)
            for playerGUID in range(10,20):
                handle = gsPlayerDB.getObjectHandle(playerGUID)
                f2.addPlayers({playerGUID:handle.getPosition()})
    
        f2.setLineup()
        f2.setRotation()

        tgs1 = TeamGameState.TeamGameState(f1)
        tgs2 = TeamGameState.TeamGameState(f2)

        gameState = GameState.GameState(tgs1,tgs2,gsPlayerDB)

        sim = SimRunner.SimRunner(gameState)
        sim.startSimTimer()
        while 1:
            gameEvents = sim.step()
        #print "Game Events: %s\n" % str(gameEvents)
            if "GAMEOVER" in gameEvents:#gameEvents[-1].gameOver():
                break
        dt = sim.stopSimTimer()
        print "Sim Timer: %.5f" % dt

        playerGameStates = tgs1.getPlayerGameStates()
        updatePlayerStatsEvents = []
        for (playerGUID, playerGameStats) in playerGameStates.iteritems():
            handle = gsPlayerDB.getObjectHandle(playerGUID)
            updaterPlaterStatsEvents = handle.updatePlayerStats(playerGameStats)

        playerGameStates = tgs2.getPlayerGameStates()
        updatePlayerStatsEvents = []
        for (playerGUID, playerGameStats) in playerGameStates.iteritems():
            handle = gsPlayerDB.getObjectHandle(playerGUID)
            updaterPlaterStatsEvents = handle.updatePlayerStats(playerGameStats)

        #call this after the sim to get relevent events like who won
        gameEvents = gameState.getGameEvents()

        endGameTeamEvents1 = f1.updateFranchiseStats(tgs1, True)
        #print endGameTeamEvents1

        endGameTeamEvents2 = f2.updateFranchiseStats(tgs2, False)
    #print endGameTeamEvents1

        gsGlobalDB.writeAll()
        gsPlayerDB.writeAll()
        gsFranchiseDB.writeAll()

        del(sim)
        sim = None
        del(gameState)
        gameState = None
        del(tgs1)
        tgs1 = None
        del(tgs2)
        tgs2 = None
        del(f1)
        f1 = None
        del(f2)
        f2 = None
    ### END LOOP ###

        runcnt += 1

    return

if __name__ == "__main__":
    main()

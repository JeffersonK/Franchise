import Globals
import cPickle
import os

gsPLAYERDBLOC = "players"
gsPLAYERFILEEXT = "plr"

class PlayerDB:

    #
    #
    #
    def __init__(self):

        #as we read the players from disk we load them into the cache
        #we pass references to them
        self.__dbcache = {}
        
        #make player directory
        if not os.path.exists(gsPLAYERDBLOC):
            os.makedirs(gsPLAYERDBLOC)

        return

    #
    #
    #
    def _makePlayerFileStr(self, playerObjectGuid):
        return os.path.join(gsPLAYERDBLOC, 
                            "%s.%s" % (playerObjectGuid, gsPLAYERFILEEXT))

    #
    #
    #
    def writeAll(self):
        for playerGUID in self.__dbcache.keys():
            self.write(playerGUID)
            
    #
    #
    #
    def write(self, playerGUID):
        if playerGUID not in self.__dbcache:
            print "write() - Inconsistency PlayerGUID:%d not in dbcache" % playerGUID
            return -1
        
        playerObject = self.__dbcache[playerGUID]
        filename = self._makePlayerFileStr(playerGUID)
        if os.path.exists(filename):
            os.rename(filename, filename+".backup")
        
            file = open(filename, "w+")
            if file == None:
                os.rename(filename+".backup", filename)
                return -1

            cPickle.dump(playerObject, file)
            file.close()
            return 0

        print filename
        file = open(filename, "w+")
        if file == None:
            return -1
        
        cPickle.dump(playerObject, file)
        file.close()
        return 0

    #
    #
    #   
    def _insertIntoCache(self, playerGUID, playerObj):

        if self._checkCache(playerGUID) != None:
            return -1

        self.__dbcache[playerGUID] = playerObj

        return 0
    
    #
    #
    #
    def _checkCache(self, playerGUID):
        if playerGUID in self.__dbcache:
            return self.__dbcache[playerGUID]

        return None
    
    #
    #
    #
    def addPlayer(self, playerGUID, playerObject):
        
        if self._insertIntoCache(playerGUID, playerObject) < 0:
            return -1

        if self.write(playerGUID) < 0:
            return -1

        return 0
    
    #
    #
    #
    def addPlayers(self, playerList):
        for (guid, object) in playerList:
            self.addPlayer(guid, object)
    #
    #
    #
    def getPlayerHandle(self, playerGUID):

        playerObj = self._checkCache(playerGUID)

        if playerObj != None:
            return playerObj

        filename = self._makePlayerFileStr(playerGUID)
        
        if os.path.exists(filename):
            file = open(filename, "r")
            if file == None:
                return None

            playerObj = cPickle.load(file)
            file.close()

            #insert it into the cache
            self.__dbcache[playerGUID] = playerObj
            return playerObj

    #
    #flush to disk and
    #remove from the cache, 
    #TODO: make sure there are no more references to it
    def closePlayerHandle(self, playerGUID):

        if self._checkCache(playerGUID) != None:
            self.write(playerGUID)
            del(self.__dbcache[playerGUID])
            return 0

        return -1

        
gsPlayerDB = PlayerDB()

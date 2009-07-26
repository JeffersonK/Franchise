import Globals
import cPickle
import os
import glob

gsPLAYERDBLOC = "players"
gsPLAYERFILEEXT = "plr"

class ObjectDB:


    #
    #
    #
    def __init__(self, objectdbLoc, objectdbFileDxt):

        #as we read the players from disk we load them into the cache
        #we pass references to them
        self.__dbcache = {}
        self.__objectdbLoc = objectdbLoc
        self.__objectdbFileExt = objectdbFileDxt

        #make player directory
        if not os.path.exists(self.__objectdbLoc):
            os.makedirs(self.__objectdbLoc)

        return

    #
    #
    #
    def _makeObjectFileStr(self, ObjectGuid):
        return os.path.join(self.__objectdbLoc, 
                            "%s.%s" % (ObjectGuid, self.__objectdbFileExt))

    #
    #
    #
    def writeAll(self):
        for objGUID in self.__dbcache.keys():
            self.write(objGUID)
            
    #
    #
    #
    def write(self, objGUID):
        if objGUID not in self.__dbcache:
            print "write() - Inconsistency objGUID:%d not in dbcache" % objGUID
            return -1
        
        Object = self.__dbcache[objGUID]
        filename = self._makeObjectFileStr(objGUID)
        if os.path.exists(filename):
            os.rename(filename, filename+".backup")
        
            file = open(filename, "w+")
            if file == None:
                os.rename(filename+".backup", filename)
                return -1

            cPickle.dump(Object, file)
            file.close()
            return 0

        #print filename
        file = open(filename, "w+")
        if file == None:
            return -1
        
        cPickle.dump(Object, file)
        file.close()
        return 0

    #
    #
    #   
    def _insertIntoCache(self, objectGUID, Obj):

        if self._checkCache(objectGUID) != None:
            return -1

        self.__dbcache[objectGUID] = Obj

        return 0
    
    #
    #
    #
    def _checkCache(self, objectGUID):
        #print "%d %s" % (objectGUID, self.__dbcache)

        if objectGUID in self.__dbcache:
            return self.__dbcache[objectGUID]

        return None
    
    #
    #
    #
    def addObject(self, objectGUID, objectObject):
        
        if self._insertIntoCache(objectGUID, objectObject) < 0:
            return -1

        if self.write(objectGUID) < 0:
            return -1

        return 0
    
    #
    #
    #
    def addObjects(self, ObjectList):
        for (guid, object) in ObjectList:
            self.addObject(guid, object)
    #
    #
    #
    def getObjectHandle(self, ObjectGUID):

        #print "%d %s" % (ObjectGUID, self.__dbcache)

        ObjectObj = self._checkCache(ObjectGUID)

        if ObjectObj != None:
            return ObjectObj

        filename = self._makeObjectFileStr(ObjectGUID)
        
        if os.path.exists(filename):
            file = open(filename, "r")
            if file == None:
                return None

            ObjectObj = cPickle.load(file)
            file.close()

            #insert it into the cache
            self.__dbcache[ObjectGUID] = ObjectObj
            return ObjectObj

    #
    #
    #
    def getAllObjectGUIDs(self, dbLoc, objFileExt):
        #list all .xxx files in xxx/
        guidList = []
        for infile in glob.iglob(os.path.join(dbLoc, "*.%s" % objFileExt)):
            guidList += [int(infile[len(dbLoc)+1:-(len(objFileExt)+1)])]

        return guidList
    #
    #
    #for Player Objs args are ('players/', 'plr')
    def iteritems(self, dbLoc, objFileExt):
        objList = []
        guidList = self.getAllObjectGUIDs(dbLoc, objFileExt)
        
        #open all player file objects and load them into the cache
        for guid in guidList:
            obj = self.getObjectHandle(guid)
            objList += [(guid, obj)]

        return objList

    def __str__(self):
        return str(self.__dbcache)
    #
    #flush to disk and
    #remove from the cache, 
    #TODO: make sure there are no more references to it
    #def closeObjectHandle(self, ObjectGUID):
    #    
    #    if self._checkCache(ObjectGUID) != None:
    #        self.write(ObjectGUID)
    #        del(self.__dbcache[ObjectGUID])
    #        return 0
    #    return -1

        

if __name__ == '__main__':
    main()

def main():

    return

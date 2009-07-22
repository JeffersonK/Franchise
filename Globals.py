#gs = global static
gsPlayerPositions = ['P','C','1B','2B','3B','SS','LF','CF','RF']
gsBATTING_LINEUP_LENGTH = 9
gsPLAYERFREEAGENT = -1

class GlobalState:
 
    def __init__(self):
        self.__nextPlayerGUID = 0
        self.__nextFranchiseGUID = 0
        return

    def __str__(self):
        return self.__getstate__()

    def nextPlayerGUID(self):
        self.__nextPlayerGUID += 1
        return self.__nextPlayerGUID - 1
    
    def nextFranchiseGUID(self):
        self.__nextFranchiseGUID += 1
        return self.__nextFranchiseGUID - 1

    def __getstate__(self):
        
        state = "{'nextPlayerGUID':%d,'nextFranchiseGUID':%d}" % (self.__nextPlayerGUID, self.__nextFranchiseGUID)
        return state 

    def __setstate__(self, dictStr):
        print "TODO: check for eval errors when loading Global State"        
        d = eval(dictStr)
        self.__nextPlayerGUID = d['nextPlayerGUID']
        self.__nextFranchiseGUID = d['nextFranchiseGUID']

#globalState = GlobalState()

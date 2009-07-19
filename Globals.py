#gs = global static
gsPlayerPositions = ['P','C','1B','2B','3B','SS','LF','CF','RF']

#don't change this order !!! (add things to the front if they are always possible)
#gsBatterResults = ['S','2B','3B','HR','BB','SO','HBP','GO','AO','SAC','DP','TP']#,'IBB']
#gsSINGLEOUTPLAYS = ['GO','SO','AO','SAC']
#gsMULTIOUTSPLAYS = ['DP','TP']
#gsHITS = ['S','2B','3B','HR']
#gsDONTADDPITCH = ['SO','BB']
#gsMAXPITCHCOUNT = 10
#gsMAXGAMEINNINGS = 9
#gsOUTSPERINNING = 3
gsBATTING_LINEUP_LENGTH = 9
#gsBASEEMPTY = -1
gsPLAYERFREEAGENT = -1
#gsNOTATBAT = ['BB','HBP']

#can happen anytime
#['S','2B','3B','HR','BB','SO','HBP','GO','AO']
# can only happen if < 2 out & runner on base
#['SAC', 'DP']
# >= 2 people on base and 0 outs
#['TP']


class GlobalState:
 
    def __init__(self):
        self.__next_playerGUID = 0
        self.__next_franchiseGUID = 0
        return

    def __str__(self):
        return

    def nextPlayerGUID(self):
        self.__next_playerGUID += 1
        return self.__next_playerGUID - 1
    
    def nextFranchiseGUID(self):
        self.__next_franchiseGUID += 1
        return self.__next_franchiseGUID - 1


globalState = GlobalState()

from Globals import *

class Play:

    def __init__(self, batterGUID, pitcherGUID, 
                 pitchType, pitchZone, pitchSpeed, 
                 ballCount, strikeCount, earlyResultCode=None):

        #Always Passed
        self.__batterGUID = batterGUID
        self.__pitcherGUID = pitcherGUID

        self.__pitchType = pitchType
        self.__pitchZone = pitchZone
        self.__pitchSpeed = pitchSpeed
        self.__strikeCount = strikeCount
        self.__ballCount = ballCount

        #Calculated After Object Creation
        self.__where = (0,0)#where the ball was hit to: (theta, radius)
        self.__fieldersInPlay = []#None #(i.e. - 6-4-3)

        self.__runnersAdvanced = [] #[GUID:(0,1),GUID:(1,2)

        self.__runnersScored = [] #None #(i.e. guid list)

        self.__playResultEncoding = gsNULL_ATBATRESULT_CODE #same semantics as AtBatResult
        if earlyResultCode != None:
            self.__playResultEncoding = earlyResultCode
            self.createPlayEncoding()
            
        return

    def __str__(self):
        return self.__playResultEncoding

    
    #def parseResultEncoding(self, str):
    
    def createPlayEncoding(self):
        
        enc = "%s(%d,%d,%s,%d,%d,%d-%d,%s,%s,%s)" % (self.__playResultEncoding,
                                                     self.__batterGUID,
                                                     self.__pitcherGUID,
                                                     self.__pitchType,
                                                     self.__pitchZone,
                                                     self.__pitchSpeed,
                                                     self.__ballCount,
                                                     self.__strikeCount,
                                                     str(self.__where),
                                                     str(self.__fieldersInPlay), #Who
                                                     str(self.__runnersAdvanced))
        self.__playResultEncoding = enc

    def setResult(self, resultString):
        self.__playResultEncoding = resultString

    def setHitEndLocation(self, theta, r):
        self.__where = (theta, r)

    def setFieldersInPlay(self, posStr):
        self.__fieldersInPlay = [posStr]

    #TODO: Need 'set' funcs for each piece of data in the Play Encoding
    def getHitDistance(self):
        return self.__where[1] #(theta, r)

    def isFoul(self):
        return self.__playResultEncoding.startswith(gsPITCHCALL_FOUL)

    def setRunnersAdvanced(self, runnersAdvanced):
        #[(guid, start base, finish base),...]
        self.__runnersAdvanced = runnersAdvanced
        for runner in runnersAdvanced:
            (guid, start ,finish) = runner
            if finish == gsHOMEBASE:
                self.__runnersScored += [guid]

    #def setRunnersScored(self, runnersScoredList):
    #    self.__runnersScored = runnersScoredList
    def getRunnerScoredList(self):
        return self.__runnersScored

    def runsScoredOnPlay(self):
        return len(self.__runnersScored)

    def isHit(self):
        if self.isSingle() or \
                self.isDouble() or \
                self.isTriple() or \
                self.isHomeRun():
            return True
        return False

    def isSingle(self):
        return self.__playResultEncoding.startswith(gsATBATRESULT_SINGLE)

    def isDouble(self):
        return self.__playResultEncoding.startswith(gsATBATRESULT_DOUBLE)

    def isTriple(self):
        return self.__playResultEncoding.startswith(gsATBATRESULT_TRIPLE)

    def isHomeRun(self):
        return self.__playResultEncoding.startswith(gsATBATRESULT_HOMERUN)

    def isGrandSlam(self):
        if self.isHomeRun() and self.runsScoredOnPlay() == 4: #bases loaded
            return True
        return False

    def isOut(self):
        if self.__playResultEncoding.startswith(gsATBATRESULT_GROUNDOUT):
            return True
        elif self.__playResultEncoding.startswith(gsATBATRESULT_AIROUT):
            return True
        elif self.__playResultEncoding.startswith(gsATBATRESULT_SACOUT):
            return True
        elif self.__playResultEncoding.startswith(gsATBATRESULT_STRIKEOUT):
            return True
        return False

    def isStrikeOut(self):
        if self.__playResultEncoding.startswith(gsATBATRESULT_STRIKEOUT):
            return True        
        return False

    def isWalk(self):
        if self.__playResultEncoding.startswith(gsATBATRESULT_WALK):
            return True
        return False

    def isDoublePlay(self):
        return self.__playResultEncoding.startswith(gsATBATRESULT_DOUBLEPLAY)

    def isTriplePlay(self):
        return self.__playResultEncoding.startswith(gsATBATRESULT_TRIPLEPLAY)


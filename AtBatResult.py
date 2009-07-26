import random
import ProbabilityEngine as PrEng
from Globals import *
from FieldGameState import *
from PlayerStats import *

nextPitch = 0
gsPitches = None
#nextSwing = 0
#gsSwings = None

OLD = """gsBATTINGEVENTS = ['1B','2B','3B','HR','BB','SO','HBP',
                       'GO','AO','SAC','DP','TP']#,'IBB']
gsHITS = ['1B','2B','3B','HR']
gsNOTATBAT = ['BB','HBP']
#gsDONTADDPITCH = ['SO','BB']
gsSINGLEOUTPLAYS = ['GO','SO','AO','SAC']
gsMULTIOUTPLAYS = ['DP','TP']
gsOUTEVENTS = gsSINGLEOUTPLAYS + gsMULTIOUTPLAYS
gsRUNNERSADVANCEEVENTS = gsHITS + ['BB','HBP','SAC']
gsMAXPITCHCOUNT = 10"""
  

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


class BatBallContactResult:
    
    def __init__(self,
                 batterAbil=None,
                 pitcherAbil=None):
        

        #0 is first base line
        #90 is third base line
        # < 0 is foul ball
        #> 90 is foul ball
        self.__Theta = random.randint(-10,100)

        #R is Radius or distance of hit, if its in the Air
        #this is where it will land
        #if its a grandball this the power which can eventually determine error rates
        #NOTE: this will become magnitude or velocity of ball off the bat
        #      which together will determine the distance with _phi
        self.__Radius = random.randint(1,450)

        #the angle that the ball leaves the bat
        #for now 0 is a ground ball and 1 is in the air
        self.__Phi = random.randint(0,1)
                 

    def getHitParams(self):
        return (self.__Theta, self.__Phi, self.__Radius)

####
#
#
####
class AtBatResult:
    
    def __init__(self, 
                 batterGUID, batterAbil,
                 pitcherGUID, pitcherAbil,
                 fieldState): #(numOuts, numOnBase) TODO: make this a proper object
            
        self.__pitcherGUID = pitcherGUID
        self.__pitcherAbil = pitcherAbil
        self.__pitcherStats = PitcherStats(gsSTATSUBTYPE_SINGLEPLAYSTATS)
        self.__pitcherStats.addBatterFaced()

        self.__batterGUID = batterGUID
        self.__batterAbil = batterAbil
        self.__batterStats = BatterStats(gsSTATSUBTYPE_SINGLEPLAYSTATS)
        self.__batterStats.addAtBat()

        self.__fieldState = fieldState

        #we have to copy this because we are going to modify it
        self.__allowedEvents = gsCONTACTMADEEVENTS[:]#gsBATTINGEVENTS[:]

        #initialize pitch counts
        #self.__fouls = 0
        #self.__strikeCount = 0
        #self.__ballCount = 0
        #self.__totPitches = 0

        self.__contactMade = False



        #fill these in later
        self.__playObj = None
        self.__atBatEventLog = [] #list of strings
        self.__runnersOut = [] 
        #self.__runnersScored = [] #[playerGUID,]
        self.__resultCode = gsNULL_ATBATRESULT_CODE

        global gsPitches
        if gsPitches == None:
             file = open("pitch.loc", "r")
             pitches = file.readline()
             file.close()
             gsPitches = eval(pitches)

        #global gsSwings
        #if gsSwings == None:
        #    file = open("swing.loc", "r")
        #    swings = file.readline()
        #    file.close()
        #    gsSwings = eval(swings)

    def __del__(self):
        #TODO: make sure we aren't causing memory leak
        
        #don't delete these next TWO  objects because 
        #they are references from the player object
        self.__pitcherAbil = None 
        self.__batterAbil = None
        #don't delete this because it is stored in the GameState Obj
        self.__fieldState = None

        del(self.__pitcherStats)
        self.__pitcherStats = None
        del(self.__batterStats)
        self.__batterStats = None

    def __str__(self):
        s = "AtBatEvent Object(%d):" % id(self)
        s += self.__getstate__()
        return s
    
    def contactMade(self):
        return self.__contactMade

    def getPitcherStats(self):
        return self.__pitcherStats

    def getBatterStats(self):
        return self.__batterStats

    def __getstate__(self):
        s = "{'pitcherGUID':%d," +\
            "'pitcherStats':%s," +\
            "'batterGUID':%d," +\
            "'batterStats':%s," +\
            "'fieldState':%s," +\
            "'allowedEvents':%s," +\
            "'contactMade':%s," +\
            "'atBatEventLog':%s," +\
            "'runnersOut':%s," +\
            "'resultCode':%s}"

        #DEBUG
        #print type(self.__pitcherGUID)
        #print type(self.__batterGUID)
        #print type(self.__fieldState)
        #print type(self.__allowedEvents)
        #print type(self.__fouls)
        #print type(self.__strikeCount)
        #print type(self.__ballCount)
        #print type(self.__totPitches)
        #print type(self.__contactMade)
        #print type(self.__atBatEventLog)
        #print type(self.__runnersOut)
        #print type(self.__runnersScored)
        #print type(self.__resultCode)

        return s % (self.__pitcherGUID,
                    self.__pitcherStats,
                    self.__batterGUID,
                    self.__batterStats,
                    str(self.__fieldState),
                    str(self.__allowedEvents),
                    str(self.__contactMade),
                    str(self.__atBatEventLog),
                    str(self.__runnersOut),
                    self.__resultCode)

    def _logAtBatEvent(self, eventStr):
        self.__atBatEventLog += [eventStr]

    def _getNextPitch(self):
        global gsPitches
        global nextPitch
        nextPitch += 1
        
        #TODO: weight the number of balls thrown out of the strikezone according to the
        #      pitchers control

        #TODO: weight the pitchtype and pitchzone according to the pitchers strengths
        r = random.randint(0,len(gsPITCHTYPES)-1)
        return (gsPITCHTYPES[r], gsPitches[nextPitch])

    #def _getNextSwing(self):
    #    global gsSwings
    #    global nextSwing
    #    print gsSwings[nextSwing]
    #    nextSwing += 1
    #    return gsSwings[nextSwing]

    def simPitch(self, pitcherAbil=None, batterAbil=None, pitch=None):

        if pitcherAbil == None:
            pitcherAbil = self.__pitcherAbil
        
        if batterAbil == None:
            batterAbil = self.__batterAbil

        pitchType = None
        pitchZone = -1
        
        if pitch == None:
            (pitchType, pitchZone) = self._getNextPitch()
        else:
            (pitchType, pitchZone) = pitch
        
        if pitchZone not in gsSTRIKEZONE:
            #the pitch is in the strike zone

            #TODO: calculate batter pateince to see if he swings at this pitch
            #if (batter swings) :
            #   => it's a strike

            #TODO: base on pitchers control decide whether or not he hit the batter
            # if gsATBATRESULT_HITBYPITCH

            if self.__pitcherStats.getBalls() == gsMAXBALLCOUNT-1:
                #TODO: need to check to see if runs score and generate a Play()
                playObj = Play(self.__batterGUID, self.__pitcherGUID,
                               pitchType, pitchZone, 0, 
                               self.__pitcherStats.getBalls(), 
                               self.__pitcherStats.getStrikes(), 
                               gsATBATRESULT_WALK) #earlyResultCode

                bases = self.__fieldState.getBasesState()
                runnersAdvancedList = bases.simBaseRunners(gsATBATRESULT_WALK)
                playObj.setResult(gsATBATRESULT_WALK)
                playObj.setRunnersAdvanced(runnersAdvancedList)
                self.__resultCode = str(playObj)                
                
                #TODO: need to use fieldState to determine who 
                #      scored and set appropriately
                #      in the playObj because in the case of a WALK/HBP runs can
                #      score without a ball being in play
                self.__batterStats.addPitchReceived(pitchType, pitchZone, 0, gsPITCHCALL_WALK, playObj)
                self.__pitcherStats.addPitchThrown(pitchType, pitchZone, 0, gsPITCHCALL_WALK, playObj)

                self.__playObj = playObj
                return gsPITCHCALL_WALK

            else:
                #this addPitchReceived does nothing for now 
                #because we don't track
                #individual pitches for batters
                self.__pitcherStats.addPitchThrown(pitchType, pitchZone, 0, gsPITCHCALL_BALL)
                self.__batterStats.addPitchReceived(pitchType, pitchZone, 0, gsPITCHCALL_BALL, 0)
                return gsPITCHCALL_BALL

        #else:
        #it's in the strike zone
        #we always swing this call get the probability that the
        #batter makes contact
        pr = PrEng.PrContact(pitcherAbil, 
                             batterAbil,
                             (pitchType, pitchZone))

        #using the probability of contact we then
        #do our monte carlo simulation to determine
        #if the ball is actually hit
        r = random.randint(0,999)
        if r <= (pr * 1000):
            #fuckin' contact!
            self.__contactMade = True
            playObj = Play(self.__batterGUID, self.__pitcherGUID,
                           pitchType, pitchZone, 0, 
                           self.__pitcherStats.getBalls(), 
                           self.__pitcherStats.getStrikes())
            self.simBallInPlay(playObj)

            if playObj.isFoul():#.startswith(gsPITCHCALL_FOUL):
                self.__contactMade = False
                self.__pitcherStats.addPitchThrown(pitchType, pitchZone, 0, gsPITCHCALL_FOUL)
                self.__batterStats.addPitchReceived(pitchType, pitchZone, 0, 0, gsPITCHCALL_FOUL)
                self.__resultCode = gsNULL_ATBATRESULT_CODE

                self.__playObj = playObj
            else:
                playObj.createPlayEncoding()
                self.__resultCode = str(playObj)
                self.__pitcherStats.addPitchThrown(pitchType, pitchZone, 0, None, playObj)                
                self.__batterStats.addPitchReceived(pitchType, pitchZone, 0, None, 0, playObj)                

                self.__playObj = playObj

                return gsPITCHCALL_CONTACT

        #else:
        #he whiff'd!
        if self.__pitcherStats.getStrikes() == gsMAXSTRIKECOUNT-1:
            #it's a strikeout
            playObj = Play(self.__batterGUID, self.__pitcherGUID,
                           pitchType, pitchZone, 0, 
                           self.__pitcherStats.getBalls(), 
                           self.__pitcherStats.getStrikes(),
                           gsATBATRESULT_STRIKEOUT) #earlyResultCode

            self.__fieldState.incOuts(1)
            playObj.setResult(gsATBATRESULT_STRIKEOUT)
            playObj.setRunnersAdvanced([])
            self.__resultCode = str(playObj)                

            self.__pitcherStats.addPitchThrown(pitchType, pitchZone, 0, gsPITCHCALL_STRIKEOUT, playObj)
            self.__batterStats.addPitchReceived(pitchType, pitchZone, 0, gsPITCHCALL_STRIKEOUT, 0, playObj)

            self.__playObj = playObj
            return gsPITCHCALL_STRIKEOUT
        else:
            #its just a strike
            self.__pitcherStats.addPitchThrown(pitchType, pitchZone, 0, gsPITCHCALL_STRIKE)
            self.__batterStats.addPitchReceived(pitchType, pitchZone, 0, gsPITCHCALL_STRIKE, 0)
            return gsPITCHCALL_STRIKE

    #########
    #
    #
    #
    #
    #########
    def _startSimAtBat(self):
        return

    def _endSimAtBat(self, ret):
        return ret
    
    def simAtBat(self, pitcherAbil=None, batterAbil=None, pitch=None):

        self._startSimAtBat()
            
        if pitcherAbil == None:
            pitcherAbil = self.__pitcherAbil
        
        if batterAbil == None:
            batterAbil = self.__batterAbil

        ret = ""
        while 1:
            ret = self.simPitch(pitcherAbil, batterAbil, pitch)
            if ret == gsPITCHCALL_FOUL:
                continue
            if ret != gsPITCHCALL_BALL and  ret != gsPITCHCALL_STRIKE: #or FOUL
                return self._endSimAtBat(ret)

        return self._endSimAtBat(ret)

    ########################
    #heart of simulation code
    #needs to simluate the physics of the bat hitting the ball to determine its trajectory
    #and use inconjunction with the player abilities in the field and the players abilities
    #on base to determine how the play is fielded and who advances on base
    #the playObj is fully described in the playObj which is modified as it is passed
    ########################
    def simBallInPlay(self, playObj):
        #def _generateAtBatResult(self):
        self._findAllowedEvents()
        
        bbcr = BatBallContactResult()
        fieldState = self.__fieldState#DefensiveFieldState()#self.__bases, self.__outs)#FieldGeometry, None)
        ((result, fielder, radius), runnersAdvancedList) = fieldState.simDefense(bbcr)#FieldBallContact(bbcr)
        #print bbcr.getHitParams()
        #print "%s %s %d" % (result, fielder, r)
        playObj.setFieldersInPlay(fielder)
        playObj.setHitEndLocation(0, radius)
        playObj.setResult(result)
        playObj.setRunnersAdvanced(runnersAdvancedList)

        self.__play = playObj

        self.__resultCode = str(playObj)

        
    def _safeRemoveEvent(self, list, eventStr):
        if eventStr in list:
            list.remove(eventStr)

    def _findAllowedEvents(self):
        (numOuts, numOnBase) = self.__fieldState.getStateOutsAndOnBase()

        #allowedEvents = self.gsBATTINGEVENTS[:]
        if numOuts == 2 or numOnBase == 0:
            self._safeRemoveEvent(self.__allowedEvents, gsATBATRESULT_SACOUT)
            self._safeRemoveEvent(self.__allowedEvents, gsATBATRESULT_DOUBLEPLAY)
            self._safeRemoveEvent(self.__allowedEvents, gsATBATRESULT_TRIPLEPLAY)
            
        elif numOuts <= 1 and numOnBase > 0:
            if numOuts == 0 and numOnBase >= 2:
                #allowedEvents = allowedEvents
                None
            else:
                self._safeRemoveEvent(self.__allowedEvents, gsATBATRESULT_SACOUT)
                self._safeRemoveEvent(self.__allowedEvents, gsATBATRESULT_TRIPLEPLAY)
        
        if self.__contactMade:
            self._safeRemoveEvent(self.__allowedEvents, gsATBATRESULT_HITBYPITCH)

        return

 
    def logAtBatEvent(self, eventStr):
        self.__atBatEventLog += [eventStr]

    def atBatEventLog(self):
        return self.__atBatEventLog

    def isOut(self):
        x = [outevent for outevent in gsOUTEVENTS if self.__resultCode.startswith(outevent)] 
        return len(x) != 0#self.__resultCode in gsOUTEVENTS

    def outsMade(self):
        x = [outevent for outevent in gsSINGLEOUTPLAYS if self.__resultCode.startswith(outevent)] 
        #if self.__resultCode in gsSINGLEOUTPLAYS:
        if len(x) != 0:
            return 1

        if self.DoublePlay():
            return 2

        if self.TriplePlay():
            return 3

        return 0

    def countsAsAtBat(self):
        x = [event for event in gsNOTATBAT if self.__resultCode.startswith(event)] 
        return len(x) > 0
        #return self.__resultCode not in gsNOTATBAT

    def runsScored(self):
        return len(self.__runnersScored)

    def runnersAdvance(self):
        x = [event for event in gsRUNNERSADVANCEEVENTS if self.__resultCode.startswith(event)] 
        return len(x) > 0

    def Single(self):
        return self.__resultCode.startswith(gsATBATRESULT_SINGLE)

    def isHit(self):
        x = [event for event in gsHITS if self.__resultCode.startswith(event)]
        return len(x) != 0 #self.__resultCode in gsHITS

    def Double(self):
        return self.__resultCode.startswith(gsATBATRESULT_DOUBLE)

    def Triple(self):
        return self.__resultCode.startswith(gsATBATRESULT_TRIPLE)

    def HomeRun(self):
        return self.__resultCode.startswith(gsATBATRESULT_HOMERUN)

    def Walk(self):
        return self.__resultCode.startswith(gsATBATRESULT_WALK)

    def HitByPitch(self):
        return self.__resultCode.startswith(gsATBATRESULT_HITBYPITCH)

    def StrikeOut(self):
        return self.__resultCode.startswith(gsATBATRESULT_STRIKEOUT)

    def GroundOut(self):
        return self.__resultCode.startswith(gsATBATRESULT_GROUNDOUT)

    def FlyOut(self):
        return self.__resultCode.startswith(gsATBATRESULT_AIROUT)

    def SacrificeOut(self):
        return self.__resultCode.startswith(gsATBATRESULT_SACOUT)

    def DoublePlay(self):
        return self.__resultCode.startswith(gsATBATRESULT_DOUBLEPLAY)

    def TriplePlay(self):
        return self.__resultCode.startswith(gsATBATRESULT_TRIPLEPLAY)

    def teamScored(self):        
        if self.__playObj == None:
            return False

        return self.__playObj.runsScoredOnPlay() > 0

    #DEPRECATED
    #def setRunnersScored(self, runnerGUIDList):
    #    self.__runnersScored = runnerGUIDList

    def getRunnersScored(self):
        return self.__playObj.getRunnerScoredList()

    def getResultCode(self):
        return self.__resultCode

    def getPitcherGUID(self):
        return self.__pitcherGUID

    def getBatterGUID(self):
        return self.__batterGUID

    #def getPitchCounts(self):
    #    return (self.__totPitches, self.__strikeCount + self.__fouls, self.__ballCount)

    old = """def _OLDgenerateAtBatResult(self):
        self._findAllowedEvents()

        if self.__ballCount == 4:
            self.__resultCode = 'BB'
            return

        if self.__strikeCount == 3:
            self.__resultCode = 'SO'
            return
        
        random.seed()
        r = random.randint(0,len(self.__allowedEvents)-1)
        self.__resultCode = self.__allowedEvents[r]

        #if self__resultCode == 'HR':
        #TODO: populate event log for different kinds of events    
        return"""

    
    old = """def RANDOMLYgeneratePitchCount(self):

        #generate pitches
        if self.__resultCode == 'SO':
            self.__strikeCount = 3     
            self.__ballCount = random.randint(0,3)

        elif self.__resultCode == 'BB':
            self.__strikeCount = random.randint(0,2)     
            self.__ballCount = 4
            
        else:
            self.__strikeCount = random.randint(0,2)     
            self.__ballCount = random.randint(0,3)     

        if self.__strikeCount >= 2:
            self.__fouls = random.randint(self.__ballCount + self.__strikeCount,
                                          gsMAXPITCHCOUNT)
            self.__totPitches = self.__ballCount + self.__strikeCount + self.__fouls
        else:
            self.__totPitches = self.__ballCount + self.__strikeCount
            
        if self.__resultCode == 'HBP':
            self.__ballCount += 1

        if self.__resultCode not in gsDONTADDPITCH:
            self.__totPitches += 1

        return """

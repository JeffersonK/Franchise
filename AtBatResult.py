import random
import ProbabilityEngine as PrEng
from Globals import *
from FieldGameState import *

nextPitch = 0
gsPitches = None
#nextSwing = 0
#gsSwings = None

gsBATTINGEVENTS = ['1B','2B','3B','HR','BB','SO','HBP',
                       'GO','AO','SAC','DP','TP']#,'IBB']
gsHITS = ['1B','2B','3B','HR']
gsNOTATBAT = ['BB','HBP']
#gsDONTADDPITCH = ['SO','BB']
gsSINGLEOUTPLAYS = ['GO','SO','AO','SAC']
gsMULTIOUTPLAYS = ['DP','TP']
gsOUTEVENTS = gsSINGLEOUTPLAYS + gsMULTIOUTPLAYS
gsRUNNERSADVANCEEVENTS = gsHITS + ['BB','HBP','SAC']
gsMAXPITCHCOUNT = 10
  
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
                 batterGUID,batterAbil,
                 pitcherGUID, pitcherAbil,
                 currentState): #(numOuts, numOnBase)
            
        self.__pitcher_playerGUID = pitcherGUID
        self.__pitcherAbil = pitcherAbil
        
        self.__batter_playerGUID = batterGUID
        self.__batterAbil = batterAbil
        
        self.__currentState = currentState

        #we have to copy this because we are going to modify it
        self.__allowedEvents = gsBATTINGEVENTS[:]

        #initialize pitch counts
        self.__fouls = 0
        self.__strikeCount = 0
        self.__ballCount = 0
        self.__totPitches = 0

        self.__contactMade = False

        #fill these in later
        self.__atBatEventLog = [] #list of strings
        self.__runnersOut = [] 
        self.__runnersScored = [] #[playerGUID,]
        self.__resultCode = ""

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

    def _logAtBatEvent(self, eventStr):
        self.__atBatEventLog += [eventStr]

    def _getNextPitch(self):
        global gsPitches
        global nextPitch
        #print gsPitches[nextPitch]
        nextPitch += 1
        return ('fastball', gsPitches[nextPitch])

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
            
        self.__totPitches += 1
            
        if pitchZone not in gsSTRIKEZONE:
            self.__ballCount += 1
            
            if self.__ballCount == 4:
                self.__resultCode = 'BB'
                #self._logAtBatEvent("%d is walked." % self.__playerGUID)
                return 'BB'  
            else:
                return 'BALL'

        else:
            pr = PrEng.PrContact(pitcherAbil, 
                                 batterAbil,
                                 (pitchType, pitchZone))

        r = random.randint(0,999)
        if r <= (pr * 1000):
            #fuckin' contact!
            self.__contactMade = True
            #self.__resultCode = 'HR'
            self._generateAtBatResult()
            if self.__resultCode.startswith('FOUL'):
                if self.__strikeCount < 2:
                    self.__strikeCount += 1
                    self.__resultCode = ""
            else:
                return 'CONTACT'

        #else:
        #he whiff'd!
        self.__strikeCount += 1
            
        if self.__strikeCount == 3:
            self.__resultCode = 'SO'
            #self._logAtBatEvent("%d goes down swinging." % self.__batter_playerGUID)
            return 'SO'
        else:
            return 'STRIKE'

    def simAtBat(self, pitcherAbil=None, batterAbil=None, pitch=None):
        if pitcherAbil == None:
            pitcherAbil = self.__pitcherAbil
        
        if batterAbil == None:
            batterAbil = self.__batterAbil
        
        while 1:
            ret = self.simPitch(pitcherAbil, batterAbil, pitch)
            if ret == 'FOUL':
                continue
            if ret != 'BALL' and  ret != 'STRIKE': #or FOUL
                return ret
        return

    def _simAtBat(self):
        #TODO: handle fouls and HBP
        while 1:            
            pitch = self._getNextPitch()
            self.__totPitches += 1

            swing = self._getNextSwing()

            if pitch == 0 and swing in range(0,5):
                #or HBP
                self.__ballCount += 1
            
            elif pitch == 0 and swing != 0:
                self.__strikeCount += 1  
            
            elif pitch == swing:
             #contact
                self._OLDgenerateAtBatResult()
                return

            else:
                self.__strikeCount += 1

            if self.__strikeCount == 3:
                self.__resultCode = 'SO'
                return

            if self.__ballCount == 4:
                self.__resultCode = 'BB'
                return
            
        return

    def _safeRemoveEvent(self, list, eventStr):
        if eventStr in list:
            list.remove(eventStr)

    def _findAllowedEvents(self):
        (numOuts, numOnBase) = self.__currentState

        #allowedEvents = self.gsBATTINGEVENTS[:]
        if numOuts == 2 or numOnBase == 0:
            self._safeRemoveEvent(self.__allowedEvents, 'SAC')
            self._safeRemoveEvent(self.__allowedEvents, 'DP')
            self._safeRemoveEvent(self.__allowedEvents, 'TP')
            
        elif numOuts <= 1 and numOnBase > 0:
            if numOuts == 0 and numOnBase >= 2:
                #allowedEvents = allowedEvents
                None
            else:
                self._safeRemoveEvent(self.__allowedEvents, 'SAC')
                self._safeRemoveEvent(self.__allowedEvents, 'TP')

        if self.__strikeCount < 3:
            self._safeRemoveEvent(self.__allowedEvents, 'SO')

        if self.__ballCount < 4:
            self._safeRemoveEvent(self.__allowedEvents, 'BB')
        
        if self.__contactMade:
            self._safeRemoveEvent(self.__allowedEvents, 'HBP')

        return

    def _generateAtBatResult(self):
        self._findAllowedEvents()

        bbcr = BatBallContactResult()
        fieldState = DefensiveFieldState()#self.__bases, self.__outs)#FieldGeometry, None)
        result = fieldState.simFieldBallContact(bbcr)
        #print bbcr.getHitParams()
        self.__resultCode = result

 
    
    def __str__(self):
        return "%d - %s" % ( self.__batter_playerGUID, self.__resultCode)


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

    def teamScored(self):
        return len(self.__runnersScored) > 0

    def Single(self):
        return self.__resultCode.startswith('1B')

    def isHit(self):
        x = [event for event in gsHITS if self.__resultCode.startswith(event)]
        return len(x) != 0 #self.__resultCode in gsHITS

    def Double(self):
        return self.__resultCode.startswith('2B')

    def Triple(self):
        return self.__resultCode.startswith('3B')

    def HomeRun(self):
        return self.__resultCode.startswith('HR')

    def Walk(self):
        return self.__resultCode.startswith('BB')

    def HitByPitch(self):
        return self.__resultCode.startswith('HBP')

    def StrikeOut(self):
        return self.__resultCode.startswith('SO')

    def GroundOut(self):
        return self.__resultCode.startswith('GO')

    def FlyOut(self):
        return self.__resultCode.startswith('AO')

    def SacrificeOut(self):
        return self.__resultCode.startswith('SAC')

    def DoublePlay(self):
        return self.__resultCode.startswith('DP')

    def TriplePlay(self):
        return self.__resultCode.startswith('TP')

    def setRunnersScored(self, runnerGUIDList):
        self.__runnersScored = runnerGUIDList

    def getRunnersScored(self):
        return self.__runnersScored

    def getResultCode(self):
        return self.__resultCode

    def getPitcherGUID(self):
        return self.__pitcher_playerGUID

    def getBatterGUID(self):
        return self.__batter_playerGUID

    def getPitchCounts(self):
        return (self.__totPitches, self.__strikeCount + self.__fouls, self.__ballCount)

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

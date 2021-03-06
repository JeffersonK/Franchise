from Globals import *
from PointLine import *

LOC_P = (45.0, 60.5)
LOC_C = (45.0, -5)
LOC_1B = (85.0, 115)
LOC_2B = (60.5, 145)
LOC_3B = (5, 115)
LOC_SS = (33.0, 145)
LOC_LF = (22.5, 250)
LOC_CF = (45.0, 250)
LOC_RF = (77.5, 250)
gsDEFAULT_PLAYER_LOCS = [LOC_P, LOC_C, LOC_1B, 
                         LOC_2B, LOC_3B, LOC_SS, 
                         LOC_LF, LOC_CF, LOC_RF]

gsTHETA_LEFTFIELD_FOULPOLE = 0
gsTHETA_RIGHTFIELD_FOULPOLE = 90
gsRADIUS_OUTFIELD_WALL = 410
gsTHETA_FOUL_RANGE = 10

#Simple Defensive Model for infielder ranges 
gsTHETA_THIRDBASERANGE = range(1,10)
gsTHETA_SSRANGE = range(25,38)
gsTHETA_SECONDBASERANGE = range(45, 58)
gsTHETA_FIRSTBASERANGE = range(80, 90)

gsMAXINFIELDRADIUS = 155
gsOUTFIELDSHALLOW = 280
gsOUTFIELDERMAXRADIUS = 340
gsOUTFIELDDOUBLE = gsRADIUS_OUTFIELD_WALL#410#385
#gsOUTFIELDTRIPLE = 400

#class FieldGeometry:
#    def __init__(self):
#        self.__radiusInfieldEdge = gsMAXINFIELDRADIUS
#        self.__radiusOutfieldWall = [(gsTHETA_LEFTFIELD_FOULPOLE, gsTHETA_RIGHTFIELD_FOULPOLE, gsRADIUS_OUTFIELD_WALL)]


DEBUG_FIELDGAMESTATE = 0

#if we want a more accurate simulation of how runners advance
#should be dependent on where the ball is hit who is fielding the
#ball and the abilities of the runners. We will simulate this later
#
class BasesState:

    ########
    #
    #
    #arguments are playerGUIDs
    ########
    def __init__(self, atBat=gsBASEEMPTY, onFirst=gsBASEEMPTY, 
                 onSecond=gsBASEEMPTY, onThird=gsBASEEMPTY):
        
        #self.__runnerAbilities = None
        self.__bases = [atBat, onFirst, onSecond, onThird]
        return

    def numOnBase(self):
        numOn = 0
        if self.__bases[gsFIRSTBASE] != gsBASEEMPTY:
            numOn += 1

        if self.__bases[gsSECONDBASE] != gsBASEEMPTY:
            numOn += 1

        if self.__bases[gsTHIRDBASE] != gsBASEEMPTY:
            numOn += 1

        return numOn

    def playerOn(self, n):
        return self.__bases[n]


    def manOn(self, n):
        if n < 0 or n > 3:
            print "DEBUG: Bad Argument passed to manOn()"
            return None

        if self.__bases[n] == gsBASEEMPTY:
            return False
        
        return True

    def setBatterGUID(self, batterGUID):
        self.__bases[gsHOMEBASE] = batterGUID

    def clearBases(self):
        self.__bases = [gsBASEEMPTY] * 4

    def simBaseRunners(self, ABRCode):
        runnersAdvanced = []
        runnersScored = []
        basesReversed = self.__bases[:]
        basesReversed.reverse()

        if ABRCode == gsATBATRESULT_SINGLE:#atBatResultObj.Single():

            i = 0
            while(i < 4):
                if self.__bases[i] != gsBASEEMPTY:
                    runnersAdvanced += [(self.__bases[i],i,(i+1)%4)]
                i += 1

            runnersScored = [basesReversed[0]]
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY] + self.__bases[0:3]
            
        elif ABRCode == gsATBATRESULT_DOUBLE:

            i = 0
            while(i < 4):
                if self.__bases[i] != gsBASEEMPTY:
                    if i > 1:
                        runnersAdvanced += [(self.__bases[i],i,0)]
                    else:
                        runnersAdvanced += [(self.__bases[i],i,(i+2)%4)]
                i += 1

            runnersScored = basesReversed[0:2]
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY]*2 + self.__bases[0:2]

            
        elif ABRCode == gsATBATRESULT_TRIPLE:
            i = 0
            while(i < 4):
                if self.__bases[i] != gsBASEEMPTY:
                    if i > 0:
                        runnersAdvanced += [(self.__bases[i],i,0)]
                    else:
                        runnersAdvanced += [(self.__bases[i],i,(i+3)%4)]
                i += 1

            runnersScored = basesReversed[0:3]
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY]*3 + [self.__bases[0]]

        elif ABRCode == gsATBATRESULT_HOMERUN:

            i = 0
            while(i < 4):
                if self.__bases[i] != gsBASEEMPTY:
                    runnersAdvanced += [(self.__bases[i],i,0)]
                i += 1
            
            runnersScored = basesReversed
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY]*4

        elif ABRCode == gsATBATRESULT_WALK:
            
            i = 1
            runnersAdvanced += [(self.__bases[0], 0, 1)]
            stopAdvancing = False
            while(i <= 3):
                if self.__bases[i] == gsBASEEMPTY:
                    #stop if a base is empty
                    stopAdvancing = True                
                else:
                    if not stopAdvancing:
                        runnersAdvanced += [(self.__bases[i],i,(i+1)%4)]
                    else:
                        runnersAdvanced += [(self.__bases[i],i,i)]
                i += 1
                    
            if not self.manOn(1):

                self.__bases[1] = self.__bases[0]
                self.__bases[0] = gsBASEEMPTY

            elif self.manOn(1) and not self.manOn(2):
                self.__bases[2] = self.__bases[1]
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = gsBASEEMPTY

            elif self.manOn(1) and self.manOn(2) and not self.manOn(3):
                self.__bases[3] = self.__bases[2]
                self.__bases[2] = self.__bases[1]
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = gsBASEEMPTY

            elif self.manOn(1) and self.manOn(2) and self.manOn(3):
                runnersScored = [self.__bases[3]]
                self.__bases = [gsBASEEMPTY] + self.__bases[0:3]

            else:
                print "DEBUG: Hit Default Case in _handleAdvanceAllRunners()\n"

        elif ABRCode == gsATBATRESULT_SACOUT:

            #TODO: runnersAdvanced
            runnersScored = [basesReversed[0]]
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY]*2 + self.__bases[1:3]

        
        elif ABRCode == gsATBATRESULT_STRIKEOUT or\
                ABRCode == gsATBATRESULT_GROUNDOUT or \
                ABRCode == gsATBATRESULT_AIROUT:
            
            #return set of tuples that indicate that the runners did not move
            i = 1
            for runner in self.__bases[1:]:
                if runner != gsBASEEMPTY:
                    runnersAdvanced += [(runner, i, i)]
                i += 1
        
        return runnersAdvanced #list of runners and how they advanced

#holds position and locations of base runners
#as well as the abilities of players at those positions
class DefensiveFieldState:

    def __init__(self, basesState=None, outCount=0):
        #FieldGeometry=None, PlayerFielderAbilities=None):

        self.__basesState = basesState
        if basesState == None:
            self.__basesState = BasesState()

        self.__outs = outCount
        
        #contains information about the trajectory of the hit
        #of the hit
        #self.__batBallContactResult = None (this will get passed in)
        
        #self.__batterAtBatScoring = None

        #information about the geometry of the field so we know 
        #if the ball is hit out of the park or not
        #self.__fieldGeometry = None

        #abilities of players in the field by GUID
        #self.__playersFielders = PlayerFielderAbilities

        #coordinates for where the players are in the field
        #self.__playersFieldCoordinates = None
        
    def getStateOutsAndOnBase(self):
        return (self.__outs, self.__basesState.numOnBase())

    def incOuts(self, n=1):
        self.__outs += n

    def getNumOuts(self):
        return self.__outs

    def playerOn(self, n):
        return self.__basesState.playerOn(n)

    def numRunnersInScoringPos(self):
        cnt = 0
        if self.__basesState.manOn(2):
            cnt += 1
        
        if self.__basesState.manOn(3):
            cnt += 1
        
        return cnt

    def reset(self):
        self.__basesState.clearBases()
        self.__outs = 0

    def setBatterGUID(self, batterGUID):
        self.__basesState.setBatterGUID(batterGUID)

    def getInfieldLoc(self, theta, radius):
        if radius < 20:
            return gsCATCHER_POSCODE #gsPOSITION_POSSTR[gsCATCHER_POSCODE]

        if radius < 100:
            return gsPITCHER_POSCODE #gsPOSITION_POSSTR[gsPITCHER_POSCODE]
            #return 'P'

        if theta < min(gsTHETA_THIRDBASERANGE):#up the 3rd base line
            return gsTHIRDBASE_POSCODE#gsPOSITION_POSSTR[gsTHIRDBASE_POSCODE]       
            #return '3B'
        
        if theta in gsTHETA_THIRDBASERANGE:
            return gsTHIRDBASE_POSCODE#gsPOSITION_POSSTR[gsTHIRDBASE_POSCODE]       
            #return '3B'
        
        if theta < min(gsTHETA_SSRANGE):
            return gsSHORTSTOP_POSCODE#gsPOSITION_POSSTR[gsSHORTSTOP_POSCODE]       
            #return 'SS'
        
        if theta in gsTHETA_SSRANGE:
            return gsSHORTSTOP_POSCODE#gsPOSITION_POSSTR[gsSHORTSTOP_POSCODE]       
            #return 'SS'
        
        if theta < min(gsTHETA_SECONDBASERANGE):
            return gsSECONDBASE_POSCODE#gsPOSITION_POSSTR[gsSECONDBASE_POSCODE]       
            #return '2B'
        
        if theta in gsTHETA_SECONDBASERANGE:
            return gsSECONDBASE_POSCODE#gsPOSITION_POSSTR[gsSECONDBASE_POSCODE]       
            #return '2B'
        
        if theta < min(gsTHETA_FIRSTBASERANGE):
            return gsFIRSTBASE_POSCODE#gsPOSITION_POSSTR[gsFIRSTBASE_POSCODE]       
            #return '1B'
        
        if theta in gsTHETA_FIRSTBASERANGE:
            return gsFIRSTBASE_POSCODE#gsPOSITION_POSSTR[gsFIRSTBASE_POSCODE]       
            #return '1B'
        
        if theta <= gsTHETA_RIGHTFIELD_FOULPOLE:
            return gsFIRSTBASE_POSCODE#gsPOSITION_POSSTR[gsFIRSTBASE_POSCODE]       
            #return '1B'

    def isChangeSides(self):
        return self.__outs == gsOUTSPERINNING

    def getFieldLocModifier(self, radius):
        #thetaLoc = ''
        #descriptor = '' #deep, shallow
        #if radius < gsINFIELDMAXRADIUS:
        #    return 'INF'
        #if radius < gs
        return radius#"%s" % radius

    def getOutfieldLoc(self, theta):
        if theta < 33:
            return gsLEFTFIELDER_POSCODE#gsPOSITION_POSSTR[gsLEFTFIELDER_POSCODE]       
            #return 'LF'
        if theta < 66:
            return gsCENTERFIELDER_POSCODE#gsPOSITION_POSSTR[gsCENTERFIELDER_POSCODE]       
            #return 'CF'
        if theta <= 90:
            return gsRIGHTFIELDER_POSCODE#gsPOSITION_POSSTR[gsRIGHTFIELDER_POSCODE]       
            #return 'RF'
    
    def getBasesState(self):
        return self.__basesState

    def _testNewAlgorithm(self, theta, phi, radius):

        if DEBUG_FIELDGAMESTATE:
            print "\n === NEW HIT ==="
        i = 1
        playMade = False
        playerRange = 25.0

        for plyr in gsDEFAULT_PLAYER_LOCS:
            playMade = False
            minDist = 500.0
            if phi == 0:#its on the ground
                (onLineSeg, minDist) = PointLineIntersect((theta, radius), plyr)
                if minDist < playerRange:
                    playMade = True
                    if DEBUG_FIELDGAMESTATE:
                        print "--- %s MADE PLAY ---" % gsPOSITION_POSSTR[i]

            elif phi > 0:
                minDist = distance((theta, radius), plyr)
                if minDist < playerRange:
                    playMade = True
                    if DEBUG_FIELDGAMESTATE:
                        print "--- %s MADE PLAY ---" % gsPOSITION_POSSTR[i]

            if DEBUG_FIELDGAMESTATE:
                print "HIT LOC: %d %d %d" % (theta, phi, radius)
                print "%s(%f) within %f " % (gsPOSITION_POSSTR[i], playerRange,
                                                 minDist)
            i += 1

        return

    def simDefense(self, batBallContactResultOverride=None):

        batBallContactResult = None#self.__batBallContactResult
        if batBallContactResultOverride != None:
            batBallContactResult = batBallContactResultOverride
            
        (theta, phi, radius) = batBallContactResult.getHitParams()

        
        #TESTING
        self._testNewAlgorithm(theta, phi, radius)
        

        if theta < gsTHETA_LEFTFIELD_FOULPOLE or theta > gsTHETA_RIGHTFIELD_FOULPOLE:
            result = gsPITCHCALL_FOUL
            return ((gsPITCHCALL_FOUL, None, radius), [])

        result = ""

        if phi:
            #its in the air
            if radius < gsMAXINFIELDRADIUS:
                result = (gsATBATRESULT_AIROUT, self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                self.__outs += 1

            elif radius < gsOUTFIELDSHALLOW:
                result = (gsATBATRESULT_SINGLE, self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))

            elif radius < gsOUTFIELDERMAXRADIUS:
                result = (gsATBATRESULT_AIROUT, self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
                self.__outs += 1

            elif radius < gsOUTFIELDDOUBLE:
                result = (gsATBATRESULT_DOUBLE, self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
            
            #elif radius < gsOUTFIELDTRIPLE:
            #    return '3B(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))

            else:
                result = (gsATBATRESULT_HOMERUN, self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
        else:
            #its a ground ball
            if radius < gsMAXINFIELDRADIUS:
                result = (gsATBATRESULT_GROUNDOUT, self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                self.__outs += 1

            elif theta < min(gsTHETA_THIRDBASERANGE):#up the 3rd base line
                result = (gsATBATRESULT_TRIPLE, self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))

            elif theta in gsTHETA_THIRDBASERANGE:
                result = (gsATBATRESULT_GROUNDOUT, self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                self.__outs += 1
            
            elif theta < min(gsTHETA_SSRANGE):
                result = (gsATBATRESULT_SINGLE, self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))

            elif theta in gsTHETA_SSRANGE:
                result = (gsATBATRESULT_GROUNDOUT, self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                self.__outs += 1

            elif theta < min(gsTHETA_SECONDBASERANGE):
                result = (gsATBATRESULT_SINGLE, self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))

            elif theta in gsTHETA_SECONDBASERANGE:
                result = (gsATBATRESULT_GROUNDOUT, self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                self.__outs += 1

            elif theta < min(gsTHETA_FIRSTBASERANGE):
                result = (gsATBATRESULT_SINGLE, self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))

            elif theta in gsTHETA_FIRSTBASERANGE:
                result =(gsATBATRESULT_GROUNDOUT, self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                self.__outs += 1
            
            elif theta <= gsTHETA_RIGHTFIELD_FOULPOLE:               
                result = (gsATBATRESULT_TRIPLE, self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))

            else:
                print "unmatched case in simFieldBallContact"

            #needed by advanceRunners()
        runnersScored = self.__basesState.simBaseRunners(result[0])
        if DEBUG_FIELDGAMESTATE:
            print result
        return (result, runnersScored)#result

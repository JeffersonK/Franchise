from Globals import *


gsTHETA_LEFTFIELD_FOULPOLE = 0
gsTHETA_RIGHTFIELD_FOULPOLE = 90
gsRADIUS_OUTFIELD_WALL = 400

#Simple Defensive Model for infielder ranges 
gsTHETA_THIRDBASERANGE = range(2,15)
gsTHETA_SSRANGE = range(20,41)
gsTHETA_SECONDBASERANGE = range(46, 61)
gsTHETA_FIRSTBASERANGE = range(71, 82)

gsMAXINFIELDRADIUS = 155
gsOUTFIELDSHALLOW = 225
gsOUTFIELDERMAXRADIUS = 350
gsOUTFIELDDOUBLE = 400#385
#gsOUTFIELDTRIPLE = 400
class FieldGeometry:

    def __init__(self):
        self.__radiusInfieldEdge = gsMAXINFIELDRADIUS
        self.__radiusOutfieldWall = [(gsTHETA_LEFTFIELD_FOULPOLE, gsTHETA_RIGHTFIELD_FOULPOLE, gsRADIUS_OUTFIELD_WALL)]



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


    def _manOn(self, n):
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


            
        elif ABRCode == gsATBATRESULT_DOUBLE:#atBatResultObj.Double():

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

            
        elif ABRCode == gsATBATRESULT_TRIPLE:#atBatResultObj.Triple():
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

        elif ABRCode == gsATBATRESULT_HOMERUN:#atBatResultObj.HomeRun():

            i = 0
            while(i < 4):
                if self.__bases[i] != gsBASEEMPTY:
                    runnersAdvanced += [(self.__bases[i],i,0)]
                i += 1
            
            runnersScored = basesReversed
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY]*4

        elif ABRCode == gsATBATRESULT_WALK:#atBatResultObj.Walk() or atBatResultObj.HitByPitch():
            
            i = 0
            while(i < 4):
                if self.__bases[i] != gsBASEEMPTY:
                    runnersAdvanced += [(self.__bases[i],i,(i+1)%4)]
                i += 1
                    
            if not self._manOn(1):
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = gsBASEEMPTY
                
            elif self._manOn(1) and not self._manOn(2):
                self.__bases[2] = self.__bases[1]
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = gsBASEEMPTY

            elif self._manOn(1) and self._manOn(2) and not self._manOn(3):
                self.__bases[3] = self.__bases[2]
                self.__bases[2] = self.__bases[1]
                self.__bases[1] = self.__bases[0]
                self.__bases[0] = gsBASEEMPTY

            elif self._manOn(1) and self._manOn(2) and self._manOn(3):
                runnersScored = [self.__bases[3]]
                self.__bases = [gsBASEEMPTY] + self.__bases[0:3]

            else:
                print "DEBUG: Hit Default Case in _handleAdvanceAllRunners()\n"

        elif ABRCode == gsATBATRESULT_SACOUT:#atBatResultObj.SacrificeOut():

            #TODO: runnersAdvanced
            runnersScored = [basesReversed[0]]
            runnersScored = [runner for runner in runnersScored if runner != gsBASEEMPTY]            
            self.__bases = [gsBASEEMPTY]*2 + self.__bases[1:3]
        
        #atBatResultObj.setRunnersScored(runnersScored)
        #print "+++++++++++++++ %s +++++++++++++++++" % runnersScored
        return runnersAdvanced #runnersScored #list of runners scored

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

    def reset(self):
        self.__basesState.clearBases()
        self.__outs = 0

    def setBatterGUID(self, batterGUID):
        self.__basesState.setBatterGUID(batterGUID)

    def getInfieldLoc(self, theta, radius):
        if radius < 20:
            return gsPOSITION_POSSTR[gsCATCHER_POSCODE]

        if radius < 100:
            return gsPOSITION_POSSTR[gsPITCHER_POSCODE]
            #return 'P'

        if theta < min(gsTHETA_THIRDBASERANGE):#up the 3rd base line
            return gsPOSITION_POSSTR[gsTHIRDBASE_POSCODE]       
            #return '3B'
        
        if theta in gsTHETA_THIRDBASERANGE:
            return gsPOSITION_POSSTR[gsTHIRDBASE_POSCODE]       
            #return '3B'
        
        if theta < min(gsTHETA_SSRANGE):
            return gsPOSITION_POSSTR[gsSHORTSTOP_POSCODE]       
            #return 'SS'
        
        if theta in gsTHETA_SSRANGE:
            return gsPOSITION_POSSTR[gsSHORTSTOP_POSCODE]       
            #return 'SS'
        
        if theta < min(gsTHETA_SECONDBASERANGE):
            return gsPOSITION_POSSTR[gsSECONDBASE_POSCODE]       
            #return '2B'
        
        if theta in gsTHETA_SECONDBASERANGE:
            return gsPOSITION_POSSTR[gsSECONDBASE_POSCODE]       
            #return '2B'
        
        if theta < min(gsTHETA_FIRSTBASERANGE):
            return gsPOSITION_POSSTR[gsFIRSTBASE_POSCODE]       
            #return '1B'
        
        if theta in gsTHETA_FIRSTBASERANGE:
            return gsPOSITION_POSSTR[gsFIRSTBASE_POSCODE]       
            #return '1B'
        
        if theta <= gsTHETA_RIGHTFIELD_FOULPOLE:
            return gsPOSITION_POSSTR[gsFIRSTBASE_POSCODE]       
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
            return gsPOSITION_POSSTR[gsLEFTFIELDER_POSCODE]       
            #return 'LF'
        if theta < 66:
            return gsPOSITION_POSSTR[gsCENTERFIELDER_POSCODE]       
            #return 'CF'
        if theta <= 90:
            return gsPOSITION_POSSTR[gsRIGHTFIELDER_POSCODE]       
            #return 'RF'
    
    def getBasesState(self):
        return self.__basesState

    def simDefense(self, batBallContactResultOverride=None):

        batBallContactResult = None#self.__batBallContactResult
        if batBallContactResultOverride != None:
            batBallContactResult = batBallContactResultOverride
            
        (theta, phi, radius) = batBallContactResult.getHitParams()

        if theta < gsTHETA_LEFTFIELD_FOULPOLE or theta > gsTHETA_RIGHTFIELD_FOULPOLE:
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
            if theta < min(gsTHETA_THIRDBASERANGE):#up the 3rd base line
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
            
        return (result, runnersScored)#result



#TODO: make class for FieldGeometry
gsTHETA_LEFTFIELD_FOULPOLE = 0
gsTHETA_RIGHTFIELD_FOULPOLE = 90


#Simple Defensive Model for infielder ranges 
gsTHETA_THIRDBASERANGE = range(2,15)
gsTHETA_SSRANGE = range(20,41)
gsTHETA_SECONDBASERANGE = range(46, 61)
gsTHETA_FIRSTBASERANGE = range(71, 82)

gsMAXINFIELDRADIUS = 120
gsOUTFIELDSHALLOW = 210
gsOUTFIELDERMAXRADIUS = 350
gsOUTFIELDDOUBLE = 400#385
#gsOUTFIELDTRIPLE = 400

class DefensiveFieldState:
#holds position and locations of base runners
#as well as the abilities of players at those positions
    def __init__(self, baseState=None, outCount=None, 
                 FieldGeometry=None, PlayerFielderAbilities=None):
        self.__playersFielders = PlayerFielderAbilities

        self.__bases = baseState
        self.__outs = outCount
        #self.__batBallContactResult = None
        #self.__batterAtBatScoring = None
        #self.__fieldGeometry = None
        #self.__fielderAbilities = None
        #self.__runnerAbilities = None
        #self.__fieldState = None
        


    def getInfieldLoc(self, theta, radius):
        if radius < 20:
            return 'C'

        if radius < 100:
            return 'P'

        if theta < min(gsTHETA_THIRDBASERANGE):#up the 3rd base line
            return '3B'
        
        if theta in gsTHETA_THIRDBASERANGE:
            return '3B'
        
        if theta < min(gsTHETA_SSRANGE):
            return 'SS'
        
        if theta in gsTHETA_SSRANGE:
            return 'SS'
        
        if theta < min(gsTHETA_SECONDBASERANGE):
            return '2B'
        
        if theta in gsTHETA_SECONDBASERANGE:
            return '2B'
        
        if theta < min(gsTHETA_FIRSTBASERANGE):
            return '1B'
        
        if theta in gsTHETA_FIRSTBASERANGE:
            return '1B'
        
        if theta <= gsTHETA_RIGHTFIELD_FOULPOLE:
            return '1B'

    def getFieldLocModifier(self, radius):
        #thetaLoc = ''
        #descriptor = '' #deep, shallow
        #if radius < gsINFIELDMAXRADIUS:
        #    return 'INF'
        #if radius < gs
        return radius#"%s" % radius

    def getOutfieldLoc(self, theta):
        if theta < 33:
            return 'LF'
        if theta < 66:
            return 'CF'
        if theta <= 90:
            return 'RF'
        
    def simFieldBallContact(self, batBallContactResult):
        (theta, phi, radius) = batBallContactResult.getHitParams()

        if theta < gsTHETA_LEFTFIELD_FOULPOLE or theta > gsTHETA_RIGHTFIELD_FOULPOLE:
            return ('FOUL', None, radius)

        if phi:
            #its in the air
            if radius < gsMAXINFIELDRADIUS:
                #return 'AO(%s,%s)' % (self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                return ('AO', self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
            if radius < gsOUTFIELDSHALLOW:
                #return '1B(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
                return ('1B', self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
            if radius < gsOUTFIELDERMAXRADIUS:
                #return 'AO(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
                return ('AO', self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
            if radius < gsOUTFIELDDOUBLE:
                #return '2B(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
                return ('2B', self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
            #if radius < gsOUTFIELDTRIPLE:
            #    return '3B(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))

            else:
                #return 'HR(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
                return ('HR', self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
        else:
            #its a ground ball
            if theta < min(gsTHETA_THIRDBASERANGE):#up the 3rd base line
                #return '3B(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
                return ('3B', self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
            if theta in gsTHETA_THIRDBASERANGE:
                #return 'GO(%s,%s)' % (self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                return ('GO', self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
            if theta < min(gsTHETA_SSRANGE):
                #return '1B(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
                return ('1B', self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
            if theta in gsTHETA_SSRANGE:
                #return 'GO(%s,%s)' % (self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                return ('GO', self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
            if theta < min(gsTHETA_SECONDBASERANGE):
                #return '1B(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
                return ('1B', self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
            if theta in gsTHETA_SECONDBASERANGE:
                #return 'GO(%s,%s)' % (self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                return ('GO', self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
            if theta < min(gsTHETA_FIRSTBASERANGE):
                #return '1B(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
                return ('1B', self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
            if theta in gsTHETA_FIRSTBASERANGE:
                #return 'GO(%s,%s)' % (self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
                return ('GO', self.getInfieldLoc(theta,radius), self.getFieldLocModifier(radius))
            if theta <= gsTHETA_RIGHTFIELD_FOULPOLE:
                #return '3B(%s,%s)' % (self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
                return ('3B', self.getOutfieldLoc(theta), self.getFieldLocModifier(radius))
        return "unmatched case in simFieldBallContact"

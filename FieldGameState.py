
gsTHETA_LEFTFIELD_FOULPOLE = 0
gsTHETA_RIGHTFIELD_FOULPOLE = 90

#Simple Model for infielder ranges 
gsTHETA_THIRDBASERANGE = range(3,15)
gsTHETA_SSRANGE = range(25,40)
gsTHETA_SECONDBASERANGE = range(50, 65)
gsTHETA_FIRSTBASERANGE = range(75, 87)

class DefensiveFieldState:
#holds position and locations
#as well as the abilities of players at those positions
    def __init__(self, FieldGeometry=None, PlayerFielderAbilities=None):
        self.__palyers = PlayerFielderAbilities
        

    def simFieldBallContact(self, batBallContactResult):
        (theta, phi, radius) = batBallContactResult.getHitParams()

        if theta < gsTHETA_LEFTFIELD_FOULPOLE or theta > gsTHETA_RIGHTFIELD_FOULPOLE:
            return 'FOUL'

        if phi:
            #its in the air
            if radius < 120:
                return 'AO'
            
            if radius < 220:
                return 'S'

            if radius < 350:
                return 'AO'

            if radius < 375:
                return '2B'

            if radius < 400:
                return '3B'

            else:
                return 'HR'
        
        else:
            #its a ground ball
            if theta < min(gsTHETA_THIRDBASERANGE):#up the 3rd base line
                return '2B'

            if theta in gsTHETA_THIRDBASERANGE:
                return 'GO'

            if theta < min(gsTHETA_SSRANGE):
                return 'S'

            if theta in gsTHETA_SSRANGE:
                return 'GO'

            if theta < min(gsTHETA_SECONDBASERANGE):
                return 'S'

            if theta in gsTHETA_SECONDBASERANGE:
                return 'GO'

            if theta < min(gsTHETA_FIRSTBASERANGE):
                return 'S'

            if theta in gsTHETA_FIRSTBASERANGE:
                return 'GO'

            if theta <= gsTHETA_RIGHTFIELD_FOULPOLE:
                return '2B'

        return "unmatched case in simFieldBallContact"

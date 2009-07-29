import pystats
import array
#import PlayerAbilities
from Globals import *


################################################
#
# BoundaryConditions
#
# PrContact(given pitchType, Best Batter, Worst Pitcher) = 0.90
# PrContact(given pitchType, Worst Batter, Best Pitcher) = 0.10
# PrContact(given pitchType, Best Batter, Best Pitcher) = 0.50
# PrContact(given pitchType, Worst Batter, Worst Pitcher) = 0.50
#
# "same conditions for Zone"
#
#
# because these two probabilities are multiplied to get the PrContact
# it means the worst probability is .10^2 ~1% and the best is .90^2 ~80%
#
# We chose to have each pitch have a possible 100 levels of mastery 
# and each zone to have the same
###############################################
gsNUM_PITCHMASTERY_LEVELS = 100.0
gsNUM_ZONEMASTERY_LEVELS = 100.0
gsBC_BESTBAT_VS_WORSTPIT = 0.90
gsBC_WORSTBAT_VS_BESTPIT = 0.30
gsBC_SAMEBAT_VS_SAMEPIT = 0.60
gsPITCHMASTERY_LEVEL_STEPSIZE = (gsBC_BESTBAT_VS_WORSTPIT - gsBC_WORSTBAT_VS_BESTPIT)/float(gsNUM_PITCHMASTERY_LEVELS)
gsZONEMASTERY_LEVEL_STEPSIZE = (gsBC_BESTBAT_VS_WORSTPIT - gsBC_WORSTBAT_VS_BESTPIT)/float(gsNUM_ZONEMASTERY_LEVELS)
def PrContactNew(pitcherAbilities, batterAbilities, pitchAttrs):

    pitchType, pitchZone = pitchAttrs

    batterZoneMastery = batterAbilities.getBattingZoneMasteryMatrix()
    pitcherZoneMastery = pitcherAbilities.getPitchingZoneMasteryMatrix()

    batterPitchMastery = batterAbilities.getBattingPitchMasteryMatrix()
    pitcherPitchMastery = pitcherAbilities.getPitchingPitchMasteryMatrix()

    if pitchType not in pitcherPitchMastery:
        print "DEBUG pitchType: %s not in pitch mastery matrix for pitcher\n" % pitchType

    if pitchType not in batterPitchMastery:
        print "DEBUG pitchType: %s not in pitch mastery matrix for pitcher\n" % pitchType

    batterPitchLvl = batterPitchMastery[pitchType]
    pitcherPitchLvl = pitcherPitchMastery[pitchType]

    batterZoneLvl = batterZoneMastery[pitchZone]
    pitcherZoneLvl = pitcherZoneMastery[pitchZone]
    
    if type(batterPitchLvl) != type(float()):
        print "DEBUG: batterPitchLvl not a float"

    if type(pitcherPitchLvl) != type(float()):
        print "DEBUG: pitcherPitchLvl not a float"

    if type(batterZoneLvl) != type(float()):
        print "DEBUG: batterZoneLvl not a float"

    if type(pitcherZoneLvl) != type(float()):
        print "DEBUG: pitcherZoneLvl not a float"

    prContactPitch = gsBC_SAMEBAT_VS_SAMEPIT  + (batterPitchLvl*gsPITCHMASTERY_LEVEL_STEPSIZE) - (pitcherPitchLvl*gsPITCHMASTERY_LEVEL_STEPSIZE)
    prContactZone = gsBC_SAMEBAT_VS_SAMEPIT + (batterZoneLvl*gsZONEMASTERY_LEVEL_STEPSIZE) - (pitcherZoneLvl*gsZONEMASTERY_LEVEL_STEPSIZE)
    #print prContactPitch
    #print prContactZone
    return prContactPitch * prContactZone

OLD = """
#
#
#
def Chi2Prime(Chi2Batter, Chi2Pitcher):
    if Chi2Batter > PlayerAbilities.gsChi2BatterMax:
        print "Chi2BatterMax Error: %f > %f.\n" % (Chi2Batter, PlayerAbilities.gsChi2BatterMax)
        return 

    if Chi2Pitcher > PlayerAbilities.gsChi2PitcherMax:
        print "Chi2PitcherMax Error: %f > %f.\n" % (Chi2Pitcher, PlayerAbilities.gsChi2PitcherMax)

    Chi2prime = PlayerAbilities.gsChi2Normal - Chi2Batter + Chi2Pitcher
    return Chi2prime
#
#
#
def MuPrime(MuBatter, MuPitcher):
    
    if MuPitcher > MuBatter:
        return MuPitcher - MuBatter
    
    #else muB >= muP
    return 0.0


#def PrPower(pitcherAbilities, batterAbilities, 

#
# 
#
def PrContact(pitcherAbilities, batterAbilities, pitchAttrs):
    
    (pitchType, pitchZone) = pitchAttrs
    
    #print "TODO: check pitchZone is valid"
    #print "TODO: check pitchType is valid"
    
    #print pitcherAbilities
    #print batterAbilities
   
    batterZoneMastery = batterAbilities.getBattingZoneMasteryMatrix()#['zoneMastery']
    pitcherZoneMastery = pitcherAbilities.getPitchingZoneMasteryMatrix()#['zoneMastery']

    batterPitchMastery = batterAbilities.getBattingPitchMasteryMatrix()#['pitchMastery']
    pitcherPitchMastery = pitcherAbilities.getPitchingPitchMasteryMatrix()#['pitchMastery']

    #set to defaults
    pitcherMu = 0.0
    batterMu = 0.0 
    if pitchType not in pitcherPitchMastery:
        print "pitchType: %s not in pitch mastery matrix for pitcher\n" % pitchType
    else:
        pitcherMu = pitcherPitchMastery[pitchType]

    if pitchType not in batterPitchMastery:
        print "pitchType: %s not in pitch mastery matrix for pitcher\n" % pitchType
    else:
        batterMu = batterPitchMastery[pitchType]

    #subtracts from pitcherMu for given pitch type
    #if a batter skill > a pitcher skill 

    muPrime = MuPrime(batterMu, pitcherMu)

    chi2prime = Chi2Prime(batterZoneMastery[pitchZone], pitcherZoneMastery[pitchZone])

    probOfContactZone = numIntegrate(100, -5, 5, 
                                     chi2prime, PlayerAbilities.gsBATTERMUFIXED,
                                     PlayerAbilities.gsPITCHERCHI2FIXED, muPrime)
                                 
    #chi2PrimePitch = Chi2Prime(batterPitchMastery[pitchType], pitcherPitchMastery[pitchType])
    #probOfContactPitch = numIntegrate(100, -5, 5,
    #                                  chi2PrimePitch, PlayerAbilities.gsBATTERMUFIXED,
    #                                  PlayerAbilities.gsPITCHERCHI2FIXED, muPrime)
    

                                      
    #print "Pr(ZoneContact):%f\n" % probOfContactZone
    #print "Pr(PitchContact):%f\n" % probOfContactPitch

    return probOfContactZone#*probOfContactPitch


def pdfXY(xy, mx, my, sx, sy):
    return pystats.normpdf(xy, mx, sx) * pystats.normpdf(xy, my, sy)

def numIntegrate1(n, x0, x1, stdDev=1.0, mean=0.0):

    accum = 0.0

    #step size
    dx = (float(x1) - float(x0)) / float(n)
    #print "dx: %f\n" % dx
    #print "nsteps: %d\n" % n

    i = 0
    xn = float(x0)
    xnplus1 = float(x0) + dx
    while i < n:

        yn = pystats.normpdf(xn, mean, stdDev)
        ynplus1 = pystats.normpdf(xnplus1, mean, stdDev)
        #yn = pdfXY(xn, batMean, pitchMean, batStdDev, pitchStdDev)
        #ynplus1 = pdfXY(xnplus1, batMean, pitchMean, batStdDev, pitchStdDev)

        h = (yn + ynplus1) / 2.0
                
        accum += h*dx

        xn = xnplus1 
        xnplus1 += dx

        i += 1

    return accum


def numIntegrate(n, x0, x1, 
                batStdDev=1.0, batMean=0.0, 
                pitchStdDev=1.0, pitchMean=0.0):

    accum = 0.0

    #batStdDev = 0.1#chi^2
    #batMean = 0.0 #mu 

    #pitchStdDev = 0.1
    #pitchMean = 0.0

    #step size
    dx = (float(x1) - float(x0)) / float(n)
    #print "dx: %f\n" % dx
    #print "nsteps: %d\n" % n

    i = 0
    xn = float(x0)
    xnplus1 = float(x0) + dx

    while i < n:

        #yn = pystats.normpdf(xn, mean, stdDev)
        #ynplus1 = pystats.normpdf(xnplus1, mean, stdDev)
        yn = pdfXY(xn, batMean, pitchMean, batStdDev, pitchStdDev)
        ynplus1 = pdfXY(xnplus1, batMean, pitchMean, batStdDev, pitchStdDev)

        h = (yn + ynplus1) / 2.0
                
        accum += h*dx

        xn = xnplus1 
        xnplus1 += dx

        i += 1

    return accum
"""

def generateVaryBattersChiSq():
    #Vary bat(chi^2)
    batChiSq = 0.01
    stepSize = 0.00001
    file = open("chi2.csv", "w+")
    for i in range(50000):
        prob = numIntegrate(100,-5,5, batChiSq, 0.0, 1.0, 0.0)
        #print "chi^2(%f) => %f\n" % (batChiSq, prob)
        file.write("%f , %f\n" % (batChiSq, prob))
        batChiSq += stepSize

    file.close()

def generateVaryBattersMu():
    #Vary bat Mu
    batMu = 0.0
    stepSize = 0.001
    file = open("mu.csv", "w+")
    for i in range(25000):
        prob = estIntegral(100,-5,5, 1.0, batMu, 1.0, 0.0)
        #print "chi^2(%f) => %f\n" % (batChiSq, prob)
        if prob < 0.50000:
            break
        file.write("%f , %f\n" % (batMu, prob))
        batMu += stepSize

    file.close()

def generateVaryBatterChi2MaxPitcherMu():
    maxMu = 3.65
    minMu = 0.00
    maxChi2 = 40
    minChi2 = 0.01
    #Vary bat Mu
    batChi2 = 0.01
    stepSize = 0.1
    file = open("batterChiMaxPitcherMu.csv", "w+")
    for i in range(10000):
        prob = estIntegral(100,-5,5, batChi2, 0.0, 1.0, maxMu)
        #print "chi^2(%f) => %f\n" % (batChiSq, prob)
        file.write("%f , %f\n" % (batChi2, prob))
        batChi2 += stepSize

    file.close()


#generateVaryBattersMu()
#generateVaryBattersChiSq()
#generateVaryBatterChi2MaxPitcherMu()

def main():
    import PlayerAbilities
    for i in range(9):
        if not i % 3:
            print ""
        p = 0.0
        p = PrContactNew(PlayerAbilities.PlayerAbilities(), 
                      PlayerAbilities.PlayerAbilities(), 
                      (gsFASTBALL, i))
        print "%f\t" % p,

    print ""
    return



if __name__ == "__main__":
    main()

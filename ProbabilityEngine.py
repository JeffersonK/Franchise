import pystats
import array


#Chi => Zone
#mu => pitch

######
#
# Chi2
######
Chi2Normal = 1.0
Chi2PrimeMin = 0.018
Chi2PrimeMax = 3.862#Chi2Normal - Chi2PrimMin

Chi2BatterMax = Chi2Normal - Chi2PrimeMin #0.982
Chi2PitcherMax = Chi2PrimeMax - Chi2Normal

Chi2BatterMin = 0.0
Chi2PitcherMin = 0.0

Chi2b0 = Chi2BatterMin + .25
Chi2p0 = Chi2PitcherMin #+ 2.862

PITCHERCHI2FIXED = 1.0
BATTERMUFIXED = 0.0

######
#
# Mu
######


MuPrimeMax = 3.65

MuBatterMin = 0.0
MuPitcherMin = 0.0#2.5

MuBatterMax = MuPrimeMax
MuPitcherMax = MuPrimeMax

minPower = 1
batterPowerZones = [minPower, minPower, minPower,
                    minPower, minPower, minPower,
                    minPower, minPower, minPower]
                    

batterZoneMastery = [Chi2b0, Chi2b0, Chi2b0,
                     Chi2b0, Chi2b0, Chi2b0,
                     Chi2b0, Chi2b0, Chi2b0]

batterPitchMastery = {'curveball':MuBatterMin, 
                       'fastball':MuBatterMin,
                       'slider':MuBatterMin,
                       'changeup':MuBatterMin,
                       'knuckleball':MuBatterMin}

pitcherZoneMastery = [Chi2p0, Chi2p0, Chi2p0,
                      Chi2p0, Chi2p0, Chi2p0,
                      Chi2p0, Chi2p0, Chi2p0]


pitcherPitchMastery = {'curveball':MuPitcherMin, 
                       'fastball':MuPitcherMin,
                       'slider':MuPitcherMin,
                       'changeup':MuPitcherMin,
                       'knuckleball':MuPitcherMin}

pitcherAbil = {'zoneMastery':pitcherZoneMastery,
               'pitchMastery':pitcherPitchMastery}

batterAbil = {'zoneMastery':batterZoneMastery,
              'pitchMastery':batterPitchMastery,
              'powerZones':batterPowerZones}

#
#
#
def Chi2Prime(Chi2Batter, Chi2Pitcher):
    if Chi2Batter > Chi2BatterMax:
        print "Chi2BatterMax Error: %f > %f.\n" % (Chi2Batter, Chi2BatterMax)
        return 

    if Chi2Pitcher > Chi2PitcherMax:
        print "Chi2PitcherMax Error: %f > %f.\n" % (Chi2Pitcher, Chi2PitcherMax)

    Chi2prime = Chi2Normal - Chi2Batter + Chi2Pitcher
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
    
    #TODO: check pitchZone is valid
    #TODO: check pitchType is valid

    batterZoneMastery = batterAbilities['zoneMastery']
    pitcherZoneMastery = pitcherAbilities['zoneMastery']

    batterPitchMastery = batterAbilities['pitchMastery']
    pitcherPitchMastery = pitcherAbilities['pitchMastery']

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

    probOfContact = numIntegrate(100, -5, 5, 
                                 chi2prime, BATTERMUFIXED,
                                 PITCHERCHI2FIXED, muPrime)
                                 
                                 

    #print "%f\n" % probOfContact
    return probOfContact


def pdfXY(xy, mx, my, sx, sy):
    return pystats.normpdf(xy, mx, sx) * pystats.normpdf(xy, my, sy)

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


def generateVaryBattersChiSq():
    #Vary bat(chi^2)
    batChiSq = 0.01
    stepSize = 0.0001
    file = open("chi2.csv", "w+")
    for i in range(50000):
        prob = estIntegral(100,-5,5, batChiSq, 0.0, 1.0, 0.0)
        #print "chi^2(%f) => %f\n" % (batChiSq, prob)
        file.write("%f , %f\n" % (batChiSq, prob))
        batChiSq += stepSize

    file.close()

def generateVaryBattersMu():
    #Vary bat Mu
    batMu = 0.0
    stepSize = 0.001
    file = open("mu.csv", "w+")
    for i in range(10000):
        prob = estIntegral(100,-5,5, 1.0, batMu, 1.0, 0.0)
        #print "chi^2(%f) => %f\n" % (batChiSq, prob)
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
    
    for i in range(9):
        if not i % 3:
            print ""
        p = 0.0
        p = PrContact(pitcherAbil, batterAbil, ('curveball', i))
        print "%f\t" % p,

    print ""
    return



if __name__ == "__main__":
    main()

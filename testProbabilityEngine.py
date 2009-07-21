import GameState as GS

Chi2b0 = 0.0
Chi2p0 = 0.0

MuBatterMin = 0.0
MuPitcherMin = 0.0

bzm = [Chi2b0, Chi2b0, Chi2b0,
       Chi2b0, Chi2b0, Chi2b0,
       Chi2b0, Chi2b0, Chi2b0]

bpm = {GS.CURVEBALL:MuBatterMin, 
       GS.FASTBALL:MuBatterMin,
       GS.SLIDER:MuBatterMin,
       GS.CHANGEUP:MuBatterMin,
       GS.KNUCKLEBALL:MuBatterMin}

pzm = [Chi2p0, Chi2p0, Chi2p0,
       Chi2p0, Chi2p0, Chi2p0,
       Chi2p0, Chi2p0, Chi2p0]

ppm = {GS.CURVEBALL:MuPitcherMin, 
       GS.FASTBALL:MuPitcherMin,
       GS.SLIDER:MuPitcherMin,
       GS.CHANGEUP:MuPitcherMin,
       GS.KNUCKLEBALL:MuPitcherMin}

pa = {'zoneMastery':pzm,
      'pitchMastery':ppm}

ba = {'zoneMastery':bzm,
      'pitchMastery':bpm}



abr = GS.AtBatResult(0,1,(0, 0))
#ret = abr.simAtBat(pa, ba,(GS.FASTBALL,1))
ret = abr.simPitch(pa, ba,(GS.FASTBALL,1))
print abr
print ret

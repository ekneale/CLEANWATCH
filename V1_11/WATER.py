import Iso, Eff
from math import pow
import numpy as np
r = 10026.35e-3
vol = np.pi*pow(r, 3)*2
defPPM = [0.002, 0.01]
IsoAct = defPPM
revIsoAct = PPM
IsoList = Iso.WATER
IsoDecay = [Iso.Rn222,
            Iso.RN]
IsoEff = [Eff.WATERRn222,
         [1]]
EffErr = [Eff.WATERRn222Err,
         [0]]
def Activity(PPM):
    for i in range(len(PPM)-1):
        IsoAct[i] = PPM[i]*vol
def revActivity(BG, Eff):
    for i in range(len(BG)-1):
        maxbg = max(BG[i])
        x = BG[i].index(maxbg)
        if Eff[i][x] != 0:
            revIsoAct[i] = maxbg/Eff[i][x]/vol
        else:
            revIsoAct[i] = 0
defAct = Activity(defPPM)

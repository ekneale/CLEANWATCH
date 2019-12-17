import Iso, Eff
import numpy as np
from math import pow
den = 2165
vol = np.pi*((pow(18,2)*35.5)-pow(13,2)*25.5)
mass = den*vol
defPPM = [10e-3, 220e-3, 750, 0.02]
IsoAct = defPPM
revIsoAct = defPPM
IsoList = Iso.ROCK
IsoDecay = [Iso.U238,
            Iso.Th232,
            Iso.K40,
            Iso.FN]
IsoEff = [Eff.ROCKU238,
          Eff.ROCKTh232,
          Eff.ROCKK40,
          [1]]
EffErr = [Eff.ROCKU238Err,
          Eff.ROCKTh232Err,
          Eff.ROCKK40Err,
          [0]]
def Activity(PPM):
    IAct = []
    for i in range(len(PPM)-1):
        IAct.append(((Iso.Lam[i]*Iso.Abs[i])/(Iso.Ms[i]*1e6))*mass*PPM[i])
    IAct.append(defPPM[-1])
    return IAct
def revActivity(BG, Eff):
    rIsoAct = []
    for i in range(len(BG)):
        maxbg = max(BG[i])
        x = BG[i].index(maxbg)
        if Eff[i][x] != 0:
            rIsoAct.append(maxbg/Eff[i][x]/mass/((Iso.Ms[i]*1e6)/(Iso.Lam[i]*Iso.Abs)))
        else:
            rIsoAct.append(0)
    return rIsoAct
defAct = Activity(defPPM)

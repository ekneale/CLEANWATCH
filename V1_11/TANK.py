import Iso, Eff
from math import pow
import numpy as np
h = 10026.35e-3
r = 10026.35e-3
t = 6.35e-3
vol = (2*np.pi*h*pow(r, 2))-(2*np.pi*(h-t)*pow(r-t, 2)) #m^
den = 8000 #kg/m^3
mass = vol*den #96200.08945836162 kg
#print(mass)
defPPM = [0.17, 3.8e-3, 34e-3, 19e-3, 7.7e-4]
IsoAct = defPPM
revIsoAct = defPPM
IsoList = Iso.TANK
IsoDecay = [Iso.U238,
            Iso.Th232,
            Iso.K40,
            Iso.Co60,
            Iso.Cs137]
IsoEff =   [Eff.TANKU238,
            Eff.TANKTh232,
            Eff.TANKK40,
            Eff.TANKCo60,
            Eff.TANKCs137]
EffErr =   [Eff.TANKU238Err,
            Eff.TANKTh232Err,
            Eff.TANKK40Err,
            Eff.TANKCo60Err,
            Eff.TANKCs137Err]
def Activity(PPM):
    IAct = []
    for i in range(len(PPM)):
        IAct.append(PPM[i]*mass)
        print('Activity due to ' + Iso.TANK[i] + ' = %.5e' % IAct[i])
    return IAct
def revActivity(BG, Eff):
    rIsoAct = [0 for i in range(len(IsoList))]
    for i in range(len(BG)):
        maxbg = max(BG[i])
        x = BG[i].index(maxbg)
        if Eff[i][x] != 0:
            rIsoAct[i] = (maxbg/Eff[i][x]/mass)
        else:
            rIsoAct[i] = 0
    return rIsoAct

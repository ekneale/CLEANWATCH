import Iso
from math import pow
import numpy as np
vol = np.pi*(51/2)*(pow(13,2)-pow(12.5,2))-(np.pi/2)*pow(13,2) #m^3
den = 2300
mass = vol*den
defPPM = [61, 30, 493]
IsoAct = defPPM
revIsoAct = defPPM
IsoList = Iso.CONC
IsoDecay = [Iso.U238,
            Iso.Th232,
            Iso.K40]
IsoEff =   [[0, 0, 0, 0, 0], #U238
            [0, 0, 0, 0],    #Th232
            [0]]             #K40
EffErr = IsoEff
def Activity(PPM):
    IAct = []
    for i in range(len(PPM)):
        IAct.append(PPM[i]*mass)
        print('Activity due to ' + Iso.CONC[i] + ' = %.5e' % IAct[i])
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

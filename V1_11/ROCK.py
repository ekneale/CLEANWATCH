import Iso, Eff
import numpy as np
from math import *
den = 2165
vol = np.pi*((pow(18,2)*35.5)-pow(13,2)*25.5)
mass = den*vol
#print(mass)
defPPM = [10e-3, 220e-3, 750, 0.02]
IType = ['PPM', 'PPM', 'PPM', 'Events per day']
IsoAct = defPPM
revIsoAct = defPPM
IsoList = Iso.ROCK
IType = ['PPM', 'PPM', 'PPM', 'Events per day']
IsoDecay = [Iso.U238,
            Iso.Th232,
            Iso.K40]#,
            #Iso.FN]
IsoEff = [[0, 0, 0, 0, 0],
          [0, 0, 0, 0],
          [0]]#,
          #[1]]
EffErr = [[0, 0, 0, 0, 0],
          [0, 0, 0, 0],
          [0]]#,
          #[0]]
def Activity(PPM):
    IAct = []
    for i in range(len(PPM)-1):
        IAct.append((Iso.Lam[i]*Iso.Abs[i])/(Iso.Ms[i]*1e6)*mass*PPM[i])
        print('Activity for ' + Iso.ROCK[i] + ' = %5e' % IAct[i])
    IAct.append(defPPM[-1])
    return IAct
def revActivity(BG, Eff,NEff):
    rIsoAct = [0 for i in range(len(IsoList))]
    for i in range(len(BG)):
        maxbg = max(BG[i])
        x = BG[i].index(maxbg)
        if i > len(BG) - 1:
            if Eff[i][x] != 0:
                rIsoAct[i] = sqrt(maxbg/Eff[i][x]/NEff[i][x])/mass*(Iso.Ms[i]*1e6)/(Iso.Lam[i]*Iso.Abs[i])
            else:
                rIsoAct[i] = 0
        else:
            rIsoAct[i] = BG[i][x]
    return rIsoAct
#defAct = Activity(defPPM)

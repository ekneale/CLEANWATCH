#imports
from math import log, pow
import numpy as np
import Eff
import Prate as Pr
import Nrate as Nr
Ms = [3.953e-25, 3.853145e-25, 6.636286e-26]
Lam = [4.916e-18, 1.57e-18, 1.842e-18]
halfL = Lam
for i in range(len(Lam)):
    halfL[i] = (log(2)/Lam[i])/(pow(60,2)*24*365*1e6)
Abs = [1, 1, 0.00117]
#FN = 0.02
Iso = ['U238', 'Th232', 'K40', 'Fast Neutron']
IsoDecay = [['Pa234', 'Pb214', 'Bi214', 'Bi210', 
            'Tl210'],
            ['Ac228', 'Pb212', 'Bi212', 'Tl208'],
            ['K40'],
            ['FN']]
IsoDefault = [10e-3, 220e-3, 750, 0.02]
ROCKEff = [Eff.ROCKU238,
           Eff.ROCKTh232,
           Eff.ROCKK40
           [1]]
ROCKErr = [Eff.ROCKU238Err,
           Eff.ROCKTh232Err,
           Eff.ROCKK40Err,
           [0]]
ROCK_Pr = [Pr.ROCKU238,
           Pr.ROCKTh232,
           Pr.ROCKK40,
           [0]]
ROCK_Nr = [Nr.ROCKU238,
           Nr.ROCKTh232,
           Nr.ROCKK40,
           [0]]
def ROCKAct(PPM):
    den = 2165 #kg/m^3
    vol = np.pi*((pow(18,2)*35.5)-(pow(13,2)*25.5))
    mass = den*vol
    Act = PPM
    for i in range(len(Act)-1):
        Act[i] = ((Lam[i]*PPM[i])/(Ms[i]*1e6))*mass
    Act[-1] = FN
    return Act
ROCKIsoAct = ROCKAct(IsoDefault)
def ErrProp(EffErr, Eff, BG):
    if Eff != 0:
        centErr = EffErr/Eff
        err = BG*centErr
    else:
        err = 0
    return err
def BGRate():
    ROCKBGIso = [[], [], [], []]
    ROCKBGR = 0
    ROCKBGIso_N = [[], [], [], []]
    ROCKBGR_N = 0
    ROCKBGErr = [[], [], [], []]
    for i in range(len(ROCKIsoDecay)):
        for x in range(len(ROCKIsoDecay[i])):
            if ROCKIsoDecay[i][x] == 'Tl210':
                ROCKBGIso[i].append(ROCKIsoAct[i][x]*ROCKIsoEff[i][x]*0.002)
            else:
                ROCKIsoBG[i].append(ROCKIsoAct[i][x]*ROCKIsoEff[i][x])
            #ROCKBGErr[i].append(
            print('BGR due to ' + ROCKIsoDecay[i][x] + ' %.5e +/- %.5e' % (ROCKBGIso[i][x], ROCKBGErr[i][x]))
        ROCKBGR += sum(ROCKBGIso[i])
        #ROCKBGR_N += sum(ROCKBGIsoN[i])
    return ROCKBGIso, ROCKBGR

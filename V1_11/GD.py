import numpy as np
from math import pow
import Eff
import Iso
TankR = 10026.35e-3
Height = 10026.35e-3
defPPM = [10e-3, 0.25e-3, 0.2e-3, 0.28e-3, 1.7e-3, 0.35e-3] #mBq/kg
IsoAct = defPPM
revIsoAct = defPPM
IsoList = Iso.GD
IsoDecay = [Iso.U238,        #U238
            Iso.Th232,       #Th232
            Iso.U235,        #U235
            Iso.U238,        #U238
            Iso.Th232,       #Th232
            Iso.U235]        #U235
IsoEff =   [Eff.GDU238,      #U238
            Eff.GDTh232,     #Th232
            Eff.GDU235]      #U235
EffErr =   [Eff.GDU238Err,   #U238
            Eff.GDTh232Err,  #Th232
            Eff.GDU235Err]   #U235
Err = EffErr
def Activity(PPM):
    IAct = []
    mass = np.pi*pow(TankR, 2)*(2*Height)*1e3
    for i in range(len(PPM)):
        IAct.append(PPM[i]*mass*0.002)
        print('Activity of ' + Iso.GD[i] + ' = %.5e Bq' % (IAct[i]))
    return IAct
def revActivity(BG, Eff):
    rIsoAct = [0 for i in range(len(IsoList))]
    mass = np.pi*pow(TankR, 2)*(2*Height)*1e3
    const = mass*0.002
    for i in range(len(BG)):
        maxbg = max(BG[i])
        x = BG[i].index(maxbg)
        if Eff[i][x] != 0:
            revIsoAct[i] = (maxbg/Eff[i][x]/const)
        else:
            revIsoAct[i] = 0
    return rIsoAct
#defAct = Activity(defPPM)
#print('No Errors')

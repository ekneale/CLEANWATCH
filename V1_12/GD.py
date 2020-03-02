import numpy as np
from math import *
import Eff
import Iso
TankR = 10026.35e-3
Height = 10026.35e-3
defPPM = [10e-3, 0.2e-3, 0.25e-3, 0.28e-3, 0.35e-3, 1.7e-3] #mBq/kg
IsoAct = defPPM
revIsoAct = defPPM
IsoList = Iso.GD
IType = ['PPM' for i in range(len(IsoList))]
IsoDecay = [['Pa234'],                                   #U238 upper
            ['Ac228'],                                   #Th232 upper
            ['Th231'],                                   #U235 upper
            ['Pb214', 'Bi214', 'Bi210', 'Tl210'],        #U238 lower
            ['Pb212', 'Bi211', 'Tl208'],                 #Th232 lower 
            ['Fr223', 'Pb211', 'Bi211', 'Tl207']]        #U235 lower
IsoEff =   [Eff.GDU238u,      #U238_u
            Eff.GDTh232u,     #Th232_u
            Eff.GDU235u,      #U235_u
            Eff.GDU238l,      #U238_l
            Eff.GDTh232l,     #Th232_l
            Eff.GDU235l]      #U235_l
EffErr =   [Eff.GDU238uErr,   #U238_u
            Eff.GDTh232uErr,  #Th232_u
            Eff.GDU235uErr,   #U235_u
            Eff.GDU238lErr,   #U238_l
            Eff.GDTh232lErr,  #Th232_l
            Eff.GDU235lErr]   #U235_l
Err = EffErr
def Activity(PPM):
    IAct = []
    mass = np.pi*pow(TankR, 2)*(2*Height)*1e3
    for i in range(len(PPM)):
        IAct.append(PPM[i]*mass*0.002)
        print('Activity of ' + Iso.GD[i] + ' = %.5e Bq' % (IAct[i]))
    return IAct
def revActivity(BG, Eff,NEff):
    rIsoAct = [0 for i in range(len(IsoList))]
    mass = np.pi*pow(TankR, 2)*(2*Height)*1e3
    const = mass*0.002
    for i in range(len(IsoList)):
        maxbg = max(BG[i])
        x = BG[i].index(maxbg)
        if Eff[i][x] != 0:
            rIsoAct[i] = maxbg/Eff[i][x]/const
        else:
            print('Efficiency = 0')
            rIsoAct[i] = 0
    return rIsoAct
#defAct = Activity(defPPM)
#print('No Errors')

import numpy as np
from math import pow
import Eff
TankR = 10026.35e-3
Height = 10026.35e-3
PPM = [1, 1, 1, 1, 1, 1]
Iso = ['U238', 'Th232', 'U235', 'U238_l', 'Th232_l', 'U235_l']
IsoDecay = [['Pa234', 'Pb214', 'Bi214', 'Bi210',
             'Tl210'], #U238
            ['Ac228', 'Pb212', 'Bi212', 'Tl208'], 
                       #Th232
            ['Th231', 'Fr223', 'Pb211', 'Bi211', 
             'Tl207'], #U235
            ['Pa234', 'Pb214', 'Bi214', 'Bi210',
             'Tl210'], #U238_l
            ['Ac228', 'Pb212', 'Bi212', 'Tl208'], 
                       #Th232_l
            ['Th231', 'Fr223', 'Pb211', 'Bi211',
             'Tl207']] #U235_l
GDIsoEff = [Eff.GDU238,   #U238
            Eff.GDTh232,  #Th232
            Eff.GDU235,   #U235
            Eff.GDU238,   #U238_l
            Eff.GDTh232,  #Th232_l
            Eff.GDU235]   #U235_l
GDEffErr = [Eff.GDU238Err,   #U238
            Eff.GDTh232Err,  #Th232
            Eff.GDU235Err,   #U235
            Eff.GDU238Err,   #U238_l
            Eff.GDTh232Err,  #Th232_l
            Eff.GDU235Err]   #U235_l
GDErr = [[], #U238
         [], #Th232
         [], #U235
         [], #U238_l
         [], #Th232_l
         []] #U235_l
GDIsoBG = [[], #U238
           [], #Th232
           [], #U235
           [], #U238_l
           [], #Th232_l
           []] #U235_l
def ErrProp(EffErr, Eff, BG):
    if Eff != 0:
        centErr = EffErr/Eff
        Err = BG*centErr
    else:
        Err = 0
    return Err
def GDAct(PPM):
    mass = np.pi*pow(TankR, 2)*(2*Height)*1e3
    const = mass*0.002
    IsoAct = list(range(len(PPM)))
    for i in range(len(PPM)):
        IsoAct[i] = PPM[i]*const
        print('Activit of ' + Iso[i] + ' = %.5e x %.5e = %.5e' % (PPM[i], const, IsoAct[i]))
    return IsoAct
Activity = GDAct(PPM)
def BGrate():
    for i in range(len(IsoDecay)):
        for x in range(len(IsoDecay[i])):
            if IsoDecay[i][x] == 'Tl210':
                GDIsoBG[i].append(Activity[i]*GDIsoEff[i][x]*0.002)
            else:
                GDIsoBG[i].append(Activity[i]*GDIsoEff[i][x])
        #print(GDEffErr[i][x])
        #print(GDIsoEff[i][x])
        #print(GDIsoBG[i][x])
            GDErr[i].append(ErrProp(GDEffErr[i][x], GDIsoEff[i][x], GDIsoBG[i][x]))
        #print(GDErr)
            print('BG rate for ' + IsoDecay[i][x] + ' = %.5e +/- %.5e' % (GDIsoBG[i][x], GDErr[i][x]))
BGrate()

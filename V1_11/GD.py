import numpy as np
from math import pow
import Eff
TankR = 10026.35e-3
Height = 10026.35e-3
PPM = [1, 1, 1, 1, 1, 1]
IsoAct = PPM
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
IsoEff = [Eff.GDU238,   #U238
            Eff.GDTh232,  #Th232
            Eff.GDU235,   #U235
            Eff.GDU238,   #U238_l
            Eff.GDTh232,  #Th232_l
            Eff.GDU235]   #U235_l
EffErr = [Eff.GDU238Err,   #U238
            Eff.GDTh232Err,  #Th232
            Eff.GDU235Err,   #U235
            Eff.GDU238Err,   #U238_l
            Eff.GDTh232Err,  #Th232_l
            Eff.GDU235Err]   #U235_l
Err = [[], #U238
         [], #Th232
         [], #U235
         [], #U238_l
         [], #Th232_l
         []] #U235_l
IsoBG = [[], #U238
           [], #Th232
           [], #U235
           [], #U238_l
           [], #Th232_l
           []] #U235_l
def ErrProp(IsoEffErr, IsoEff, BG):
    if IsoEff != 0:
        centErr = IsoEffErr/IsoEff
        IsoErr = BG*centErr
    else:
        IsoErr = 0
    return IsoErr
def setPPM():
    for i in range(len(Iso)):
        try:
            a = input('Input PPM for ' + Iso[i] + ': ')
            a >= 0
            PPM[i] = a
            print('PPM for ' + Iso[i] + ' = %.5e' % PPM[i])
        except:
            print('PPM for ' + Iso[i] + ' set to default value of = %.5e' % PPM[i])
def setEff():
    for i in range(len(IsoDecay)):
        print(Iso[i] + ' chain')
        for x in range(len(IsoDecay[x])):
            try:
                a = input('Input Efficiency for ' + IsoDecay[i][x] + ': ')
                a >= 0
                IsoEff[i][x] = a
                print('Efficiency for ' + IsoDecay[i][x] + ' = %.5e' % IsoEff[i][x])
            except:
                print('Efficiency for ' + IsoDecay[i][x] + ' set to default value of = %.5e' % IsoEff[i][x])
def Activity(PPM):
    mass = np.pi*pow(TankR, 2)*(2*Height)*1e3
    const = mass*0.002
    IsoAct = list(range(len(PPM)))
    for i in range(len(PPM)):
        IsoAct[i] = PPM[i]*const
        print('Activity of ' + Iso[i] + ' = %.5e x %.5e = %.5e' % (PPM[i], const, IsoAct[i]))
def BGrate():
    t = 0
    for i in range(len(IsoDecay)):
        for x in range(len(IsoDecay[i])):
            if IsoDecay[i][x] == 'Tl210':
                IsoBG[i].append(IsoAct[i]*IsoEff[i][x]*0.002)
            else:
                IsoBG[i].append(IsoAct[i]*IsoEff[i][x])
            Err[i].append(ErrProp(EffErr[i][x], IsoEff[i][x], IsoBG[i][x]))
            print('BG rate for ' + IsoDecay[i][x] + ' = %.5e +/- %.5e' % (IsoBG[i][x], Err[i][x]))
        t += sum(IsoBG[i])
    return t
#print('No Errors')

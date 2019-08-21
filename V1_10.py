#imports
import numpy as np
from math import log, pow
import os
#dim vars
bgi = False
#Isotope properties
Ms = [3.953e-25, 3.853145e-26, 6.636286e-26] #[U238, Th232, K40] kg per atom
Lam = [4.916e-18, 1.57e-18, 1.842e-18] #[U238, Th232, K40] decay constant
halfL = list(range(len(Lam)))
for i in range(len(Lam)):
    halfL[i] = (log(2)/Lam[i])/(60**2*24*365*1e9) #half life in billions of years
Abs = [0.992745, 1.0, 0.00117] #[U238, Th232, K40] Natural Abundance
#measurements
TankR = 10026.35e-3 #m
Height = 10026.35e-3 #m
SThick = 6.35e-3 #m
#User input
InType = ['PPM', 'Activity', 'Efficiency', 'Signal Rate']
Iso = [['U238', 'Th232', 'K40'], #[[PMT], 
       ['U238', 'Th232', 'K40'], # [VETO], 
       ['U238', 'Th232', 'K40', 'Co60', 'Cs137'], # [TANK],
       ['U238', 'Th232', 'K40'], # [CONCRETE], 
       ['U238', 'Th232', 'K40'], # [ROCK],
       ['U238', 'Th232', 'U235','U238_l', 'Th232_l', 'U235_l']] #[WATER]]
IsoDefault = [[0.043, 0.133, 16], #[[PMT],
              [0.043, 0.133, 36], # [VETO],
              [0, 0, 0, 19e-3, 0.77e-3], # [TANK],
              [61, 30, 493],      # [CONCRETE],
              [0.067, 0.125,1130],# [ROCK]
              [10, 0.2, 0.25, 0.28, 0.35, 1.7]] # [WATER]]
Comp = ['PMT', 'VETO', 'TANK', 'CONCRETE', 'ROCK', 'Gd WATER']
def InputVals(IType, isotope, component, x):
    """
        IType = Input Type (str)
        isotope = Isotope (str)
        component = Component (str)
        x = default value of PPM for the specified Isotope in the specified component (float)
    """
    try:
        i = float(input('Input Value of ' + IType + ' of the ' + isotope + ' isotope for ' + component + ' component: '))
        print(IType + ' of ' + isotope + ' for ' + component + ' set to value of %.5e' % i)
    except:
        i = x
        print(IType + ' of ' + isotope + ' for ' + component + ' set to default value of %.5e' % x)
    return i
def disdefval(IType, isotope, component, x):
    print(IType + ' of ' + isotope + ' for ' + component + ' set to default value of %.5e' % x)
def clear():
    ui = ""
    while ui.lower() != 'y' or ui.lower() != 'n':
        ui = input('Do you want to clear the output? [y/n] ')
        if ui.lower() == 'y':
            os.system('clc' if os.name == 'nt' else 'clear')
            break
        if ui.lower() == 'n':
            break
#######################################################################
#Background activity from Glass in PMTs
def PMTAct(PPM): #done
    #def mass
    mass = 1.4 #kg - mass of glass in PMT
    #DimVars
    n = 3542
    IsoAct = list(range(len(Iso[0])))
    for i in range(len(PPM)):
        IsoAct[i] = (Lam[i]*PPM[i])/(Ms[i]*1e6*Abs[i])*mass*n
    return IsoAct
#######################################################################
#Background Activity from VETO Region
def VETOAct(PPM): #done
    #def mass
    mass = 1.4 #kg
    #Dim Vars
    n = 354
    IsoAct = list(range(len(Iso[1])))
    for i in range(len(Iso[1])):
                IsoAct[i] += (Lam[i]*PPM[i])/(Ms[i]*1e6*Abs[i])*mass*n
    return IsoAct
#######################################################################
#Background Activity from Steel Tank
def TankAct(Act): #done
    #def mass
    vol = (np.pi*Height*TankR**2) - (np.pi*(Height-2*SThick)*(TankR-(SThick**2))) #def this - use load.py defaults
    den = 8000 #kg/m^3
    mass = vol * den
    #dim other vars
    Act = IsoAct = list(range(len(Iso[2])))
    #print('##################################################')
    #print('Activity of Tank')
    for i in range(len(Act)):
         IsoAct[i] = Act[i]*mass
    return IsoAct
#######################################################################
#Background Activity from concrete
def ConcAct(Act): #done 
    #def mass
    vol = 25.5*(np.pi*pow(13.,2)-np.pi*pow(12.5,2))+0.5*np.pi*pow(13.,2)
    den = 2300 #kg/m^3
    mass = vol * den
    #defaults
    IsoAct = list(range(len(Iso[3])))
    for i in range(len(Act)):
        IsoAct[i] = Act[i]*mass
    return IsoAct
#######################################################################
#Background Activity from Rock Salt
def RockAct(PPM): #done
    #def mass
    den = 2165 #kg/m^3
    vol = np.pi*((pow(18,2)*35.5)-(pow(13,2)*25.5)) #m^3
    mass = vol*den
    #dim vars
    PPM = IsoAct = list(range(len(Iso[4])))
    #Activity Loop
    for i in range(len(PPM)):
        IsoAct[i] = ((Lam[i]*PPM[i])/(Ms[i]*1e6*Abs[i]))*mass
    return IsoAct
#######################################################################
#Background Activity from Gd Water
def WaterAct(PPM): #done
    #def mass of water
    mass = np.pi*pow(TankR, 2)*(2*Height)*1e-3
    #dim vars
    PPM = IsoAct = list(range(len(Iso[5])))
    for i in range(len(PPM)):
        IsoAct[i] = PPM[i]*mass*0.002
    return IsoAct
#######################################################################
#Efficiences
IsoDecay = [['Pa234', 'Pb214', 'Bi214', 'Bi210', 'Tl210'], #U238 decay chain
            ['Ac228', 'Pb212', 'Bi212', 'Tl208'],          #Th232 decay chain
            ['Th231', 'Fr223', 'Pb211', 'Bi211', 'Tl207'], #U235 decay chain
            ['K40'],                                       #K40 decay chain
            ['Pb214', 'Bi214', 'Bi210', 'Tl210'],          #Rn222 decay chain
            ['Co60'],                                      #Co60 decay chain
            ['Cs137']]                                     #Cs137 decay chain
#######################################################################
##dim vars
#PMT
PMTIsoDecay = [IsoDecay[0], IsoDecay[1], IsoDecay[3]] #[[U238 chain], [Th232 chain], [K40 chain]]
PMTIsoDefault = [[0.000130259, 0, 0.0017544, 0, 0.00501633], #[[Pa234, Pb214, Bi214, Bi210, Tl210], 
                 [0, 0, 0, 0.0210737],                       #[Ac228, Pb212, Bi212, Tl208]
                 [0]]                                        #[K40]]
PMTIsoEff = PMTIsoDefault
#######################################################################
#VETO
VETOIsoDecay = [IsoDecay[0], IsoDecay[1], IsoDecay[3]] #[[U238 chain], [Th232 chain], [K40 chain]]
VETOIsoDefault = [[0, 0, 0, 0, 5.84932e-5], #[[Pa234, Pb214, Bi214, Bi210, Tl210],
                  [0, 0, 0, 0.000612745],   #[Ac228, Pb212, Bi212, Tl208],
                  [0]]                      #[K40]]
VETOIsoEff = VETOIsoDefault
#######################################################################
#TANK
TANKIsoDecay = [IsoDecay[0], IsoDecay[1], IsoDecay[3], IsoDecay[5], IsoDecay[6]]
TANKIsoDefault = [[0, 0, 0, 0, 0], #[[Pa234, Pb214, Bi214, Bi210, Tl210],
                  [0, 0, 0, 0],    #[Ac228, Pb212, Bi212, Tl208],
                  [0],             #[K40],
                  [0],             #[Co60],
                  [0]]             #[Cs137]]
TANKIsoEff = TANKIsoDefault
#######################################################################
#CONCRETE
CONCIsoDecay = [IsoDecay[0], IsoDecay[1], IsoDecay[3]]
CONCIsoDefault = [[0, 0, 0, 0, 0], #[[Pa234, Pb214, Bi214, Bi210, Tl210],
                  [0, 0, 0, 0],    #[Ac228, Pb212, Bi212, Tl208],
                  [0]]             #[K40]]
CONCIsoEff = CONCIsoDefault
#######################################################################
#ROCK
ROCKIsoDecay = [IsoDecay[0], IsoDecay[1], IsoDecay[3]]
ROCKIsoDefault = [[0, 0, 0, 0, 0], #[[Pa234, Pb214, Bi214, Bi210, Tl210],
                [0, 0, 0, 0],       #[Ac228, Pb212, Bi212, Tl208],
                [0]]               #[K40]]
ROCKIsoEff = ROCKIsoDefault
#######################################################################
#WATER
WATERIsoDecay = IsoDecay[4] #Rn222 decay chain
WATERIsoDefault = [0, 0.0171801, 0, 0.113282] #[Pb214, Bi214, Bi210, Tl210]
WATERIsoEff = WATERIsoDefault
#print("WaterIsoEff = ", WATERIsoEff, type(WATERIsoEff))
#######################################################################
#Background Rate
scale = 1/6 #(pow(fiducialRaduis, 2)*fiducialHeight)/(pow(detectorRaduis, 2)*decetorHeight)
#######################################################################
def BGRate():    
    ###################################################################
    #PMTs
    print('##################################################') 
    print('BGR due to PMTs')
    PMTBGIso = list()
    for i in range(len(PMTIsoDecay)):
        for x in range(len(PMTIsoEff[i])):
            PMTBGIso.append(dataAct[0][i]*PMTIsoEff[i][x]/scale)
            print('BGR due to ' + PMTIsoDecay[i][x] + ' =  %.5e'  % PMTBGIso[x]) 
    PMTBGR = sum(PMTBGIso)
    print('Total BGR due to PMTs = %.5e' % PMTBGR)
    ###################################################################
    #VETO
    print('##################################################') 
    print('BGR due to VETO')
    VETOBGIso = list()
    for i in range(len(VETOIsoDecay)):
        for x in range(len(VETOIsoEff[i])):
            VETOBGIso.append(dataAct[1][i]*VETOIsoEff[i][x]/scale)
            print('BGR due to ' + VETOIsoDecay[i][x] + ' = %.5e' % VETOBGIso[x])
    VETOBGR = sum(VETOBGIso)
    print('Total BRG due to Veto = %.5e' % VETOBGR)
    ###################################################################
    #TANK
    print('##################################################') 
    print('BGR due to TANK')
    TANKBGIso = list()
    for i in range(len(TANKIsoDecay)):
        for x in range(len(TANKIsoEff[i])):
            TANKBGIso.append(dataAct[2][i]*TANKIsoEff[i][x]/scale)
            print('BGR due to ' + TANKIsoDecay[i][x] + ' = %.5e' % TANKBGIso[x])
    TANKBGR = sum(TANKBGIso)
    print('Total BGR due to Tank = %.5e' % TANKBGR)
    ###################################################################
    #CONCRETE
    print('##################################################') 
    print('BGR due to CONCRETE')
    CONCBGIso = list()
    for i in range(len(CONCIsoDecay)):
        for x in range(len(CONCIsoEff[i])):
            CONCBGIso.append(dataAct[3][i]*CONCIsoEff[i][x]/scale)
            print('BGR due to ' + CONCIsoDecay[i][x] + ' = %.5e' % CONCBGIso[x])
    CONCBGR = sum(CONCBGIso)
    print('Total BGR due to Concrete = %.5e' % CONCBGR)
    ###################################################################
    #ROCK
    print('##################################################') 
    print('BGR due to ROCK')
    ROCKBGIso = list()
    for i in range(len(ROCKIsoDecay)):
        for x in range(len(ROCKIsoEff[i])):
            ROCKBGIso.append(dataAct[4][i]*ROCKIsoEff[i][x]/scale)
            print('BGR due to ' + ROCKIsoDecay[i][x] + ' = %.5e' % ROCKBGIso[x])
    ROCKBGR = sum(ROCKBGIso)
    print('Total BGR due to Rock = %.5e' % ROCKBGR)
    ###################################################################
    #Gd Water
    print('##################################################') 
    print('BGR due to Gd WATER')
    WATERBGIso = list()
    for i in range(len(WATERIsoDecay)): #1d array
            WATERBGIso.append(dataAct[5][i]*WATERIsoEff[i]/scale)
            print('BGR due to ' + WATERIsoDecay[i] + ' = %.5e' % WATERBGIso[i])
    WATERBGR = sum(WATERBGIso)
    print('Total BGR due to Gd Water = %.5e' % WATERBGR)
    ###################################################################
    #Total
    tot = PMTBGR + VETOBGR + TANKBGR + CONCBGR + ROCKBGR + WATERBGR
    #print('##################################################')
    #print('Total BGR is %.5e' % tot)
    bgi = True
    tot = tot/(60**2*24)
    return tot
IsoShare = [1.41021e-3, 2.87123e-4, 3.28426e-3, 6.56741e-4, 1.40556e-1, 3.94469e-3, 1.77373e-1, 4.24271e-1, 1.36098e-3]
PMTShare = [4.60123e-1, 5.37989e-1, 2.52750e-1, 5.25258e-1, 2.37596e-1, 5.78219e-1, 6.22010e-1, 5.48328e-1, 3.62383e-1, 4.29666e-1]
VETOShare = [3.95017e-1, 4.12636e-1, 2.13334e-1, 4.23952e-1, 2.14290e-1, 3.33691e-1, 3.77990e-1, 4.00277e-1, 2.17803e-1, 3.51135e-1]
TANKShare = [1.44844e-1, 4.79718e-2, 5.01119e-1, 5.07907e-2, 5.15283e-1, 8.44188e-2, 0, 5.05090e-2, 3.83691e-1, 2.08981e-1]
CONCShare = [1.39419e-5, 1.33521e-3, 3.23317e-2, 0, 3.13512e-2, 3.33691e-1, 0, 8.51275e-4, 3.45508e-2, 9.77846e-3]
ROCKShare = [0, 6.84725e-5, 1.46546e-3, 0, 1.48012e-3, 2.23804e-4, 0, 3.54698e-5, 1.57184e-3, 4.40601e-4]
def Max(bg, share):
    for i in range(len(share)):
        BG += bg*IsoShare[i]*share[i]
    return BG
########################################################################Accidental Background
#U238  = [Pa234, Pb214, Bi214, Tl210, Bi210]
#Th232 = [Ac228, Bi212, Pb212, Tl208]
#K40   = [K40]
#PMT
PMT_Pr =  [[3.20946e-4, 0, 3.36027e-3, 9.81119e-3, 0],  #U238 chain
          [2.14329e-5, 3.04153e-4, 0, 3.88494e-2],      #Th232 chain
          [7.42865e-5]]                                 #K40 chain
PMT_Nr =  [[1.75361e-4, 0, 2.58670e-3, 7.23630e-3, 0],  #U238 chain
          [7.07220e-6, 1.73195e-4, 0, 3.02348e-2],      #Th232 chain
          [6.57061e-5]]                                 #K40 chain
#VETO
VETO_Pr = [[0, 0, 4.49260e-5, 1.59123e-4, 0],           #U238 chain
          [0, 0, 0, 9.69449e-4],                        #Th232 chain
          [4.15627e-6]]                                 #K40 chain
VETO_Nr = [[0, 0, 3.94931e-5, 1.19808e-4, 0],           #U238 chain
          [0, 0, 0, 7.49615e-4],                        #Th232 chain
          [0]]                                          #K40
#TANK
TANK_Pr = [[0, 0, 0, 0, 0],                             #U238 chain
          [0, 0, 0, 0],                                 #Th232 chain
          [0]]                                          #K40 chain
TANK_Nr = [[0, 0, 0, 0, 0],                             #U238 chain
          [0, 0, 0, 0],                                 #Th232 chain
          [0]]                                          #K40
#CONC
CONC_Pr = [[0, 0, 0, 0, 0],                             #U238 chain
          [0, 0, 0, 0],                                 #Th232 chain
          [0]]                                          #K40 chain
CONC_Nr = [[0, 0, 0, 0, 0],                             #U238 chain
          [0, 0, 0, 0],                                 #Th232 chain
          [0]]                                          #K40 chain
#ROCK
ROCK_Pr = [[0, 0, 0, 0, 0],                             #U238 chain
          [0, 0, 0, 0],                                 #Th232 chain
          [0]]                                          #K40 chain
ROCK_Nr = [[0, 0, 0, 0, 0],                             #U238 chain
          [0, 0, 0, 0],                                 #Th232 chain
          [0]]                                          #K40
def AccBack(Prate, Nrate):
    timeScale = 0.0001*86400*0.05
    back = 0
    for i in range(len(Prate)):
        for x in range(len(Prate[i])):
            back += Prate[i][x]*Nrate[i][x]*timeScale
    return back
PMT_Acc = AccBack(PMT_Pr, PMT_Nr)
VETO_Acc = AccBack(VETO_Pr, VETO_Nr)
TANK_Acc = AccBack(TANK_Pr, TANK_Nr)
CONC_Acc = AccBack(CONC_Pr, CONC_Nr)
ROCK_Acc = AccBack(ROCK_Pr, ROCK_Nr)
#######################################################################
#k constant
#print('k = ' + str(k))
#events from process (evp?) = total event rate for process (data->GetEntries()) / BGR(=tot) (results.txt, 3rd column from end) <- plot this
#k = (BGR - x) * events from process(^)
#different k for each component
#read off efficiences form histogram - use command in notebook
#######################################################################
ans = ""
ai = False
ei = False
dataAct = list()
for i in range(len(IsoDefault)):
    dataAct.append(IsoDefault[i])
options = ['a', 'e', 'bgr', 'exit', 'td', 'maxbg', 'cb']
#Activity lists initialised to default values
PMTPPM = IsoDefault[0]
VETOPPM = IsoDefault[1]
TANKACT = IsoDefault[2]
CONCACT = IsoDefault[3]
ROCKPPM = IsoDefault[4]
GdWPPM = IsoDefault[5]
def menu(): #menu text
    a = ''
    options = ['a', 'e', 'bgr', 'exit', 'td', 'maxbg', 'cb']
    while a.lower() not in options:
        print('##################################################')
        #os.system('clc' if os.name == 'nt' else 'clear')
        print('WATCHMAN Cleanliness software')
        print('Alex Healey, UoS, 2019')
        print('Options: ')
        print('- Input Values for Activity    [a]')
        print('- Input Values for Efficiency  [e]')
        print('- Calculate Background Rate    [bgr]')
        print('- Calculate Time Detection     [td]')
        print('- Calculate Maximum Background [maxbg]')
        print('- Cleanliness Budget           [cb]')
        print('- Exit software                [exit]')
        a = str(input('Select an option: '))
        if a.lower() in options:
            #print('Option selected')
            #print('Loading...')
            break
    return a
ans = ""
while ans.lower() != "exit":
    ans = menu()
    #Activity
    if ans.lower() == 'a':
        in_ans = ''
        ##UI
        #PMT
        try:
            in_ans = input('Do you want to input values of ' + InType[0] + ' for ' + Comp[0] + ' ? [y/n] ')
            in_ans.lower() == 'y' or in_ans.lower() == 'n'
        except:
            print('Invalid value')
        if in_ans.lower() == 'y':
            print('##################################################')
            print('Input Values of ' + InType[0] + ' for ' + Comp[0] + ': ')
            for i in range(len(PMTPPM)):
                PMTPPM[i] = InputVals(InType[0], Iso[0][i], Comp[0], IsoDefault[0][i])
        elif in_ans.lower() == 'n':
            print('##################################################')
            for i in range(len(PMTPPM)):
                disdefval(InType[0], Iso[0][i], Comp[0], IsoDefault[0][i])
        #VETO
        in_ans = ''
        try:
            in_ans = input('Do you want to input values of ' + InType[0] + ' for ' + Comp[1] + ' ? [y/n] ')
            in_ans.lower() == 'y' or in_ans.lower()  == 'n'
        except:
            print('Invalid Value')
        if in_ans.lower() == 'y':
            print('##################################################')
            print('Input Values of ' + InType[0] + ' for ' + Comp[1] + ': ')
            for i in range(len(VETOPPM)):
                VETOPPM[i] = InputVals(InType[0], Iso[1][i], Comp[1], IsoDefault[1][i])
        elif in_ans.lower()=='n':
            print('##################################################')
            for i in range(len(VETOPPM)):
                disdefval = InputVals(InType[0], Iso[1][i], Comp[1], IsoDefault[1][i])
        #TANK
        in_ans = ''
        try:
            in_ans = input('Do you want to input values of ' + InType[1] + ' for ' + Comp[2] + ' ? [y/n] ')
            in_ans.lower() == 'y' or in_ans.lower() == 'n'
        except:
            print('Invalid Value')
        if ans.lower() == 'y':
            print('##################################################')
            print('Input Values of ' + InType[1] + ' for ' + Comp[2] + ': ')
            for i in range(len(TANKACT)):
                TANKACT[i] = InputVals(InType[1], Iso[2][i], Comp[2], IsoDefault[2][i])
        elif ans.lower() =='n':
            print('##################################################')
            for i in range(len(TANKACT)):
                disdefval(InType[1], Iso[2][i], Comp[2], IsoDefault[2][i])
        #CONCRETE
        in_ans = ''
        try:
            in_ans = input('Do you want to input values of ' + InType[1] + ' for ' + Comp[3] + ' ? [y/n] ')
            in_ans.lower() == 'y' or in_ans.lower() == 'n'
        except:
            print('invalid Value')
        if ans.lower() == 'y':
            print('##################################################')
            print('Input Values of ' + InType[1] + ' for ' + Comp[3] + ': ')
            for i in range(len(CONCACT)):
                CONCACT[i] = InputVals(InType[1], Iso[3][i], Comp[3], IsoDefault[3][i])
        elif ans.lower() == 'n':
            print('##################################################')
            for i in range(len(CONCACT)):
                disdefval(InType[1], Iso[3][i], Comp[3], IsoDefault[3][i])
        #ROCK
        in_ans = ''
        try:
            in_ans = input('Do you want to input values of ' + InType[0] + ' for ' + Comp[4] + ' ? [y/n] ')
            in_ans.lower() == 'y' or in_ans.lower() == 'n'
        except:
            print('Invalid value')
        if in_ans.lower() == 'y':
            print('##################################################')
            print('Input Values of ' + InType[0] + ' for ' + Comp[4] + ': ')
            for i in range(len(ROCKPPM)):
                ROCKPPM[i] = InputVals(InType[0], Iso[4][i], Comp[4], IsoDefault[4][i])
        elif in_ans.lower() == 'n':
            print('##################################################')
            disdefval(InType[0], Iso[4][i], Comp[4], IsoDefault[4][i])
        #Gd WATER
        in_ans = ''
        try:
            in_ans = input('Do you want to input values of ' + InType[0] + ' for ' + Comp[5] + ' ? [y/n] ')
            in_ans.lower() == 'y' or in_ans.lower() == 'n'
        except:
            print('Invalid value')
        if in_ans.lower() == 'y':
            print('##################################################')
            print('Input Values of ' + InType[0] + ' for ' + Comp[5] + ': ')
            for i in range(len(GdWPPM)):
                GdWPPM[i] = InputVals(InType[0], Iso[5][i], Comp[5], IsoDefault[5][i])
        elif in_ans.lower() == 'n':
            print('##################################################')
            disdefval(InType[0], Iso[5][i], Comp[5], IsoDefault[4][i])
        #Get Data
        dataAct[0] = PMTAct(PMTPPM)
        dataAct[1] = VETOAct(VETOPPM)
        dataAct[2] = TankAct(TANKACT)
        dataAct[3] = ConcAct(CONCACT)
        dataAct[4] = RockAct(ROCKPPM)
        dataAct[5] = WaterAct(GdWPPM)
        #output
        i = 0
        for i in range(len(Comp)):
            print('##################################################')
            print('Activity of Isotopes in ' + Comp[i] + ': ')
            for x in range(len(Iso[i])):
                print('   Activity of ' + Iso[i][x] + ' = %.5e Bq' % dataAct[i][x])
        ans = ""
        ai = True
        clear()
        ans = ''
    elif ans.lower() == 'e':
        #PMTs
        in_ans = ''
        try:
            in_ans = input('Do you want to input values of ' + InType[2] + ' for ' + Comp[0] + ' ? [y/n] ')
            in_ans.lower() == 'y' or in_ans.lower() == 'n'
        except:
            print('Invalid value')
        if in_ans.lower() == 'y':
            print('##################################################')    
            print('Efficiency of Isotopes in PMT')
            for i in range(len(PMTIsoDecay)):
                for x in range(len(PMTIsoEff[i])):
                    PMTIsoEff[i][x] = InputVals(InType[2], PMTIsoDecay[i][x], Comp[0], PMTIsoDefault[i][x])
        elif in_ans.lower() == 'n':
            print('##################################################')
            print('Efficiency of Isotopes in PMT')
            for i in range(len(PMTIsoDecay)):
                for x in range(len(PMTIsoEff[i])):
                    disdefval(InType[2], PMTIsoDecay[i][x], Comp[0], PMTIsoDefault[i][x])
        #VETOS
        in_ans = ''
        try:
            in_ans = input('Do you want to input values of ' + InType[2] + ' for ' + Comp[1] + ' ? [y/n] ')
            in_ans.lower() == 'y' or in_ans.lower() == 'n'
        except:
            print('Invalid value')
        if in_ans.lower() =='y':
            print('##################################################')
            print('Efficiency of Isotopes in VETO')
            for i in range(len(VETOIsoDecay)):
                for x in range(len(VETOIsoEff[i])):
                    VETOIsoEff[i][x] = InputVals(InType[2], VETOIsoDecay[i][x], Comp[1], VETOIsoDefault[i][x])
        elif in_ans.lower() == 'n':
            print('##################################################')
            print('Efficiency of Isotopes in VETO')
            for i in range(len(VETOIsoDecay)):
                for x in range(len(VETOIsoEff[i])):
                    disdefval(InType[2], VETOIsoDecay[i][x], Comp[1], VETOIsoDefault[i][x])
        #TANK
        in_ans = ''
        try:
            in_ans = input('Do you want to input values of ' + InType[2] + ' for ' + Comp[2] + ' ? [y/n] ')
            in_ans.lower() == 'y' or in_ans.lower() == 'n'
        except:
            print('Invalid value')
        if in_ans.lower() == 'y':
            print('##################################################')
            print('Efficiency of Isotopes in TANK')
            for i in range(len(TANKIsoDecay)):
                for x in range(len(TANKIsoEff[i])):
                    TANKIsoEff[i][x] = InputVals(InType[2], TANKIsoDecay[i][x], Comp[2], TANKIsoDefault[i][x])
        elif in_ans.lower() == 'n':
            print('##################################################')
            print('Efficiency of Isotopes in TANK')
        #CONCRETE
        print('##################################################')
        print('Efficiency of Isotopes in CONCRETE')
        for i in range(len(CONCIsoDecay)):
            for x in range(len(CONCIsoEff[i])):
                CONCIsoEff[i][x] = InputVals(InType[2], CONCIsoDecay[i][x], Comp[3], CONCIsoDefault[i][x])
         #ROCK
        print('##################################################')
        print('Efficiency of Isotopes in ROCK')
        for i in range(len(ROCKIsoDecay)):
            for x in range(len(ROCKIsoEff[i])):
                ROCKIsoEff[i][x] = InputVals(InType[2], ROCKIsoDecay[i][x], Comp[4], ROCKIsoDefault[i][x])
        #WATER
        print('##################################################')
        print('Efficiency of Isotopes in WATER')
        for i in range(len(WATERIsoDecay)): #1d list
            WATERIsoEff[i] = InputVals(InType[2], WATERIsoDecay[i], Comp[5], WATERIsoDefault[i])
        ei = True
        clear()
        ans = ''
    elif ans.lower() == 'bgr':
        if ai == False:
            print('##################################################')
            print('Setting Activity values to default values')
            for i in range(len(Iso)):
                print('##############################################')
                print('Activity of Isotopes in ' + Comp[i])
                print(i)
                print("len: ", len(Iso[i]))
                for x in range(len(Iso[i])):
                    if i == 2 or i == 3:
                        disdefval(InType[1], Iso[i][x], Comp[i], dataAct[i][x])
                    else:
                        disdefval(InType[0], Iso[i][x], Comp[i], dataAct[i][x])
        else:
            pass
        if ei == False:
            print('##################################################')
            print('Setting Efficiency values to default values')
            #just print out lists as set to default when lists are defined
            #PMT
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[0])
            for i in range(len(PMTIsoDecay)):
                for x in range(len(PMTIsoDefault[i])):
                    disdefval(InType[0], PMTIsoDecay[i][x], Comp[0], PMTIsoDefault[i][x])
        else:
            pass
        #BGR Code
        tot = BGRate()
        ###############################################################
        #Accidental BG Rate
                print('##################################################')
        print('PMT  Accidental background = %.5e' % PMT_Acc)
        print('VETO Accidental background = %.5e' % VETO_Acc)
        print('TANK Accidental background = %.5e' % TANK_Acc)
        print('CONC Accidental background = %.5e' % CONC_Acc)
        print('ROCK Accidental background = %.5e' % ROCK_Acc)
        print('##################################################')
        tot += (PMT_Acc + VETO_Acc + TANK_Acc + CONC_Acc + ROCK_Acc)
        print('Total Backgroud Rate = %.5e' % tot)
        clear()
        ans = ''
    elif ans.lower() == 'td':
        if ai == False:
            print('##################################################')
            print('Setting Activity values to default values')
            for i in range(len(Iso)):
                print('##################################################')
                print('Activity of Isotopes in ' + Comp[i])
                for x in range(len(Iso[i])):
                    if i == 2 or i == 3:
                        disdefval(InType[1], Iso[i][x], Comp[i], dataAct[i][x])
                    else:
                        disdefval(InType[0], Iso[i][x], Comp[i], dataAct[i][x])
        else:
            pass
        if ei == False:
            print('##################################################')
            print('Setting Efficiency values to default values')
            #just print out lists as set to default when lists are defined
            #PMT
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[0])
            for i in range(len(PMTIsoDecay)):
                for x in range(len(PMTIsoDefault[i])):
                    disdefval(InType[0], PMTIsoDecay[i][x], Comp[0], PMTIsoDefault[i][x])
        else:
            pass
        if bgi == False:
            tot = BGRate() + PMT_Acc + VETO_Acc + TANK_Acc + CONC_Acc + ROCK_Acc
        else:
            pass
        try:
            signal = float(input('Input signal rate: '))
            signal < 1
        except:
            signal = 0.5
            print('Signal rate set to default value of %.3e' % signal)
        B = signal*1.035 + tot
        S = signal*0.9
        sigma = 4.65
        t = pow(sigma, 2)*(B+((B+S)/(3/2)))*(1/pow(S,2)) #/((60**2)*24) #[days]
        print('Time to detection @ 3 sigma rate = ' + str(t) + ' days')
        clear()
        ans = ''
    elif ans.lower() == 'maxbg':
        if ai == False:
            print('##################################################')
            print('Setting Activity values to default values')
            for i in range(len(Iso)):
                print('##################################################')
                print('Activity of Isotopes in ' + Comp[i])
                for x in range(len(Iso[i])):
                    if i == 2 or i == 3:
                        disdefval(InType[1], Iso[i][x], Comp[i], dataAct[i][x])
                    else:
                        disdefval(InType[0], Iso[i][x], Comp[i], dataAct[i][x])
        else:
            pass
        if ei == False:
            print('##################################################')
            print('Setting Efficiency values to default values')
            #just print out lists as set to default when lists are defined
            #PMT
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[0])
            for i in range(len(PMTIsoDecay)):
                for x in range(len(PMTIsoDefault[i])):
                    disdefval(InType[0], PMTIsoDecay[i][x], Comp[0], PMTIsoDefault[i][x])
        else:
            pass
        if bgi == False:
            tot = BGRate() + PMT_Acc + VETO_Acc + TANK_Acc + CONC_Acc + ROCK_Acc
        else:
            pass
        #signal input
        try:
            signal = input('Input signal rate: ')
            print('Signal rate set to value of %.3e' % s)
        except:
            signal = 0.5
            print('Signal rate set to default value of %.3e' % s)
        #get number of days
        try:
            days = input('Input time dection in days: ')
            print('Time dection set to value of %.5e days' % days)
        except:
            days = 1
            print('Time dection set to default value of %.3e days' % days)
        #def sigma
        sigma = 4.65
        S = signal*0.9
        Mbg = (1/5)*(((3*days*pow(S,2))/(pow(sigma,2))) - 2*S)
        print('Maximum Background for this time dection @ 3 sigma rate is %.5e' % Mbg)
        clear()
        ans = ''
    elif ans.lower() == 'cb':
        IsoShare = [7.90973e-02, 8.87580e-2, 1.61053e-02, 1.84219e-01, 1.60078e-3, 8.42900e-02, 2.49073e-01, 3.68388e-02, 1.83681e-1, 7.63377e-2] 
        Iso_cb_labels = ['Pa234', 'Ac228', 'Pb214', 'Bi214', 'Pb212', 'Bi212', 'Tl210', 'Bi210', 'Tl208', 'K40'] 
        Iso_cb = list()
        PMT_Iso = [4.60125e-01, 3.49298e-01, 5.37989e-01, 2.51743e-01, 5.59632e-01, 4.30561e-01, 2.37596e-01, 5.25258e-01, 3.875000e-01, 4.29666e-01]
        VETO_Iso = [3.95017e-01, 2.59425e-01, 4.12636e-01, 2.13328e-01, 4.34460e-01, 3.65216e-01, 2.14290e-01, 4.23952e-01, 3.81624e-01, 3.51135e-01]
        TANK_Iso = [1.44844e-01, 3.73504e-01, 4.79718e-02, 5.01133e-01, 5.90822e-03, 1.95711e-01, 5.15283e-01, 5.07907e-02, 1.12262e-01, 2.08981e-01]
        CONC_Iso = [1.39419e-05, 2.59425e-01, 1.33521e-03, 3.23309e-02, 0, 4.32656e-03, 3.13512e-02, 0, 1.12262e-01, 9.77846e-03]
        ROCK_Iso = [0, 4.96978e-04, 6.84725e-05, 1.46542e-03, 0, 4.18658e-03, 1.48012e-03, 0, 6.35248e-03, 4.40601e-04]
        PMT_BG_CB = 0
        VETO_BG_CB = 0
        TANK_BG_CB = 0
        CONC_BG_CB = 0
        ROCK_BG_CB = 0
        #signal input
        try:
            signal = float(input('Input signal rate: '))
            print('Signal rate set to value of %.3e' % s)
        except:
            signal = 0.5
            print('Signal rate set to default value of %.3e' % s)
        #get number of days
        try:
            days = float(input('Input time dection in days: '))
            print('Time dection set to value of %.3e days' % days)
        except:
            days = 1
            print('Time dection set to default value of %.3e days' % days)
        #def sigma
        B = signal*1.035 + tot
        S = signal*0.9
        sigma = 4.65
        t = pow(sigma, 2)*(B+((B+S)/(3/2)))*(1/pow(S,2)) #/((60**2)*24) #[days]
        print('Time to detection @ 3 sigma rate = ' + str(t) + ' days')
        Mbg = ((1/5)*(((3*days*pow(S,2))/(pow(sigma,2))) - 2*S))
        print('Maximum Background for this time dection @ 3 sigma rate is %.5e' % Mbg)
        print('##################################################')
        for i in range(len(IsoShare)):
            Iso_cb.append(Mbg*IsoShare[i])
            print(Iso_cb_labels[i] + ' = %.5e' % Iso_cb[i])
        print('##################################################')
        for i in range(len(PMT_Iso)):
            PMT_BG_CB += Iso_cb[i]*PMT_Iso[i]
        print('Max BG from PMT = %.5e' % PMT_BG_CB)
        print('##################################################')
        for i in range(len(VETO_Iso)):
            VETO_BG_CB += Iso_cb[i]*VETO_Iso[i]
        print('Max BG from VETO = %.5e' % VETO_BG_CB)
        print('##################################################')
        for i in range(len(TANK_Iso)):
            TANK_BG_CB += Iso_cb[i]*TANK_Iso[i]
        print('Max BG from TANK = %.5e' % TANK_BG_CB)
        print('##################################################')
        for i in range(len(CONC_Iso)):
            CONC_BG_CB += Iso_cb[i]*CONC_Iso[i]
        print('Max BG from CONC = %.5e' % CONC_BG_CB)
        print('##################################################')
        for i in range(len(ROCK_Iso)):
            ROCK_BG_CB += Iso_cb[i]*ROCK_Iso[i]
        print('Max BG from ROCK = %.5e' % ROCK_BG_CB)
        print('##################################################')
        print('Total = %.5e' % (PMT_BG_CB + VETO_BG_CB + TANK_BG_CB + CONC_BG_CB + ROCK_BG_CB))
        diff = (Mbg - (PMT_BG_CB + VETO_BG_CB + TANK_BG_CB + ROCK_BG_CB))
        print('Abs Diff = %.5e' %  diff)
        print('Percent Diff = %.5e' % (diff/Mbg))
        print('##################################################')
        clear()
        ans = ''
    elif ans.lower() == 'exit':
        break

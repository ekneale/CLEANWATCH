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
        print(IType + ' of ' + isotope + ' for ' + component + ' set to value of %.3e' % i)
    except:
        i = x
        print(IType + ' of ' + isotope + ' for ' + component + ' set to default value of %.3e' % x)
    return i
def disdefval(IType, isotope, component, x):
    print(IType + ' of ' + isotope + ' for ' + component + ' set to default value of %.3e' % x)
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
scale = 1e-4 # fid_vol/Sigma(vol)
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
            print('BGR due to ' + PMTIsoDecay[i][x] + ' =  %.3e'  % PMTBGIso[x]) 
    PMTBGR = sum(PMTBGIso)
    print('Total BGR due to PMTs = %.3e' % PMTBGR)
    ###################################################################
    #VETO
    print('##################################################') 
    print('BGR due to VETO')
    VETOBGIso = list()
    for i in range(len(VETOIsoDecay)):
        for x in range(len(VETOIsoEff[i])):
            VETOBGIso.append(dataAct[1][i]*VETOIsoEff[i][x]/scale)
            print('BGR due to ' + VETOIsoDecay[i][x] + ' = %.3e' % VETOBGIso[x])
    VETOBGR = sum(VETOBGIso)
    print('Total BRG due to Veto = %.3e' % VETOBGR)
    ###################################################################
    #TANK
    print('##################################################') 
    print('BGR due to TANK')
    TANKBGIso = list()
    for i in range(len(TANKIsoDecay)):
        for x in range(len(TANKIsoEff[i])):
            TANKBGIso.append(dataAct[2][i]*TANKIsoEff[i][x]/scale)
            print('BGR due to ' + TANKIsoDecay[i][x] + ' = %.3e' % TANKBGIso[x])
    TANKBGR = sum(TANKBGIso)
    print('Total BGR due to Tank = %.3e' % TANKBGR)
    ###################################################################
    #CONCRETE
    print('##################################################') 
    print('BGR due to CONCRETE')
    CONCBGIso = list()
    for i in range(len(CONCIsoDecay)):
        for x in range(len(CONCIsoEff[i])):
            CONCBGIso.append(dataAct[3][i]*CONCIsoEff[i][x]/scale)
            print('BGR due to ' + CONCIsoDecay[i][x] + ' = %.3e' % CONCBGIso[x])
    CONCBGR = sum(CONCBGIso)
    print('Total BGR due to Concrete = %.3e' % CONCBGR)
    ###################################################################
    #ROCK
    print('##################################################') 
    print('BGR due to ROCK')
    ROCKBGIso = list()
    for i in range(len(ROCKIsoDecay)):
        for x in range(len(ROCKIsoEff[i])):
            ROCKBGIso.append(dataAct[4][i]*ROCKIsoEff[i][x]/scale)
            print('BGR due to ' + ROCKIsoDecay[i][x] + ' = %.3e' % ROCKBGIso[x])
    ROCKBGR = sum(ROCKBGIso)
    print('Total BGR due to Rock = %.3e' % ROCKBGR)
    ###################################################################
    #Gd Water
    print('##################################################') 
    print('BGR due to Gd WATER')
    WATERBGIso = list()
    for i in range(len(WATERIsoDecay)): #1d array
            WATERBGIso.append(dataAct[5][i]*WATERIsoEff[i]/scale)
            print('BGR due to ' + WATERIsoDecay[i] + ' = %.3e' % WATERBGIso[i])
    WATERBGR = sum(WATERBGIso)
    print('Total BGR due to Gd Water = %.3e' % WATERBGR)
    ###################################################################
    #Total
    tot = PMTBGR + VETOBGR + TANKBGR + CONCBGR + ROCKBGR + WATERBGR
    print('##################################################')
    print('Total BGR is %.3e' % tot)
    bgi = True
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
#Activity UI
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
        print('- Input Values for Activity [a]')
        print('- Input Values for Efficiency [e]')
        print('- Calculate Background Rate [bgr]')
        print('- Calculate Time Detection [td]')
        print('- Calculate Maximum Background [maxbg]')
        print('- Cleanliness Budget [cb]')
        print('- Exit software [exit]')
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
        ##UI
        #PMT
        print('##################################################')
        print('Input Values of ' + InType[0] + ' for ' + Comp[0] + ': ')
        for i in range(len(PMTPPM)):
            PMTPPM[i] = InputVals(InType[0], Iso[0][i], Comp[0], IsoDefault[0][i])
        #VETO
        print('##################################################')
        print('Input Values of ' + InType[0] + ' for ' + Comp[1] + ': ')
        for i in range(len(VETOPPM)):
            VETOPPM[i] = InputVals(InType[0], Iso[1][i], Comp[1], IsoDefault[1][i])
        #TANK
        print('##################################################')
        print('Input Values of ' + InType[1] + ' for ' + Comp[2] + ': ')
        for i in range(len(TANKACT)):
            TANKACT[i] = InputVals(InType[1], Iso[2][i], Comp[2], IsoDefault[2][i])
        #CONCRETE
        print('##################################################')
        print('Input Values of ' + InType[1] + ' for ' + Comp[3] + ': ')
        for i in range(len(CONCACT)):
            CONCACT[i] = InputVals(InType[1], Iso[3][i], Comp[3], IsoDefault[3][i])
        #ROCK
        print('##################################################')
        print('Input Values of ' + InType[0] + ' for ' + Comp[4] + ': ')
        for i in range(len(ROCKPPM)):
            ROCKPPM[i] = InputVals(InType[0], Iso[4][i], Comp[4], IsoDefault[4][i])
        #Gd WATER
        print('##################################################')
        print('Input Values of ' + InType[0] + ' for ' + Comp[5] + ': ')
        for i in range(len(GdWPPM)):
            GdWPPM[i] = InputVals(InType[0], Iso[5][i], Comp[5], IsoDefault[5][i])
            #print(i)
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
                print('   Activity of ' + Iso[i][x] + ' = %.3e Bq' % dataAct[i][x])
        ans = ""
        ai = True
        clear()
        ans = ''
    elif ans.lower() == 'e':
        #PMTs
        print('##################################################')    
        print('Efficiency of Isotopes in PMT')
        for i in range(len(PMTIsoDecay)):
            for x in range(len(PMTIsoEff[i])):
                PMTIsoEff[i][x] = InputVals(InType[2], PMTIsoDecay[i][x], Comp[0], PMTIsoDefault[i][x])
        #VETOS
        print('##################################################')
        print('Efficiency of Isotopes in VETO')
        for i in range(len(VETOIsoDecay)):
            for x in range(len(VETOIsoEff[i])):
                VETOIsoEff[i][x] = InputVals(InType[2], VETOIsoDecay[i][x], Comp[1], VETOIsoDefault[i][x])
        #TANK
        print('##################################################')
        print('Efficiency of Isotopes in TANK')
        for i in range(len(TANKIsoDecay)):
            for x in range(len(TANKIsoEff[i])):
                TANKIsoEff[i][x] = InputVals(InType[2], TANKIsoDecay[i][x], Comp[2], TANKIsoDefault[i][x])
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
        ans = ""
        ei = True
        clear()
        ans = ''
    elif ans.lower() == 'bgr':
        if ai == False:
            print('##################################################')
            print('Setting Activity values to default values')
            for i in range(len(Iso)):
                print('##################################################')
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
            tot = BGRate()
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
        t = pow(sigma, 2)*((2*B+S)/(3/2))*(1/pow(S,2))/((60**2)*24) #[days]
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
            tot = BGRate()
        else:
            pass
        #signal input
        try:
            s = float(input('Input signal rate: '))
            print('Signal rate set to value of %.3e' % s)
        except:
            s = 0.5
            print('Signal rate set to default value of %.3e' % s)
        #get number of days
        try:
            days = int(input('Input time dection in days: '))
            print('Time dection set to value of %.3e days' % days)
        except:
            days = 1
            print('Time dection set to default value of %.3e days' % days)
        #def sigma
        sigma = 4.65
        Mbg = (1/2)*(((3*pow(s, 2)*days*pow(60,2)*24)/(2*pow(sigma,2)))-s)
        print('Maximum Background for this time dection @ 3 sigma rate is %.3e' % Mbg)
        clear()
        ans = ''
    elif ans.lower() == 'cb':
        k = [0.2, 0.2, 0.2, 0.1, 0.1, 0.2] #[PMT, VETO, TANK, CONC, ROCK, WATER]
        #signal input
        try:
            s = float(input('Input signal rate: '))
            print('Signal rate set to value of %.3e' % s)
        except:
            s = 0.5
            print('Signal rate set to default value of %.3e' % s)
        #get number of days
        try:
            days = float(input('Input time dection in days: '))
            print('Time dection set to value of %.3e days' % days)
        except:
            days = 1
            print('Time dection set to default value of %.3e days' % days)
        #def sigma
        sigma = 4.65
        Mbg = (1/2)*(((3*pow(s, 2)*days*pow(60,2)*24)/(2*pow(sigma,2)))-s)
        print('Maximum Background for this time dection @ 3 sigma rate is %.3e' % Mbg)
        print('##################################################')
        #for PMT
        PMTR = Mbg/k[0]
        print('Max Rate from PMT = %.3e' % PMTR)
        #get rates for different isotopes
        #PMTIsoAct = list()
        #for i in range(len(IsoEff[0])):
        #    PMTIsoAct.append()
        ##for VETO
        VETOR = Mbg/k[1]
        print('Max Rate from VETO = %.3e' % VETOR)
        ##for TANK
        TANKR = Mbg/k[2]
        print('Max Rate from TANK = %.3e' % TANKR)
        ##for CONCRETE
        CONCR = Mbg/k[3]
        print('Max Rate from CONCRETE = %.3e' % CONCR)
        ##For ROCK
        ROCKR = Mbg/k[4]
        print('Max Rate from ROCK = %.3e' % ROCKR)
        ##For Water
        GdWATERR = Mbg/k[5]
        print('Max Rate from Gd Water = %.3e' % GdWATERR)
        #clear
        clear()
        ans = ''
    elif ans.lower() == 'exit':
        break


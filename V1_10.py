#imports
import numpy as np
from math import log, pow
import os
from ast import literal_eval
import Eff
import Prate as Pr
import Nrate as Nr
#dim vars
bgi = False
######Isotope properties############################
Ms = [3.953e-25, 3.853145e-25, 6.636286e-26] #[U238, Th232, K40] kg per atom
Lam = [4.916e-18, 1.57e-18, 1.842e-18] #[U238, Th232, K40] decay constant
halfL = list(range(len(Lam)))
for i in range(len(Lam)):
    halfL[i] = (log(2)/Lam[i])/(60**2*24*365*1e9) #half life in billions of years
Abs = [1, 1, 0.00117] #[U238, Th232, K40] Natural Abundance
#####measurements###################################
TankR = 10026.35e-3 #m
Height = 10026.35e-3 #m
SThick = 6.35e-3 #m
RN = 0.01 #radionuclides events per day
FN = 0.02 #rock events per day
######User input Type###############################
InType = ['PPM', 'Activity', 'Efficiency', 'Signal Rate']
Iso = [['U238', 'Th232', 'K40'], #[[PMT], 
       ['U238', 'Th232', 'K40'], # [VETO], 
       ['U238', 'Th232', 'K40', 'Co60', 'Cs137'], # [TANK],
       ['U238', 'Th232', 'K40'], # [CONCRETE], 
       ['U238', 'Th232', 'K40', 'Fast Neutron'], # [ROCK],
       ['Rn222','RadioNuclide'], # [WATER],
       ['U238', 'Th232', 'U235', 'U238_l', 'Th232_l', 'U235_l']] # [GD]]
IsoDecay = [['Pa234', 'Pb214', 'Bi214', 'Bi210', 'Tl210'], #U238 decay chain
            ['Ac228', 'Pb212', 'Bi212', 'Tl208'],          #Th232 decay chain
            ['Th231', 'Fr223', 'Pb211', 'Bi211', 'Tl207'], #U235 decay chain
            ['K40'],                                       #K40 decay chain
            ['Pb214', 'Bi214', 'Bi210', 'Tl210'],          #Rn222 decay chain
            ['Co60', 'Cs137']]
IsoDefault = [[0.043, 0.133, 36], #[[PMT], [U238(ppm), Th232(ppm), K40(ppm)]
              [0.043, 0.133, 36], # [VETO], [U238(ppm), Th232(ppm), K40(ppm)]
              [0.17, 3.8e-3, 34e-3, 14e-3, 4e-3], # [TANK], [U238 (1.4e-3ppm), Th232(0.93e-3ppm), K40(Bq/kg), Co60(Bq/kg), Cs137(Bq/kg)]
              [61, 30, 493],      # [CONCRETE], [U238(Bq/kg), Th232(Bq/kg), K40(Bq/kg)]
              [10e-3, 220e-3, 750, 0.02],# [ROCK], [U238(ppm), Th232(ppm), K40(ppm), fast neutrons(events per day)] 
              [0.002,0.01], #[WATER], [Rn222(Bqm-3), radionuclides(events per day)]
              [10e-3, 0.2e-3, 0.25e-3, 0.28e-3, 0.35e-3, 1.7e-3]] #[GD](Bq/kg)] [
######Components###################################
Comp = ['PMT', 'VETO', 'TANK', 'CONCRETE', 'ROCK','WATER', 'GD']
######menu func####################################
def menu(): #menu text
    """
    Displays options
    """
    a = ''
    options = ['a', 'e', 'bgr', 'exit', 'td', 'maxbg', 'cb']
    while a.lower() not in options:
        print('##################################################')
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
        print('##################################################')
        a = str(input('Select an option: '))
        if a.lower() in options and a.lower() != 'exit':
            print('Option selected')
            print('Loading...')
            break
    return a
######Input func###################################
def InputVals(IType, isotope, component, x):
    """
        IType = Input Type (str)
        isotope = Isotope (str)
        component = Component (str)
        x = default value of PPM for the specified Isotope in the specified component (float)
    """
    try:
        i = literal_eval(input('Input Value of ' + IType + ' of the ' + isotope + ' isotope for ' + component + ' component: '))
        print(IType + ' of ' + isotope + ' for ' + component + ' set to value of %.5e' % i)
    except:
        i = x
        print(IType + ' of ' + isotope + ' for ' + component + ' set to default value of %.5e' % x)
    return i
######Display default value func###################
#TODO add in GdAct
def disdefval(IType, isotope, component, x):
    print(IType + ' of ' + isotope + ' for ' + component + ' set to default value of %.5e' % x)
######Check input##################################
def inputcheck(Itype, comp):
    opts = ['y', 'n']
    ians = ''
    while ians.lower() not in opts:
        ians = input('Do you want to input values of '+ Itype + ' for ' + comp + '? [y/n] ')
        if ians.lower() in opts:
            break
        else:
            print('Invalid Value')
    return ians.lower()
######Clear display func###########################
def clear():
    """
    Clears output
    """
    ui = ""
    while ui.lower() != 'y' or ui.lower() != 'n':
        ui = input('Do you want to clear the output? [y/n] ')
        if ui.lower() == 'y':
            os.system('clc' if os.name == 'nt' else 'clear')
            break
        if ui.lower() == 'n':
            break
#####shareFunc#####################################
def share(total, Iso):
    IsoShare = Iso
    if isinstance(Iso[0], list) == True:
        for i in range(len(Iso)):
            for x in range(len(Iso[i])):
            #x = np.argmax(Iso[i])
                IsoShare[i][x] = Iso[i][x]/(total/0.05/0.0001)
    elif isinstance(Iso[0], list) == False:
        #i = np.argmax(Iso)
        for i in range(len(Iso)):
            IsoShare[i] = Iso[i]/(total/0.05/0.0001)
    return IsoShare
#####Background activity from Glass in PMTs########
def PMTAct(PPM): #done
    """
    Calculates the background activity for the PMTs
    Decay Chains: U238, Th232, K40 
    PPM = Parts per 1e6 for Isotope
    """
    #def mass
    mass = 1.4 #kg - mass of glass in PMT
    #DimVars
    n = 3258 #number of PMTs
    IsoAct = list(range(len(Iso[0])))
    for i in range(len(IsoAct)):
        IsoAct[i] = ((Lam[i]*PPM[i]*Abs[i])/(Ms[i]*1e6))*mass*n
    return IsoAct
######Reverse BG for PMT func######################
def revPMTAct(BGIso, IsoEff):
    Act = list()
    mass = 1.4 #kg - mass of glass in PMT
    n = 3258 #number of PMTs
    for i in range(len(BGIso)):
        x = np.argmax(BGIso[i])
        Act.append(((BGIso[i][x]/(mass*n*Abs[i]))*((Ms[i]*(1e6))/(Lam[i])))/(IsoEff[i][x]*0.0001*0.05))
    return Act
#####Background Activity for VETO Region###########
def VETOAct(PPM): #done
    """
    Calculates the background activity for the VETO region
    Decay Chains: U238, Th232, K40
    PPM: Parts per 1e6 for Isotope
    """
    #def mass
    mass = 1.4 #kg
    #Dim Vars
    n = 296
    IsoAct = list(range(len(Iso[1])))
    for i in range(len(Iso[1])):
        IsoAct[i] = (Lam[i]*PPM[i]*Abs[i])/(Ms[i]*1e6)*mass*n
    return IsoAct
#####Reverse BG for VETO func######################
def revVETOAct(BGIso, IsoEff):
    Act = list()
    mass = 1.4 #kg
    n = 296
    for i in range(len(BGIso)):
        x = np.argmax(BGIso[i])
        Act.append(((BGIso[i][x]/(mass*n*Abs[i]))*((Ms[i]*1e6)/Lam[i]))/(IsoEff[i][x]*0.0001*0.05))
    return Act
#####Background Activity from Steel Tank###########
def TankAct(Act): #done
    """
    Calculates the background activity for the Steel Tank
    Decay Chains: U238, Th232, K40, Co60 Cs137
    Act: Activity of the Isotope
    """
    #def mass
    vol = np.pi*2*Height*TankR**2 - np.pi*2*(Height-SThick)*pow(TankR-SThick,2) 
    den = 8000 #kg/m^3
    mass = vol * den
    #dim other vars
    IsoAct = list(range(len(Iso[2])))
    for i in range(len(IsoAct)):
         IsoAct[i] = Act[i]*mass
    return IsoAct
#####Reverse BG for TANK func######################
def revTankAct(BGIso, IsoEff):
    Act = list()
    vol = np.pi*2*Height*pow(TankR,2) - np.pi*2*(Height-SThick)*pow(TankR-SThick,2)
    den = 8000 #kg/m^3
    mass = vol * den
    for i in range(len(BGIso)):
        Act.append(BGIso[i][0]/mass/(IsoEff[i][0]*0.0001*0.05))
    return Act
#####Background Activity from concrete#############
def ConcAct(Act): #done
    """
    Calculates the background activity for the Concrete
    Decay Chains: U238, Th232, K40
    Act: Activity of the Isotope
    """
    #def mass
    vol = 25.5*(np.pi*pow(13.,2)-np.pi*pow(12.5,2))+0.5*np.pi*pow(13.,2)
    den = 2300 #kg/m^3
    mass = vol * den
    #defaults
    IsoAct = list(range(len(Iso[3])))
    for i in range(len(Act)):
        IsoAct[i] = Act[i]*mass
    return IsoAct
#####Reverse BG for CONC func######################
def revCONCAct(BGIso, IsoEff):
    Act = list()
    vol = 25.5*(np.pi*pow(13.,2)-np.pi*pow(12.5,2))+0.5*np.pi*pow(13.,2)
    den = 2300 #kg/m^3
    mass = vol * den
    for i in range(len(BGIso)):
        x = np.argmax(BGIso[i])
        Act.append(BGIso[i][x]/mass/(IsoEff[i][x]*0.0001*0.05))
    return Act
#####Background Activity from Rock Salt############
def RockAct(PPM): #done
    """
    Calculates the background activity for the Rock Salt
    Decay Chains: U238, Th232, K40
    PPM: Parts per 1e6 for Isotope
    """
    #def mass
    den = 2165 #kg/m^3
    vol = np.pi*((pow(18,2)*35.5)-(pow(13,2)*25.5)) #m^3
    mass = vol*den
    #dim vars
    IsoAct = list(range(len(Iso[4])-1))
    #Activity Loop
    for i in range(len(PPM)-1):
        IsoAct[i] = ((Lam[i]*PPM[i])/(Ms[i]*1e6))*mass
       
    return IsoAct
#####Reverse BG for ROCK func######################
def revROCKAct(BGIso, IsoEff):
    Act = list()
    den = 2165 #kg/m^3
    vol = np.pi*((pow(18,2)*35.5)-(pow(13,2)*25.5)) #m^3
    mass = vol*den
    for i in range(len(BGIso)):
        Act.append(((BGIso[i][0]/mass)*((Ms[i]*1e6)/(Lam[i])))/(IsoEff[i][0]*0.0001*0.05))
    return Act
#####Background Activity from Water################
def WaterAct(PPM): #done
    """
    Calculates the background activity for the Water
    Decay Chains: Rn222
    """
    #def mass of water
    vol = np.pi*pow(TankR, 2)*2*Height #volume in m3
    #dim vars
    IsoAct = list(range(len(Iso[5])))
    for i in range(len(PPM)-1):
        IsoAct[i] = PPM[i]*vol #Bqm-3*m3
    return IsoAct
#####reverse BG for Water func#####################
def revWaterAct(BGIso, IsoEff):
    vol = np.pi*pow(TankR, 2)*(2*Height) # m3
    Act =(BGIso[0]/(vol*0.002)/(IsoEff[0]*0.0001*0.05))
    return Act
#####Background Activity from Gd###################
def GdAct(PPM):
    """
    Calculates the background activity for the Gd
    Decay Chains: U238, Th232, U235
    """
    #def mass of water
    mass = np.pi*pow(TankR, 2)*(2*Height)*1e3 #mass in kg
    #dim vars
    IsoAct = list(range(len(Iso[6])))
    for i in range(len(PPM)):
        IsoAct[i] = PPM[i]*mass*0.002 #Gdmass*Bqkg-1
    return IsoAct
#####reverse BG for GD#############################
def revGdAct(BGIso, IsoEff):
    Act = list()
    mass = np.pi*pow(TankR, 2)*(2*Height)*1e3
    for i in range(len(BGIso)):
        Act.append(BGIso[i][0]/(mass*0.002)/(IsoEff[i][0]*0.0001*0.05))
    return Act
#####Efficiences###################################
##dim vars
#######PMT#########################################
PMTIsoDecay = [IsoDecay[0], IsoDecay[1], IsoDecay[3]] #[[U238 chain], [Th232 chain], [K40 chain]]
PMTIsoDefault = [Eff.PMTU238,    #U238 Chain
                 Eff.PMTTh232,   #Th232 Chain
                 Eff.PMTK40]     #K40 Chain
PMTIsoEff = PMTIsoDefault
#######VETO########################################
VETOIsoDecay = [IsoDecay[0], IsoDecay[1], IsoDecay[3]] #[[U238 chain], [Th232 chain], [K40 chain]]
VETOIsoDefault = [Eff.VETOU238,  #U238 Chain
                  Eff.VETOTh232, #Th232 Chain
                  Eff.VETOK40]   #K40 Chain
VETOIsoEff = VETOIsoDefault
#######TANK########################################
TANKIsoDecay = [IsoDecay[0], IsoDecay[1], IsoDecay[3], IsoDecay[5]]
TANKIsoDefault = [Eff.TANKU238,  #U238 Chain
                  Eff.TANKTh232, #Th232 Chain
                  Eff.TANKK40,   #K40 Chain
                  Eff.TANKSTEEL] #Steel Activity
TANKIsoEff = TANKIsoDefault
#######CONC########################################
CONCIsoDecay = [IsoDecay[0], IsoDecay[1], IsoDecay[3]]
CONCIsoDefault = [[1.25e-5, 1.25e-5, 1.25e-5, 1.25e-5, 1.25e-5], #[[Pa234, Pb214, Bi214, Bi210, Tl210],
                  [1.25e-5, 1.25e-5, 1.25e-5, 1.25e-5],    #[Ac228, Pb212, Bi212, Tl208],
                  [1.25e-5]]             #[K40]]
CONCIsoEff = CONCIsoDefault
#######ROCK########################################
ROCKIsoDecay = [IsoDecay[0], IsoDecay[1], IsoDecay[3]]
ROCKIsoDefault = [Eff.ROCKU238,  #U238 Chain 
                  Eff.ROCKTh232, #Th232 Chain
                  Eff.ROCKK40]   #K40 Chain
ROCKIsoEff = ROCKIsoDefault
#######GD##########################################
GDIsoDecay = [IsoDecay[0],IsoDecay[1],IsoDecay[2], IsoDecay[0], IsoDecay[1], IsoDecay[2]] 
GDIsoDefault = [Eff.GDU238,  #U238 Chain
                Eff.GDTh232, #Th232 Chain
                Eff.GDU235,  #U235 Chain
                Eff.GDU238,  #U238_l Chain
                Eff.GDTh232, #Th232_l Chain
                Eff.GDU235]  #U235_l Chain
GDIsoEff = GDIsoDefault
#######RnWater#####################################
WATERIsoDecay = IsoDecay[4] #Rn222 decay chain
WATERIsoDefault = Eff.WATERRn222 #[Pb214, Bi214, Bi210, Tl210]
WATERIsoEff = WATERIsoDefault
######Background Rate##############################
scale = 1/6 #(pow(fiducialRaduis, 2)*fiducialHeight)/(pow(detectorRaduis, 2)*decetorHeight)
###################################################
def BGRate():
    """
    Calculates the Background Rate for all components
    Unit: Events per day
    """
    ####PMTs#######################################
    print('##################################################') 
    print('BGR due to PMTs')
    PMTBGIso = [[], [], []]
    PMTBGR = 0
    for i in range(len(PMTIsoDecay)):
        for x in range(len(PMTIsoEff[i])):
            PMTBGIso[i].append(dataAct[0][i]*PMTIsoEff[i][x])
            print('BGR due to ' + PMTIsoDecay[i][x] + ' =  %.5e'  % PMTBGIso[i][x]) 
        PMTBGR += sum(PMTBGIso[i])
    print('Total BGR due to PMTs = %.5e' % PMTBGR)
    ####VETO#######################################
    print('##################################################') 
    print('BGR due to VETO')
    VETOBGIso = [[], [], []]
    VETOBGR = 0
    for i in range(len(VETOIsoDecay)):
        for x in range(len(VETOIsoEff[i])):
            VETOBGIso[i].append(dataAct[1][i]*VETOIsoEff[i][x])
            print('BGR due to ' + VETOIsoDecay[i][x] + ' = %.5e' % VETOBGIso[i][x])
        VETOBGR += sum(VETOBGIso[i])
    print('Total BRG due to Veto = %.5e' % VETOBGR)
    ####TANK#######################################
    print('##################################################') 
    print('BGR due to TANK')
    TANKBGIso = [[], [], [], []]
    TANKBGR = 0
    for i in range(len(TANKIsoDecay)):
        for x in range(len(TANKIsoEff[i])):
            TANKBGIso[i].append(dataAct[2][i]*TANKIsoEff[i][x])
            print('BGR due to ' + TANKIsoDecay[i][x] + ' = %.5e' % TANKBGIso[i][x])
        TANKBGR += sum(TANKBGIso[i])
    print('Total BGR due to Tank = %.5e' % TANKBGR)
    ####CONCRETE###################################
    print('##################################################') 
    print('BGR due to CONCRETE')
    CONCBGIso = [[], [], []]
    CONCBGR = 0
    for i in range(len(CONCIsoDecay)):
        for x in range(len(CONCIsoEff[i])):
            CONCBGIso[i].append(dataAct[3][i]*CONCIsoEff[i][x])
            print('BGR due to ' + CONCIsoDecay[i][x] + ' = %.5e' % CONCBGIso[i][x])
        CONCBGR += sum(CONCBGIso[i])
    print('Total BGR due to Concrete = %.5e' % CONCBGR)
    ####ROCK#######################################
    print('##################################################') 
    print('BGR due to ROCK')
    ROCKBGIso = [[], [], []]
    ROCKBGR = 0
    for i in range(len(ROCKIsoDecay)):
        for x in range(len(ROCKIsoEff[i])):
            ROCKBGIso[i].append(dataAct[4][i]*ROCKIsoEff[i][x])
            print('BGR due to ' + ROCKIsoDecay[i][x] + ' = %.5e' % ROCKBGIso[i][x])
        ROCKBGR += sum(ROCKBGIso[i])
    print('Total BGR due to Rock = %.5e' % ROCKBGR)
    ####RnWATER####################################
    print('##################################################')
    print('BGR due to WATER')    
    WATERBGIso = []
    for i in range(len(WATERIsoEff)): #1d array
        print('WATERIsoEff[i] = ', WATERIsoEff[i])
        WATERBGIso.append(dataAct[5][0]*WATERIsoEff[i])
        print('BGR due to ' + WATERIsoDecay[i] + ' = %.5e' % WATERBGIso[i])
    WATERBGR = sum(WATERBGIso)
    print('Total BGR due to Gd Water = %.5e' % WATERBGR)
    ####Gd#########################################
    print('##################################################') 
    print('BGR due to GD')
    GDBGIso = [[], [], [], [], [], []]
    GDBGR   = 0
    for i in range(len(GDIsoDecay)):
        for x in range(len(GDIsoEff[i])):
            GDBGIso[i].append(dataAct[6][i]*GDIsoEff[i][x])
            print('BGR due to ' + GDIsoDecay[i][x] + ' %.5e' % GDBGIso[i][x])
        GDBGR += sum(GDBGIso[i])
    print('Total BGR due to Gd = %.5e' % GDBGR)
###################################################
    #Total#########################################
    tot = PMTBGR + VETOBGR + TANKBGR + CONCBGR + ROCKBGR + WATERBGR + GDBGR
    #TODO Define the share of events for each decay in each isotope in each component. 
    # These will need to be accessible outside the function.
    # e.g.
    # PMTIsoDecayShare[i][x] = PMTBGIso[i][x]/tot 
    # ...for each component
 
    #print('##################################################')
    print('Total singles rate per second is %.5e' % tot)
    bgi = True
    tot*=0.05*0.0001
    tot+=FN+RN
    print('Total accidental + cosmic muon background rate per day is %.5e' % tot)
    return tot, PMTBGIso, VETOBGIso, TANKBGIso, CONCBGIso, ROCKBGIso, WATERBGIso, GDBGIso
###################################################
#Iso = [Pa234, Ac228, Pb214, Bi214, Pb212, Bi212, Tl210, Bi210, Tl208, K40]
#TODO Replace this with the calculation at the end of the previous function
#IsoShare = [6.73998e-2, 7.56318e-2, 1.81474e-2, 2.02340e-1, 1.36405e-3, 7.18246e-2, 2.67975e-1, 4.53142e-2, 1.56517e-1, 9.34868e-2]
#PMTShare = [4.60123e-1, 5.37989e-1, 4.06841e-1, 1.95302e-1, 2.37596e-1, 5.78219e-1, 1.88178e-1, 3.63865e-1, 3.62383e-1, 2.98963e-1]
#VETOShare = [3.95017e-1, 4.12636e-1, 3.12046e-1, 1.65500e-1, 2.14290e-1, 3.33691e-1, 1.69719e-1, 2.93687e-1, 2.17803e-1, 2.44321e-1] 
#TANKShare = [1.44844e-1, 4.79718e-2, 3.62776e-2, 3.88787e-1, 5.15283e-1, 8.44188e-2, 4.08107e-1, 3.51846e-2, 3.83691e-1, 1.45410e-1] 
#CONCShare = [1.39419e-5, 1.33521e-3, 1.00972e-3, 2.50823e-2, 3.13512e-2, 3.33691e-1, 1.17226e-3, 0, 3.45508e-2, 6.80389e-3]
#ROCKShare = [0, 6.84725e-5, 5.17807e-5, 1.13687e-3, 1.48012e-3, 2.23804e-4, 1.17226e-3, 0, 1.57184e-3, 3.06572e-4]
#RnWAshare = [0, 0, 2.43773e-1, 2.24192e-1, 0, 0, 2.07993e-1, 3.07263e-1, 0, 3.04196e-1]

def MaxBG(s,t):
    sigma = 4.65
    S = s*0.9
    #def Max BG formula
    B = (1.5*t*S**2)/(2.5*sigma**2) - S/2.5
    Mbg = B - (S*1.15)
    print('Maximum Background for this time dection @ 3 sigma rate is %.5e' % Mbg)
    return Mbg

########Max Accidental BG##########################
def Max(bg, share):
    #TODO
    # Calculate BG using IsoDecay shares calculated in BGRate function above
    # e.g. for PMTisotope:
    #               for PMTIsodecay:
    #                   BG += bg*PMTIsoDecayShare[i][x]
    # for all components!
    for i in range(len(share)):
        BG += bg*IsoShare[i]*share[i]
    return BG
########Accidental Background######################
#U238  = [Pa234, Pb214, Bi214, Tl210, Bi210]
#Th232 = [Ac228, Bi212, Pb212, Tl208]
#K40   = [K40]
#########PMT#######################################
PMT_Pr =  [Pr.PMTU238,   #U238 chain
           Pr.PMTTh232,  #Th232 chain
           Pr.PMTK40]    #K40 chain
PMT_Nr =  [Nr.PMTU238,   #U238 chain
           Nr.PMTTh232,  #Th232 chain
           Nr.PMTK40]    #K40 chain
#########VETO######################################
VETO_Pr = [Pr.VETOU238,  #U238 chain
           Pr.VETOTh232, #Th232 chain
           Pr.VETOK40]   #K40 chain
VETO_Nr = [Nr.VETOU238,  #U238 chain
           Nr.VETOTh232, #Th232 chain
           Nr.VETOK40]   #K40
#########TANK######################################
TANK_Pr = [Pr.TANKU238,  #U238 chain
           Pr.TANKTh232, #Th232 chain
           Pr.TANKK40]   #K40 chain
TANK_Nr = [Nr.TANKU238,  #U238 chain
           Nr.TANKTh232, #Th232 chain
           Nr.TANKK40]   #K40
#########CONC#########################################No data for CONCRETE in results.root
CONC_Pr = [[0, 0, 0, 0, 0], #U238 chain
          [0, 0, 0, 0], #Th232 chain
          [0]] #K40 chain
CONC_Nr = [[0, 0, 0, 0, 0],#U238 chain
          [0, 0, 0, 0],  #Th232 chain
          [0]]           #K40 chain
#########ROCK######################################
ROCK_Pr = [Pr.ROCKU238,  #U238 chain
           Pr.ROCKTh232, #Th232 chain
           Pr.ROCKK40]   #K40 chain
ROCK_Nr = [Nr.ROCKU238,  #U238 chain
           Nr.ROCKTh232, #Th232 chain
           Nr.ROCKK40]   #K40
#########RnWater###################################
WATER_Pr = Pr.WATERRn222 #Rn222 chain
WATER_Nr = Nr.WATERRn222 #Rn222 chain
#########GD########################################
GD_Pr = [Pr.GDU238,      #U238 Chain
         Pr.GDTh232,     #Th232 Chain
         Pr.GDU235]      #U235 Chain
GD_Nr = [Nr.GDU238,      #U238 Chain
         Nr.GDTh232,     #Th232 Chain
         Nr.GDU235]      #U235 Chain
###################################################
def AccBack(Prate, Nrate):
    """
    Caculates Accidental Background rate
    Prate: rate with the prompt n9 cut
    Nrate: rate with the delayed n9 cut
    """
    # perform time cut (0.0001), distance cut (0.05), 
    # convert to per day rate
    timeScale = 0.0001*0.05  
    back = 0
    if isinstance(Prate[0], list) == True: #list is 2d
        for i in range(len(Prate)):
            for x in range(len(Prate[i])):
                back += Prate[i][x]*Nrate[i][x]*timeScale
    elif isinstance(Prate[0], list) == False: #list is 1d
        for i in range(len(Prate)):
            back += Prate[i]*Nrate[i]*timeScale
    return back
PMT_Acc = AccBack(PMT_Pr, PMT_Nr)
VETO_Acc = AccBack(VETO_Pr, VETO_Nr)
TANK_Acc = AccBack(TANK_Pr, TANK_Nr)
CONC_Acc = AccBack(CONC_Pr, CONC_Nr)
ROCK_Acc = AccBack(ROCK_Pr, ROCK_Nr)
WATER_Acc = AccBack(WATER_Pr, WATER_Nr)
GD_Acc = AccBack(GD_Pr, GD_Nr)
###################################################
ans = ""
ai = False
ei = False
dataAct = [[], [], [], [], [], [], []]
options = ['a', 'e', 'bgr', 'exit', 'td', 'maxbg', 'cb']
#Activity lists initialised to default values######
PMTPPM = IsoDefault[0]
VETOPPM = IsoDefault[1]
TANKACT = IsoDefault[2]
CONCACT = IsoDefault[3]
ROCKPPM = IsoDefault[4]
RnWPPM = IsoDefault[5]
GDPPM = IsoDefault[6]
dataAct[0] = PMTAct(PMTPPM)
dataAct[1] = VETOAct(VETOPPM)
dataAct[2] = TankAct(TANKACT)
dataAct[3] = ConcAct(CONCACT)
dataAct[4] = RockAct(ROCKPPM)
dataAct[5] = WaterAct(RnWPPM)
dataAct[6] = GdAct(GDPPM)
ans = ""
while ans.lower() != "exit":
    ans = menu()
#######Activity####################################
    if ans.lower() == 'a':
    ####PMT########################################
        in_ans = inputcheck(InType[0], Comp[0])
        print('##################################################')
        if in_ans == 'y':
            for i in range(len(PMTPPM)):
                PMTPPM[i] = InputVals(InType[0], Iso[0][i], Comp[0], IsoDefault[0][i])
        elif in_ans == 'n':
            for i in range(len(PMTPPM)):
                disdefval(InType[0], Iso[0][i], Comp[0], IsoDefault[0][i])
        in_ans = ''
    ####VETO#######################################
        print('##################################################')
        in_ans = inputcheck(InType[0], Comp[1])
        print('##################################################')
        if in_ans == 'y':
            for i in range(len(VETOPPM)):
                VETOPPM[i] = InputVals(InType[0], Iso[1][i], Comp[1], IsoDefault[1][i])
        elif in_ans == 'n':
            for i in range(len(VETOPPM)):
                disdefval(InType[0], Iso[1][i], Comp[1], IsoDefault[1][i])
        in_ans = ''
    ####TANK#######################################
        print('##################################################')
        in_ans = inputcheck(InType[1], Comp[2])
        print('##################################################')
        if in_ans == 'y':
            for i in range(len(TANKACT)):
                TANKACT[i] = InputVals(InType[1], Iso[2][i], Comp[2], IsoDefault[2][i])
        elif in_ans == 'n':
            for i in range(len(TANKACT)):
                disdefval(InType[1], Iso[2][i], Comp[2], IsoDefault[2][i])
        in_ans = ''
    ####CONCRETE###################################
        print('##################################################')
        in_ans = inputcheck(InType[1], Comp[3])
        print('##################################################')
        if in_ans == 'y':
            for i in range(len(CONCACT)):
                CONCACT[i] = InputVals(InType[1], Iso[3][i], Comp[3], IsoDefault[3][i])
        elif in_ans == 'n':
            for i in range(len(CONCACT)):
                disdefval(InType[1], Iso[3][i], Comp[3], IsoDefault[3][i])
    ####ROCK#######################################
        print('##################################################')
        in_ans = inputcheck(InType[0], Comp[4])
        print('##################################################')
        if in_ans == 'y':
            for i in range(len(ROCKPPM)):
                ROCKPPM[i] = InputVals(InType[0], Iso[4][i], Comp[4], IsoDefault[4][i])
        elif in_ans == 'n':
            for i in range(len(ROCKPPM)):
                disdefval(InType[0], Iso[4][i], Comp[4], IsoDefault[4][i])
    ####Rn WATER###################################
        print('##################################################') 
        in_ans = inputcheck(InType[0], Comp[5])
        print('##################################################')
        if in_ans == 'y':
            for i in range(len(RnWPPM)):
                RnWPPM[i] = InputVals(InType[0], Iso[5][i], Comp[5], IsoDefault[5][i])
        elif in_ans == 'n':
            for i in range(len(RnWPPM)):
                disdefval(InType[0], Iso[5][i], Comp[5], IsoDefault[5][i])
    ####Gd#########################################
        print('##################################################')
        in_ans = inputcheck(InType[0], Comp[6])
        if in_ans == 'y':
            for i in range(len(GDPPM)):
                GDPPM[i] = InputVals(InType[0], Iso[6][i], Comp[6], IsoDefault[6][i])
        elif in_ans == 'n':
            for i in range(len(GDPPM)):
                disdefval(InType[0], Iso[6][i], Comp[6], IsoDefault[6][i])
    ####Get Data###################################
        dataAct[0] = PMTAct(PMTPPM)
        dataAct[1] = VETOAct(VETOPPM)
        dataAct[2] = TankAct(TANKACT)
        dataAct[3] = ConcAct(CONCACT)
        dataAct[4] = RockAct(ROCKPPM)
        dataAct[5] = WaterAct(RnWPPM)
        dataAct[6] = GdAct(GDPPM)
    #####output####################################
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
######Efficiency###################################
    elif ans.lower() == 'e':
    ####PMTs#######################################
        print('##################################################')
        in_ans = inputcheck(InType[2], Comp[0])
        print('##################################################')
        print('Efficiency of Isotopes in ' + Comp[0])
        if in_ans.lower() == 'y':
            for i in range(len(PMTIsoDecay)):
                for x in range(len(PMTIsoEff[i])):
                    PMTIsoEff[i][x] = InputVals(InType[2], PMTIsoDecay[i][x], Comp[0], PMTIsoDefault[i][x])
        elif in_ans.lower() == 'n':
            for i in range(len(PMTIsoDecay)):
                for x in range(len(PMTIsoEff[i])):
                    disdefval(InType[2], PMTIsoDecay[i][x], Comp[0], PMTIsoDefault[i][x])
    ####VETOS######################################
        print('##################################################')
        in_ans = inputcheck(InType[2], Comp[1])
        print('##################################################')
        print('Efficiency of Isotopes in ' + Comp[1])
        if in_ans.lower() =='y':
            for i in range(len(VETOIsoDecay)):
                for x in range(len(VETOIsoEff[i])):
                    VETOIsoEff[i][x] = InputVals(InType[2], VETOIsoDecay[i][x], Comp[1], VETOIsoDefault[i][x])
        elif in_ans.lower() == 'n':
            for i in range(len(VETOIsoDecay)):
                for x in range(len(VETOIsoEff[i])):
                    disdefval(InType[2], VETOIsoDecay[i][x], Comp[1], VETOIsoDefault[i][x])
    ####TANK#######################################
        print('##################################################')
        in_ans = inputcheck(InType[2], Comp[2])
        print('##################################################')
        print('Efficiency of Isotopes in ' + Comp[2])
        if in_ans.lower() == 'y':
            for i in range(len(TANKIsoDecay)):
                for x in range(len(TANKIsoEff[i])):
                    TANKIsoEff[i][x] = InputVals(InType[2], TANKIsoDecay[i][x], Comp[2], TANKIsoDefault[i][x])
        elif in_ans.lower() == 'n':
            for i in range(len(TANKIsoDecay)):
                for x in range(len(TANKIsoEff[i])):
                    disdefval(InType[2], TANKIsoDecay[i][x], Comp[3], TANKIsoDefault[i][x])
    ####CONCRETE###################################
        print('##################################################')
        in_ans = inputcheck(InType[2], Comp[3])
        print('##################################################')
        print('Efficiency of Isotopes in ' + Comp[3])
        if in_ans.lower() == 'y':
            for i in range(len(CONCIsoDecay)):
                for x in range(len(CONCIsoEff[i])):
                    CONCIsoEff[i][x] = InputVals(InType[2], CONCIsoDecay[i][x], Comp[3], CONCIsoDefault[i][x])
        elif in_ans.lower() == 'n':
            for i in range(len(CONCIsoDecay)):
                for x in range(len(CONCIsoEff[i])):
                    disdefval(InType[2], CONCIsoDecay[i][x], Comp[4], CONCIsoDefault[i][x])
    #####ROCK######################################
        print('##################################################')
        in_ans = inputcheck(InType[2], Comp[4])
        print('##################################################')
        print('Efficiency of Isotopes in ' + Comp[4])
        if in_ans.lower() == 'y':
            for i in range(len(ROCKIsoDecay)):
                for x in range(len(ROCKIsoEff[i])):
                    ROCKIsoEff[i][x] = InputVals(InType[2], ROCKIsoDecay[i][x], Comp[4], ROCKIsoDefault[i][x])
        elif in_ans.lower() == 'n':
            for i in range(len(ROCKIsoDecay)):
                for x in range(len(ROCKIsoEff[i])):
                    disdefval(InType[2], ROCKIsoDecay[i][x], Comp[4], ROCKIsoDefault[i][x])
    ####RnWATER####################################
        print('##################################################')
        in_ans = inputcheck(InType[2], Comp[5])
        print('##################################################')
        print('Efficiency of Isotopes in ' + Comp[5])
        if in_ans == 'y':
            for i in range(len(WATERIsoDecay)): #1d list
                WATERIsoEff[i] = InputVals(InType[2], WATERIsoDecay[i], Comp[5], WATERIsoDefault[i])
        elif in_ans.lower() == 'n':
            for i in range(len(WATERIsoDecay)):
                disdefval(InType[2], WATERIsoDecay[i], Comp[5], WATERIsoDefault[i])
    ####GD#########################################
        print('##################################################')
        in_ans = inputcheck(InType[2], Comp[5])
        print('##################################################')
        print('Efficiency of Isotopes in ' + Comp[6])
        if in_ans == 'y':
            for i in range(len(GDIsoDecay)):
                for x in range(len(GDIsoDecay[i])):
                    GDIsoEff[i][x] = InputVals(InType[2], GDIsoDecay[i][x], Comp[6], GDIsoDefault[i][x])
        elif in_ans == 'n':
            for i in range(len(GDIsoDecay)):
                for x in range(len(GDIsoDecay[i])):
                    disdefval(InType[2], GDIsoDecay[i][x], Comp[6], GDIsoDefault[i][x])
    ####reset######################################
        ei = True
        clear()
        ans = ''
########Background Rate############################
    elif ans.lower() == 'bgr':
        if ai == False:
            print('##################################################')
            print('Setting Activity values to default values')
            for i in range(len(Iso)):
                print('##############################################')
                print('Activity of Isotopes in ' + Comp[i])
                for x in range(len(Iso[i])):
                    if i == 2 or i == 3:
                        disdefval(InType[1], Iso[i][x], Comp[i], IsoDefault[i][x])
                    else:
                        disdefval(InType[0], Iso[i][x], Comp[i], IsoDefault[i][x])
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
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[1])
            for i in range(len(VETOIsoDecay)):
                for x in range(len(VETOIsoEff[i])):
                    disdefval(InType[2], VETOIsoDecay[i][x], Comp[1], VETOIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[2])
            for i in range(len(TANKIsoDecay)):
                for x in range(len(TANKIsoEff[i])):
                    disdefval(InType[2], TANKIsoDecay[i][x], Comp[2], TANKIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[3])
            for i in range(len(CONCIsoDecay)):
                for x in range(len(CONCIsoEff[i])):
                    disdefval(InType[2], CONCIsoDecay[i][x], Comp[3], CONCIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[4])
            for i in range(len(ROCKIsoDecay)):
                for x in range(len(ROCKIsoDefault[i])):
                    disdefval(InType[2], PMTIsoDecay[i][x], Comp[4], PMTIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[5])
            for i in range(len(WATERIsoDecay)):
                disdefval(InType[2], WATERIsoDecay[i], Comp[5], WATERIsoEff[i])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[6])
            for i in range(len(GDIsoDecay)):
                for x in range(len(GDIsoDefault[i])):
                    disdefval(InType[2], GDIsoDecay[i][x], Comp[6], GDIsoEff[i][x])

        else:
            pass
        #BGR Code
        tot, PMTBGIso, VETOBGIso, TANKBGIso, CONCBGIso, ROCKBGIso, WATERBGIso, GDBGIso = BGRate()
#########Accidental BG Rate########################
#        print('##################################################')
#        print('PMT  Accidental background = %.5e' % PMT_Acc)
#        print('VETO Accidental background = %.5e' % VETO_Acc)
#        print('TANK Accidental background = %.5e' % TANK_Acc)
#        print('CONC Accidental background = %.5e' % CONC_Acc)
#        print('ROCK Accidental background = %.5e' % ROCK_Acc)
#        print('RnWATER Accidental background = %5e' %WATER_Acc)
#        print('GD Accidental background = %.5e' % GD_Acc)
#        print('##################################################')
#        tot += (PMT_Acc + VETO_Acc + TANK_Acc + CONC_Acc + ROCK_Acc + WATER_Acc + GD_Acc)
        clear()
        ans = ''
######time detection calculation###################
    elif ans.lower() == 'td':
        if ai == False:
            print('##################################################')
            print('Setting Activity values to default values')
            for i in range(len(Iso)):
                print('##################################################')
                print('Activity of Isotopes in ' + Comp[i])
                for x in range(len(Iso[i])):
                    if i == 2 or i == 3:
                        disdefval(InType[1], Iso[i][x], Comp[i], IsoDefault[i][x])
                    else:
                        disdefval(InType[0], Iso[i][x], Comp[i], IsoDefault[i][x])
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
                    disdefval(InType[2], PMTIsoDecay[i][x], Comp[0], PMTIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[1])
            for i in range(len(VETOIsoDecay)):
                for x in range(len(VETOIsoEff[i])):
                    disdefval(InType[2], VETOIsoDecay[i][x], Comp[1], VETOIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[2])
            for i in range(len(TANKIsoDecay)):
                for x in range(len(TANKIsoEff[i])):
                    disdefval(InType[2], TANKIsoDecay[i][x], Comp[2], TANKIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[3])
            for i in range(len(CONCIsoDecay)):
                for x in range(len(CONCIsoEff[i])):
                    disdefval(InType[2], CONCIsoDecay[i][x], Comp[3], CONCIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[4])
            for i in range(len(ROCKIsoDecay)):
                for x in range(len(ROCKIsoDefault[i])):
                    disdefval(InType[2], PMTIsoDecay[i][x], Comp[4], PMTIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[5])
            for i in range(len(WATERIsoDecay)):
                disdefval(InType[2], WATERIsoDecay[i], Comp[5], WATERIsoEff[i])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[6])
            for i in range(len(GDIsoDecay)):
                for x in range(len(GDIsoDefault[i])):
                    disdefval(InType[2], GDIsoDecay[i][x], Comp[6], GDIsoEff[i][x])
        else:
            pass
        if bgi == False:
            tot, PMTBGIso, VETOBGIso, TANKBGIso, CONCBGIso, ROCKBGIso, WATERBGIso, GDBGIso = BGRate() 
#            tot += PMT_Acc + VETO_Acc + TANK_Acc + CONC_Acc + ROCK_Acc + WATER_Acc
        else:
            pass
        print('##################################################')
        print('Total BG = %.5e per day' % tot)
        try:
            signal = literal_eval(input('Input signal rate: '))
            signal < 1
        except:
            signal = 0.430
            print('Signal rate set to default value of %.5e' % signal)
        B = signal*1.035 + tot
        S = signal*0.9
        sigma = 4.65
        t = pow(sigma, 2)*(B+((B+S)/(3/2)))*(1/pow(S,2)) #/((60**2)*24) #[days]
        print('Time to detection @ 3 sigma rate = %.5e' % t + ' days')
        clear()
        ans = ''
######Calculate max background#####################
    elif ans.lower() == 'maxbg':
        if ai == False:
            print('##################################################')
            print('Setting Activity values to default values')
            for i in range(len(Iso)):
                print('##################################################')
                print('Activity of Isotopes in ' + Comp[i])
                for x in range(len(Iso[i])):
                    if i == 2 or i == 3:
                        disdefval(InType[1], Iso[i][x], Comp[i], IsoDefault[i][x])
                    else:
                        disdefval(InType[0], Iso[i][x], Comp[i], IsoDefault[i][x])
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
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[1])
            for i in range(len(VETOIsoDecay)):
                for x in range(len(VETOIsoEff[i])):
                    disdefval(InType[2], VETOIsoDecay[i][x], Comp[1], VETOIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[2])
            for i in range(len(TANKIsoDecay)):
                for x in range(len(TANKIsoEff[i])):
                    disdefval(InType[2], TANKIsoDecay[i][x], Comp[2], TANKIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[3])
            for i in range(len(CONCIsoDecay)):
                for x in range(len(CONCIsoEff[i])):
                    disdefval(InType[2], CONCIsoDecay[i][x], Comp[3], CONCIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[4])
            for i in range(len(ROCKIsoDecay)):
                for x in range(len(ROCKIsoDefault[i])):
                    disdefval(InType[2], PMTIsoDecay[i][x], Comp[4], PMTIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[5])
            for i in range(len(WATERIsoDecay)):
                disdefval(InType[2], WATERIsoDecay[i], Comp[5], WATERIsoEff[i])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[6])
            for i in range(len(GDIsoDecay)):
                for x in range(len(GDIsoDefault[i])):
                    disdefval(InType[2], GDIsoDecay[i][x], Comp[6], GDIsoEff[i][x])
        else:
            pass
        if bgi == False:
            tot, PMTBGIso, VETOBGIso, TANKBGIso, CONCBGIso, ROCKBGIso, WATERBGIso, GDBGIso = BGRate() 
#            tot += PMT_Acc + VETO_Acc + TANK_Acc + CONC_Acc + ROCK_Acc + WATER_Acc
        else:
            pass
        #signal input
        try:
            signal = literal_eval(input('Input signal rate: '))
            signal < 1
        except:
            signal = 0.430
            print('Signal rate set to default value of %.5e' % signal)
        #get number of days
        try:
            days = literal_eval(input('Input time dection in days: '))
            days != 0
        except:
            days = 2.02667e+02
            print('Time dection set to default value of %.5e days' % days)
        Mbg = MaxBG(signal,days)   
        clear()
        ans = ''
####Cleanliness budget calculation#################
    elif ans.lower() == 'cb':
        Iso_cb_labels = ['Pa234', 'Ac228', 'Pb214', 'Bi214', 'Pb212', 'Bi212', 'Tl210', 'Bi210', 'Tl208', 'K40'] 
        Iso_cb = list()
#        PMT_BG_CB = PMT_Acc
#        VETO_BG_CB = VETO_Acc
#        TANK_BG_CB = TANK_Acc
#        CONC_BG_CB = CONC_Acc
#        ROCK_BG_CB = ROCK_Acc
#        RnW_BG_CB = WATER_Acc
#        GD_BG_CB = GD_Acc
        #signal input##############################
        if ai == False:
            print('##################################################')
            print('Setting Activity values to default values')
            for i in range(len(Iso)):
                print('##################################################')
                print('Activity of Isotopes in ' + Comp[i])
                for x in range(len(Iso[i])):
                    if i == 2 or i == 3:
                        disdefval(InType[1], Iso[i][x], Comp[i], IsoDefault[i][x])
                    else:
                        disdefval(InType[0], Iso[i][x], Comp[i], IsoDefault[i][x])
        else:
            pass
        if ei == False:
            print('##################################################')
            print('Setting Efficiency values to default values')
            #just print out lists as set to default when lists are defined
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[0])
            for i in range(len(PMTIsoDecay)):
                for x in range(len(PMTIsoEff[i])):
                    disdefval(InType[2], PMTIsoDecay[i][x], Comp[0], PMTIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[1])
            for i in range(len(VETOIsoDecay)):
                for x in range(len(VETOIsoEff[i])):
                    disdefval(InType[2], VETOIsoDecay[i][x], Comp[1], VETOIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[2])
            for i in range(len(TANKIsoDecay)):
                for x in range(len(TANKIsoEff[i])):
                    disdefval(InType[2], TANKIsoDecay[i][x], Comp[2], TANKIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[3])
            for i in range(len(CONCIsoDecay)):
                for x in range(len(CONCIsoEff[i])):
                    disdefval(InType[2], CONCIsoDecay[i][x], Comp[3], CONCIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[4])
            for i in range(len(ROCKIsoDecay)):
                for x in range(len(ROCKIsoDefault[i])):
                    disdefval(InType[2], PMTIsoDecay[i][x], Comp[4], PMTIsoEff[i][x])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[5])
            for i in range(len(WATERIsoDecay)):
                disdefval(InType[2], WATERIsoDecay[i], Comp[5], WATERIsoEff[i])
            print('##################################################')
            print('Efficiency of Isotopes in ' + Comp[6])
            for i in range(len(GDIsoDecay)):
                for x in range(len(GDIsoDefault[i])):
                    disdefval(InType[2], GDIsoDecay[i][x], Comp[6], GDIsoEff[i][x])
        else:
            pass
        if bgi == False:
            tot, PMTBGIso, VETOBGIso, TANKBGIso, CONCBGIso, ROCKBGIso, WATERBGIso, GDBGIso = BGRate()
            PMTShare = share(tot, PMTBGIso)
            VETOShare = share(tot, VETOBGIso)
            TANKShare = share(tot, TANKBGIso)
            CONCShare = share(tot, CONCBGIso)
            ROCKShare = share(tot, ROCKBGIso)
            RnWAShare = share(tot, WATERBGIso)
            GDShare = share(tot, GDBGIso)
        else:
            pass
        try:
            signal = literal_eval(input('Input signal rate: '))
            signal < 1
        except:
            signal = 0.430
            print('Signal rate set to default value of %.3e' % signal)
        #get number of days
        try:
            days = literal_eval(input('Input time dection in days: '))
            days != 0
        except:
            days = 2.02667e+02
            print('Time dection set to default value of %.3e days' % days)
        #def sigma
        #B = signal*1.035 + tot
        Mbg = MaxBG(signal,days) #Events per day
        print('Maximum Background for this time dection @ 3 sigma rate is %.5e' % Mbg)
        #TODO We will need to add an additional step. If no radioactivity rate 
        # has been changed, then the share is as below.
        # If a radioactivity rate has been changed for a component, 
        # we need to calculate the new event rates due to that 
        # isotope in that component, then do: 
        # RBg = Mbg - sum(newRate) (remaining background)
        # and then for each remainin background do:
        # MaxRate = RBg * Share * normalisation
        # where normalisation = 1/sum(RShares) so that the total of all 
        # remaining 'share' values now adds up to 1
        #for i in range(len(IsoShare)):
        #    Iso_cb.append(Mbg*IsoShare[i])
        #   print(Iso_cb_labels[i] + ' = %.5e' % Iso_cb[i])
        print('##################################################')
        PMTBGIsoCB  = PMTShare
        VETOBGIsoCB = VETOShare
        TANKBGIsoCB = TANKShare
        CONCBGIsoCB = CONCShare
        ROCKBGIsoCB = ROCKShare
        RnWBGIsoCB  = RnWAShare
        GDBGIsoCB   = GDShare
        
        for i in range(len(PMTShare)):
            for x in range(len(PMTShare[i])):
                PMT_BG_CB = Mbg*(PMTShare[i][x])
                PMTBGIsoCB[i][x] = Mbg*PMTShare[i][x]
        print('Max BG from PMT = %.5e' % PMT_BG_CB)
        PMTIsoAct = revPMTAct(PMTBGIsoCB, PMTIsoEff)
        for i in range(len(PMTIsoAct)):
            print('%.5s = %.5e' % (Iso[0][i], PMTIsoAct[i]))
        print('##################################################')
        for i in range(len(VETOShare)):
            for x in range(len(VETOShare[i])):
                VETO_BG_CB = Mbg*VETOShare[i][x]
                VETOBGIsoCB[i][x] = VETO_BG_CB
        print('Max BG from VETO = %.5e' % VETO_BG_CB)
        VETOIsoAct = revVETOAct(VETOBGIsoCB,VETOIsoEff)
        for i in range(len(VETOBGIso)):
            print('%.5s = %.5e' % (Iso[1][i], VETOIsoAct[i]))
        print('##################################################')
        for i in range(len(TANKShare)):
            for x in range(len(TANKShare[i])):
                TANK_BG_CB = Mbg*TANKShare[i][x]
                TANKBGIsoCB[i][x] = TANK_BG_CB
        print('Max BG from TANK = %.5e' % TANK_BG_CB)
        TANKIsoAct = revTankAct(TANKBGIso, TANKIsoEff)
        for i in range(len(TANKIsoAct)):
            print('%.5s = %.5e' % (Iso[2][i], TANKIsoAct[i]))
        print('##################################################')
        for i in range(len(CONCShare)):
            for x in range(len(CONCShare[i])):
                CONC_BG_CB = Mbg*CONCShare[i][x]
                CONCBGIsoCB[i][x] = CONC_BG_CB
        print('Max BG from CONC = %.5e' % CONC_BG_CB)
        CONCIsoAct = revCONCAct(CONCBGIso, CONCIsoEff)
        for i in range(len(CONCIsoAct)):
            print('%.5s = %.5e' % (Iso[3][i], CONCIsoAct[i]))
        print('##################################################')
        for i in range(len(ROCKShare)):
            for x in range(len(ROCKShare[i])):
                ROCK_BG_CB = Mbg*ROCKShare[i][x]
                ROCKBGIsoCB[i][x] = ROCK_BG_CB
        print('Max BG from ROCK = %.5e' % ROCK_BG_CB)
        ROCKIsoAct = revROCKAct(ROCKBGIso, ROCKIsoEff)
        for i in range(len(ROCKIsoAct)):
            print('%.5s = %.5e' % (Iso[4][i], ROCKIsoAct[i]))
        print('##################################################')
        for i in range(len(RnWAShare)):
            RnW_BG_CB = Mbg*RnWAShare[i]
            RnWBGIsoCB[i] = RnW_BG_CB
        print('Max BG from Rn WATER =  %.5e' % RnW_BG_CB)
        RnWIsoAct = revWaterAct(WATERBGIso, WATERIsoEff)
        print('%.5s = %.5e' % (Iso[5][0], RnWIsoAct))
        print('##################################################')
        for i in range(len(GDShare)):
           for x in range(len(GDShare[i])):
            GD_BG_CB = Mbg*GDShare[i][x]
            GDBGIsoCB[i][x] = GD_BG_CB
        print('Max BG from GD = %.5e' % GD_BG_CB)
        GDIsoAct = revGdAct(GDBGIso, GDIsoEff)
        for i in range(len(GDIsoAct)):
            print('%.8s = %.5e' % (Iso[6][i], GDIsoAct[i]))
        print('##################################################')
        tot_cb = PMT_BG_CB + VETO_BG_CB + TANK_BG_CB + CONC_BG_CB + ROCK_BG_CB + RnW_BG_CB + GD_BG_CB
        print('Total = %.5e' % (tot_cb))
        #TODO We need to output the results in the formats we discussed:
        # 1. Max BG in events per second/day per component (as above)
        # 2. Max BG in events per second/day per isotope in each component:
        # 3. Max BG in ppm per isotope in each component:
        #    MaxAct = MaxIsoDecay/IsoDecayEff/MassOrVolumeOfComponent 
        #    (select the decay and related efficiency 
        #    for the decay responsible for most events and then basically
        #    reverse the BGRate and PPM calculations)
        diff = (Mbg - (tot_cb))
        print('Abs Diff = %.5e' %  diff)
        print('%% Diff = %.5e' % (diff/Mbg))
        print('##################################################')
        clear()
        ans = ''
    elif ans.lower() == 'exit':
        break

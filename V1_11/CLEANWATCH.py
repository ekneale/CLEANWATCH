#import component
import PMT
import VETO
import TANK
import CONC
import ROCK
import WATER
import GD
#imports
import Iso
import Eff
#import Prate
import Nrate
import os
from ast import literal_eval
from math import pow
#Vars
compList = ['PMT', 'VETO', 'TANK', 'CONC', 'ROCK', 'WATER', 'GD']
#Comp = {
#    "PMT"  : PMT,
#    "VETO" : VETO,
#    "TANK" : TANK,
#    "CONC" : CONC,
#    "ROCK" : ROCK,
#    "WATER": WATER,
#    "GD"   : GD
#}
#PMT
PMTPPM = PMT.defPPM
PMTAct = PMT.defPPM 
PMTEff = PMT.IsoEff
#print(PMTEff)
PMTErr = PMT.EffErr
PMT_Nr = [Nrate.PMTU238,
          Nrate.PMTTh232,
          Nrate.PMTK40]
#VETO
VETOPPM = VETO.defPPM
VETOAct = VETO.defPPM
VETOEff = VETO.IsoEff
VETOErr = VETO.EffErr
VETO_Nr = [Nrate.VETOU238,
           Nrate.VETOTh232,
           Nrate.VETOK40]
#TANK
TANKPPM = TANK.defPPM
TANKAct = TANK.defPPM
TANKEff = TANK.IsoEff
TANKErr = TANK.EffErr
TANK_Nr = [Nrate.TANKU238,
           Nrate.TANKTh232,
           Nrate.TANKK40,
           [Nrate.TANKSTEEL[0]],
           [Nrate.TANKSTEEL[1]]]
#CONC
CONCPPM = CONC.defPPM
CONCAct = CONC.defPPM
CONCEff = CONC.IsoEff
CONCErr = CONC.EffErr
CONC_Nr = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0],
           [0]]
#ROCK
ROCKPPM = ROCK.defPPM
ROCKAct = ROCK.defPPM
ROCKEff = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0],
           [0],
           [1]]
ROCKErr = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0],
           [0],
           [0]]
ROCK_Nr = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0],
           [0],
           [0]]
#WATER
WATERPPM = WATER.defPPM
WATERAct = WATER.defPPM
WATEREff = WATER.IsoEff
WATERErr = WATER.EffErr
WATER_Nr = [Nrate.WATERRn222,
           [1]]
#GD
GDPPM = GD.defPPM
GDAct = GD.defPPM
GDEff = GD.IsoEff
GDErr = GD.EffErr
GD_Nr = [Nrate.GDU238,
         Nrate.GDTh232,
         Nrate.GDU235,
         Nrate.GDU238,
         Nrate.GDTh232,
         Nrate.GDU235]
#input check
ai = False
ei = False
compAct = []
compEff = []
tot = 0
timeD = 0
#funcs
def menu(): #menu text
    """
    Displays options
    """
    a = ''
    options = ['a', 'e', 'bgr', 'exit', 'td', 'maxbg', 'cb']
    while a.lower() not in options:
        print('##################################################')
        print('WATCHMAN Cleanliness software, V1.11')
        print('Alex Healey, UoS, 2020')
        print('Options: ')
        print('- Input Values for Activity      [a]')
        print('- Input Values for Efficiency    [e]')
        print('- Calculate Background Rate      [bgr]')
        print('- Calculate Time Detection       [td]')
        print('- Calculate Maximum Background   [maxbg]')
        print('- Cleanliness Budget             [cb]')
        print('- Exit software                  [exit]')
        print('##################################################')
        a = str(input('Select an option: '))
        if a.lower() in options and a.lower() != 'exit':
            print('Option selected')
            print('Loading...')
            break
    return a
def inputVal(itype):
    iput = []
    a = input('What components would you like to input values for ' + itype  + 'for? [PMT/VETO/TANK/CONC/ROCK/WATER/GD]  ')
    iput = a.split()
    return iput
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
def ActDefault():
    if 'PMT' not in compAct:
        print('##########################################')
        print('Default values for PPM for Iso in PMT')
        Iso.disdef(Iso.PMT, PMTPPM, 'PPM')
        PMTAct = PMT.Activity(PMTPPM)
    if 'VETO' not in compAct:
        print('##########################################')
        print('Default values for PPM for Iso in VETO')
        Iso.disdef(Iso.VETO, VETOPPM, 'PPM')
        VETOAct = VETO.Activity(VETOPPM)
    if 'TANK' not in compAct:
        print('##########################################')
        print('Default values for PPM for Iso in TANK')
        Iso.disdef(Iso.TANK, TANKPPM, 'PPM')
        TANKAct = TANK.Activity(TANKPPM)
    if 'CONC' not in compAct:
        print('##########################################')
        print('Default values for PPM for Iso in CONC')
        Iso.disdef(Iso.CONC, CONCPPM, 'PPM')
        CONCAct = CONC.Activity(CONCPPM)
    if 'ROCK' not in compAct:
        print('##########################################')
        print('Default values for PPM for Iso in ROCK')
        Iso.disdef(Iso.ROCK, ROCKPPM, 'PPM')
        ROCKAct = ROCK.Activity(ROCKPPM)
    if 'WATER' not in compAct:
        print('##########################################')
        print('Default values for PPM for Iso in WATER')
        Iso.disdef(Iso.WATER, WATERPPM, 'PPM')
        WATERAct = WATER.Activity(WATERPPM)
    if 'GD' not in compAct:
        print('##########################################')
        print('Default values for PPM for Iso in GD')
        Iso.disdef(Iso.GD, GDPPM, 'PPM')
        GDAct = GD.Activity(GDPPM)
def EffDefault():
    if 'PMT' not in compEff:
        print('##########################################')
        print('Default values for Efficiency for Iso in PMT')
        for i in range(len(Iso.PMT)):
            print('##########################################')
            print(Iso.PMT[i] + ' chain')
            for x in range(len(PMTEff[i])):
                print('Efficiency for ' + PMT.IsoDecay[i][x] + ' set to default value of = %.5e +/- %.5e' % (PMTEff[i][x], PMTErr[i][x]))
    if 'VETO' not in compEff:
        print('##########################################')
        print('Default values for Efficiency for Iso in VETO')
        for i in range(len(Iso.VETO)):
            print('##########################################')
            print(Iso.VETO[i] + ' chain')
            for x in range(len(VETOEff[i])):
                print('Efficiency for ' + VETO.IsoDecay[i][x] + ' set to default value of = %.5e +/- %.5e' % (VETOEff[i][x], VETOErr[i][x]))
    if 'TANK' not in compEff:
        print('##########################################')
        print('Default values for Efficiency for Iso in TANK')
        for i in range(len(Iso.TANK)):
            print('##########################################')
            print(Iso.TANK[i] + ' chain')
            for x in range(len(TANKEff[i])):
                print('Efficiency for ' + TANK.IsoDecay[i][x] + ' set to default value of = %.5e +/- %.5e' % (TANKEff[i][x], TANKErr[i][x]))
    if 'CONC' not in compEff:
        print('##########################################')
        print('Default values for Efficiency for Iso in CONC')
        for i in range(len(Iso.CONC)):
            print('##########################################')
            print(Iso.CONC[i] + ' chain')
            for x in range(len(CONCEff[i])):
                print('Efficiency for ' + CONC.IsoDecay[i][x] + ' set to default value of = %.5e +/- %.5e' % (CONCEff[i][x], CONCErr[i][x]))
    if 'ROCK' not in compEff:
        print('##########################################')
        print('Default values for Efficiency for Iso in ROCK')
        for i in range(len(Iso.ROCK)):
            print('##########################################')
            print(Iso.ROCK[i] + ' chain')
            for x in range(len(ROCKEff[i])):
                print('Efficiency for ' + ROCK.IsoDecay[i][x] + ' set to default value of = %.5e +/- %.5e' % (ROCKEff[i][x], ROCKErr[i][x]))
    if 'WATER' not in compEff:
        print('##########################################')
        print('Default values for Efficiency for Iso in WATER')
        for i in range(len(Iso.WATER)):
            print('##########################################')
            print(Iso.WATER[i] + ' chain')
            for x in range(len(WATEREff[i])):
                print('Efficiency for ' + WATER.IsoDecay[i][x] + ' set to default value of = %.5e +/- %.5e' % (WATEREff[i][x], WATERErr[i][x]))
    if 'GD' not in compEff:
        print('##########################################')
        print('Default values for Efficiency for Iso in GD')
        for i in range(len(Iso.GD)):
            print('##########################################')
            print(Iso.GD[i] + ' chain')
            for x in range(len(GDEff[i])):
                print('Efficiency for ' + GD.IsoDecay[i][x] + ' set to default value of = %.5e +/- %.5e' % (GDEff[i][x], GDErr[i][x]))
def ErrProp(EffErr, IsoEff, BG):
    """
    Returns error of BGR
    """
    err = 0
    if IsoEff != 0:
        err = BG*(EffErr/IsoEff)
        #print(err, EffErr)
    else:
        err = 0
    return err
def AccBG(CompPrate, CompNrate): #not used
    timeScale = 0.0001*0.05
    BG = 0
    if isinstance(CompPrate[0], list):
        for i in range(len(CompPrate)):
            for x in range(len(CompPrate[i])):
                BG += CompPrate[i][x]*CompNrate[i][x]*timeScale
    elif isinstance(CompPrate[0], list) == False:
        for i in range(len(CompPrate)):
            BG += CompPrate[i]*CompNrate[i]*timeScale
    return BG
def bgrate():
    totBG_P = 0
    totBG_N = 0
    ##PMTs
    PMT_N = [[0 for x in range(len(PMTEff[i]))] for i in range(len(PMTEff))]
    PMT_P = [[0 for x in range(len(PMTEff[i]))] for i in range(len(PMTEff))]
    PMTBGErr = [[0 for x in range(len(PMTErr[i]))] for i in range(len(PMTErr))]
    PMTBGr_P = 0
    PMTBGr_N = 0
    #PMT_Acc = AccBG(PMT_Pr, PMT_Nr)
    PMTBGrErr = 0
    print(PMT.IsoDecay)
    print('##########################################')
    print('BG for PMT')
    for i in range(len(PMTEff)):
        print('##########################################')
        print(Iso.PMT[i] + ' chain')
        for x in range(len(PMTEff[i])):
            #print(PMT.IsoDecay[i][x])
            if PMT.IsoDecay[i][x] == 'Tl210':
                PMT_P[i][x] = (PMTEff[i][x]*PMTAct[i]*0.002)
                PMT_N[i][x] = (PMT_Nr[i][x]*PMTAct[i]*0.002)
            else:
                PMT_P[i][x] = (PMTAct[i]*PMTEff[i][x])
                PMT_N[i][x] = (PMTAct[i]*PMT_Nr[i][x])
            #print(Iso.PMT[i] + ' Activity = %.5e' % PMTAct[i])
            #print(PMT.IsoDecay[i][x] + ' Efficiency = %.5e' % PMTEff[i][x])
            #print(PMT.IsoDecay[i][x] + ' Efficiency Error = %.5e' % PMTErr[i][x])
            #print('Expected BG = %.5e' % (PMTAct[i]*PMTEff[i][x]))
            PMTBGErr[i][x] = ErrProp(PMTErr[i][x], PMTEff[i][x], PMT_P[i][x])
            #PMTBGrErr += PMTBGErr[i][x]
            print('BG due to ' + PMT.IsoDecay[i][x] + ' = %.5e +/- %.5e' % (PMT_P[i][x], PMTBGErr[i][x]))
    for i in range(len(PMT_P)):
        PMTBGr_P += sum(PMT_P[i])
    for i in range(len(PMT_N)):
        PMTBGr_N += sum(PMT_N[i])
    #print('Accidental BG for PMT = %.5e' % PMT_Acc)
    print('Total BG due to PMT = %.5e +/- %.5e' % (PMTBGr_P, PMTBGrErr))
    totBG_P += PMTBGr_P
    totBG_N += PMTBGr_N
    ##VETO
    VETO_P = [[0 for x in range(len(VETOEff[i]))] for i in range(len(VETOEff))]
    VETO_N = [[0 for x in range(len(VETOEff[i]))] for i in range(len(VETOEff))]
    VETOBGErr = VETOErr
    VETOBGr_P = 0
    VETOBGr_N = 0
    VETOBGrErr = 0
    #VETO_Acc = AccBG(VETO_Pr, VETO_Nr)
    print('##########################################')
    print('BG for VETO')
    for i in range(len(Iso.VETO)):
        print('##########################################')
        print(Iso.VETO[i] + ' chain')
        for x in range(len(VETO.IsoDecay[i])):
            if VETO.IsoDecay[i][x] == 'Tl210':
                VETO_P[i][x] = (VETOEff[i][x]*VETOAct[i]*0.002)
                VETO_N[i][x] = (VETO_Nr[i][x]*VETOAct[i]*0.002)
            else:
                VETO_P[i][x] = VETOAct[i]*VETOEff[i][x]
                VETO_N[i][x] = VETOAct[i]*VETO_Nr[i][x]
            VETOBGErr[i][x] = ErrProp(VETOErr[i][x], VETOEff[i][x], VETO_P[i][x])
            VETOBGrErr += VETOBGErr[i][x]
            print('BG due to ' + VETO.IsoDecay[i][x] + ' = %.5e +/- %.5e' % (VETO_P[i][x], VETOBGErr[i][x]))   
    for i in range(len(VETO_P)):
        VETOBGr_P += sum(VETO_P[i])
    for i in range(len(VETO_N)):
        VETOBGr_N += sum(VETO_N[i])
    #print('Accidental BG for VETO = %.5e' % VETO_Acc) 
    print('Total BG due to VETO = %.5e +/- %.5e' % (VETOBGr_P, VETOBGrErr))
    totBG_P += VETOBGr_P
    totBG_N += VETOBGr_N
    ##TANK
    TANKBG_P = [[0 for x in range(len(TANKEff[i]))] for i in range(len(TANKEff))]
    TANKBG_N = [[0 for x in range(len(TANKEff[i]))] for i in range(len(TANKEff))]
    TANKBGErr = TANKErr
    TANKBGr_P = 0
    TANKBGr_N = 0
    TANKBGrErr = 0
    #TANK_Acc = AccBG(TANK_Pr, TANK_Nr)
    print('##########################################')
    print('BG for TANK')
    for i in range(len(Iso.TANK)):
        print('##########################################')
        print(Iso.TANK[i] + ' chain')
        for x in range(len(TANK.IsoDecay[i])):
            if TANK.IsoDecay[i][x] == 'Tl210':
                TANKBG_P[i][x] = (TANKEff[i][x]*TANKAct[i]*0.002)
                TANKBG_N[i][x] = (TANK_Nr[i][x]*TANKAct[i]*0.002)
            else:
                TANKBG_P[i][x] = TANKAct[i]*TANKEff[i][x]
                TANKBG_N[i][x] = TANKAct[i]*TANK_Nr[i][x]
            TANKBGErr[i][x] = ErrProp(TANKErr[i][x], TANKEff[i][x], TANKBG_P[i][x])
            TANKBGrErr += TANKBGErr[i][x]
            print('BG due to ' + TANK.IsoDecay[i][x] + ' = %.5e +/- %.5e' % (TANKBG_P[i][x], TANKBGErr[i][x]))
    for i in range(len(TANKBG_P)):
        TANKBGr_P += sum(TANKBG_P[i])
    for i in range(len(TANKBG_N)):    
        TANKBGr_N += sum(TANKBG_N[i])
    totBG_P += TANKBGr_P
    totBG_N += TANKBGr_N
    #print('Accidental BG for TANK = %.5e' % TANK_Acc)
    print('Total BG due to TANK = %.5e +/- %.5e' % (TANKBGr_P, TANKBGrErr))
    ##CONC
    CONCBG_P = [[0 for x in range(len(CONCEff[i]))] for i in range(len(CONCEff))]
    CONCBG_N = [[0 for x in range(len(CONCEff[i]))] for i in range(len(CONCEff))]
    CONCBGErr = CONCErr
    CONCBGr_P = 0
    CONCBGr_N = 0
    CONCBGrErr = 0
    #CONC_Acc = AccBG(CONC_Pr, CONC_Nr)
    print('##########################################')
    print('BG for CONC')
    for i in range(len(Iso.CONC)):
        print('##########################################')
        print(Iso.CONC[i] + ' chain')
        for x in range(len(CONC.IsoDecay[i])):
            if CONC.IsoDecay[i][x] == 'Tl210':
                CONCBG_P[i][x] = (CONCEff[i][x]*CONCAct[i]*0.002)
                CONCBG_N[i][x] = (CONC_Nr[i][x]*CONCAct[i]*0.002)
            else:
                CONCBG_P[i][x] = CONCAct[i]*CONCEff[i][x]
                CONCBG_N[i][x] = CONCAct[i]*CONC_Nr[i][x]
            CONCBGErr[i][x] = ErrProp(CONCErr[i][x], CONCEff[i][x], CONCBG_P[i][x])
            CONCBGrErr += CONCBGErr[i][x]
            print('BG due to ' + CONC.IsoDecay[i][x] + ' = %.5e +/- %.5e' % (CONCBG_P[i][x], CONCBGErr[i][x]))
    for i in range(len(CONCBG_P)):
        CONCBGr_P += sum(CONCBG_P[i])
    for i in range(len(CONCBG_N)):
        CONCBGr_N += sum(CONCBG_N[i])
    #print('Accidental BG for CONC = %.5e' % CONC_Acc)
    print('Total BG due to CONC = %.5e +/- %.5e' % (CONCBGr_P, CONCBGErr[i][x]))
    totBG_P += CONCBGr_P
    totBG_N += CONCBGr_N
    ##ROCK
    ROCKBG_P = [[0 for x in range(len(ROCKEff[i]))] for i in range(len(ROCKEff))]
    ROCKBG_N = [[0 for x in range(len(ROCKEff[i]))] for i in range(len(ROCKEff))]
    ROCKBGErr = ROCKErr
    ROCKBGr_P = 0
    ROCKBGr_N = 0
    ROCKBGrErr = 0
    print('##########################################')
    print('BG for ROCK')
    for i in range(len(Iso.ROCK)):
        print('##########################################')
        print(Iso.ROCK[i] + ' chain')
        for x in range(len(ROCK.IsoDecay[i])):
            if ROCK.IsoDecay[i][x] == 'Tl210':
                ROCKBG_P[i][x] = (ROCKEff[i][x]*ROCKAct[i]*0.002)
                ROCKBG_N[i][x] = (ROCK_Nr[i][x]*ROCKAct[i]*0.002)
            else:
                ROCKBG_P[i][x] = ROCKAct[i]*ROCKEff[i][x]
                ROCKBG_N[i][x] = ROCKAct[i]*ROCK_Nr[i][x]
            ROCKBGErr[i][x] = ErrProp(ROCKErr[i][x], ROCKEff[i][x], ROCKBG_P[i][x])
            ROCKBGrErr += ROCKBGErr[i][x]
            print('BG due to ' + ROCK.IsoDecay[i][x] + ' = %.5e +/- %.5e' % (ROCKBG_P[i][x], ROCKBGErr[i][x]))
    for i in range(len(ROCKBG_P)):
        ROCKBGr_P += sum(ROCKBG_P[i])
    for i in range(len(ROCKBG_N)):
        ROCKBGr_N += sum(ROCKBG_N[i])
    totBG_P += ROCKBGr_P
    totBG_N += ROCKBGr_N
    #print('Accidental BG for ROCK = %.5e' % ROCK_Acc)
    print('Total BG due to ROCK = %.5e +/- %.5e' % (ROCKBGr_P, ROCKBGrErr))
    ##WATER
    WATERBG_P = [[0 for x in range(len(WATEREff[i]))] for i in range(len(WATEREff))]
    WATERBG_N = [[0 for x in range(len(WATEREff[i]))] for i in range(len(WATEREff))]
    WATERBGErr = WATERErr
    WATERBGr_P = 0
    WATERBGr_N = 0
    WATERBGrErr = 0
    #WATER_Acc = AccBG(WATER_Pr, WATER_Nr)
    print('##########################################')
    print('BG for WATERVOLUME')
    for i in range(len(Iso.WATER)):
        print('##########################################')
        print(Iso.WATER[i] + ' chain')
        print(WATEREff, WATERAct)
        print(WATER_Nr)
        for x in range(len(WATER.IsoDecay[i])):
            if WATER.IsoDecay[i][x] == 'Tl210':
                WATERBG_P[i][x] = (WATEREff[i][x]*WATERAct[i]*0.002)
                WATERBG_N[i][x] = (WATEREff[i][x]*WATERAct[i]*0.002)
            else:
                WATERBG_P[i][x] = WATERAct[i]*WATEREff[i][x]
                WATERBG_N[i][x] = WATERAct[i]*WATER_Nr[i][x]
            WATERBGErr[i][x] = ErrProp(WATERErr[i][x], WATEREff[i][x], WATERBG_P[i][x])
            WATERBGrErr += WATERBGErr[i][x]
            print('BG due to ' + WATER.IsoDecay[i][x] + ' = %.5e +/- %.5e' % (WATERBG_P[i][x], WATERBGErr[i][x]))
    for i in range(len(WATERBG_P)):
        WATERBGr_P += sum(WATERBG_P[i])
    for i in range(len(WATERBG_N)):
        WATERBGr_N += sum(WATERBG_N[i])
    print('Total BG due to WATER = %.5e +/- %.5e' % (WATERBGr_P, WATERBGrErr))
    totBG_P += WATERBGr_P
    totBG_N += WATERBGr_N
    ##GD
    GDBG_P = [[0 for x in range(len(GDEff[i]))] for i in range(len(GDEff))]
    GDBG_N = [[0 for x in range(len(GDEff[i]))] for i in range(len(GDEff))]
    GDBGErr = GDErr
    GDBGr_P = 0
    GDBGr_N = 0
    GDBGrErr = 0
    print('##########################################')
    print('BG for GD')
    for i in range(len(Iso.GD)):
        print('##########################################')
        print(Iso.GD[i] + ' chain')
        for x in range(len(GD.IsoDecay[i])):
            if GD.IsoDecay[i][x] == 'Tl210':
                GDBG_P[i][x] = (GDEff[i][x]*GDAct[i]*0.002)
                GDBG_N[i][x] = (GD_Nr[i][x]*GDAct[i]*0.002)
            else:
                GDBG_P[i][x] = GDAct[i]*GDEff[i][x]
                GDBG_N[i][x] = GDAct[i]*GD_Nr[i][x]
            GDBGErr[i][x] = ErrProp(GDErr[i][x], GDEff[i][x], GDBG_P[i][x])
            GDBGrErr += GDBGErr[i][x]
            print('BG due to ' + GD.IsoDecay[i][x] + ' = %.5e +/- %.5e' % (GDBG_P[i][x], GDBGErr[i][x]))
    for i in range(len(GDBG_P)):
        GDBGr_P += sum(GDBG_P[i])
    for i in range(len(GDBG_N)):
        GDBGr_N += sum(GDBG_N[i])
    print('Total BG due to GD = %.5e +/- %.5e' % (GDBGr_P, GDBGrErr))
    totBG_P += GDBGr_P
    totBG_N += GDBGr_N
    totAcc = totBG_P*totBG_N*0.0001*0.05*(pow(60,2)*24)
    print('##########################################')
    print('Total Accidental rate = %.5e /day' % totAcc)
    print('Total BG rate = %.5e Hz' % totBG_P)
    return totBG_P, totAcc, PMT_P, VETO_P, TANKBG_P, CONCBG_P, ROCKBG_P, WATERBG_P, GDBG_P
def tdcalc(BG):
    #get signal rate
    try:
        signal = literal_eval(input('Input signal rate: '))
        signal > 0
        print('Signal rate set to = %.5e' % signal)
    except:
        signal = 0.564
        print('Signal set to default value = %.5e' % signal)
    #calculate td
    B = signal*1.035 + BG
    S = signal*0.9
    sigma = 4.65
    td = pow(sigma, 2)*(B+((B+S)/(3/2)))*(1/pow(S,2)) #/((60**2)*24) #[days] 
    #convert to days
    #td /= (pow(60,2)*24)
    print('Reactor off time to detection @ 3 sigma rate = %.5e' % td + ' days')
    return td
def maxBG():
    try:
        signal = literal_eval(input('Input signal rate: '))
        signal > 0
        print('Signal rate set to = %.5e' % signal)
    except:
        signal = 0.564
        print('Signal set to default value = %.5e' % signal)
    try:
        days = literal_eval(input('Input time to dection in days: '))
        days > 0
        print('Time to detection set to = %.5e' % days)
    except:
        days = 1.19770e+2
        print('Time to detection set to default value of = %.5e' % days)
    sigma = 4.65
    S = signal*0.9
    B = (1.5*days*pow(S, 2))/(2.5*pow(sigma, 2)) - S/2.5
    MBG = B - (S*1.15)
    print('Maximum BG rate for time detection of %.5e days = %.5e' % (days, MBG))
    return MBG
def share(total, IsoBG):
    IsoShare = IsoBG
    for i in range(len(IsoBG)):
        for x in range(len(IsoBG[i])):
            IsoShare[i][x] /= (total*0.05*0.0001)
    return IsoShare
def revBG(CompShare, MaxBG):
    CB_BG = CompShare
    for i in range(len(CompShare)):
        for x in range(len(CompShare[i])):
            CB_BG[i][x] *= MaxBG
    return CB_BG
def CBOUT(IsoAct, BGIsoCB, Iso): #BGIso, Iso): #(, , ,COMP.IsoList)
    for i in range(len(IsoAct)):
        print('Singles Budget for %.7s = %.5e Hz' % (Iso[i], sum(BGIsoCB[i])))
        print('Accidentals Budget for %.7s = %.5e Hz' % (Iso[i], (sum(BGIsoCB[i])*0.05*0.0001)))
        print('Radioactivity Budget for %.7s = %.5e' % (Iso[i], IsoAct[i]))
        #print('Nominal singles rate for %.7s = %.5e Hz' % (Iso[i], sum(BGIso[i]))) #????
######################################################################################################
ans = menu()
while ans.lower() != 'exit':
    if ans.lower() == 'a':
        ai = True
        #get list of compoents
        compAct = inputVal('PPM')
        #change PPM values
        for i in range(len(compAct)):
            if compAct[i].upper() == 'PMT':
                print('##########################################')
                print('Input values for PPM for Iso in PMT')
                PMTPPM = Iso.setPPM(Iso.PMT, PMT.defPPM)
                PMTAct = PMT.Activity(PMTPPM)
                #print(PMTPPM)
            if compAct[i].upper() == 'VETO':
                print('##########################################')
                print('Input values for PPM for Iso in VETO')
                VETOPPM = Iso.setPPM(Iso.VETO, VETO.defPPM)
                VETOAct = VETO.Activity(VETOPPM)
            if compAct[i].upper() == 'TANK':
                print('##########################################')
                print('Input values for PPM for Iso in TANK')
                TANKPPM = Iso.setPPM(Iso.TANK, TANK.defPPM)
                TANKAct = TANK.Activity(TANKPPM)
            if compAct[i].upper() == 'CONC':
                print('##########################################')
                print('Input values for PPM for Iso in CONC')
                CONCPPM = Iso.setPPM(Iso.CONC, CONC.defPPM)
                CONCAct = CONC.Activity(CONCPPM)
            if compAct[i].upper() == 'ROCK':
                print('##########################################')
                print('Input values for PPM for Iso in ROCK')
                ROCKPPM = Iso.setPPM(Iso.ROCK, ROCK.defPPM)
                ROCKAct = ROCK.Activity(ROCKPPM)
            if compAct[i].upper() == 'WATER':
                print('##########################################')
                print('Input values for PPM for Iso in WATER')
                WATERPPM = Iso.setPPM(Iso.WATER, WATER.defPPM)
                WATERAct = WATER.Activity(WATERPPM)
            if compAct[i].upper() == 'GD':
                print('##########################################')
                print('Input values for PPM for Iso in GD')
                GDPPM = Iso.setPPM(Iso.GD, GD.defPPM)
                GDAct = GD.Activity(GDPPM)
        #set to default
        ActDefault()
        clear()
        ans = menu()
    if ans.lower() == 'e':
        ei = True
        compEff = inputVal('Efficiency')
        for i in range(len(compEff)):
            print(compEff[i].upper())
            if compEff[i].upper() == 'PMT':
                print('##########################################')
                print('Input values for Efficiency for Iso in PMT')
                PMTEff, PMTErr = Iso.setEff(PMT.IsoDecay, Iso.PMT, PMT.IsoEff, PMT.EffErr)
            if compEff[i].upper() == 'VETO':
                print('##########################################')
                print('Input values for Efficiency for Iso in VETO')
                VETOEff, VETOErr = Iso.setEff(VETO.IsoDecay, Iso.VETO, VETO.IsoEff, VETO.EffErr)
            if compEff[i].upper() == 'TANK':
                print('##########################################')
                print('Input values for Efficiency for Iso in TANK')
                TANKEff, TANKErr = Iso.setEff(TANK.IsoDecay, Iso.TANK, TANK.IsoEff, TANK.EffErr)
            if compEff[i].upper() == 'CONC':
                print('##########################################')
                print('Input values for Efficiency for Iso in CONC')
                CONCEff, CONCErr = Iso.setEff(CONC.IsoDecay, Iso.TANK, TANK.IsoEff, TANK.EffErr)
            if compEff[i].upper() == 'ROCK':
                print('##########################################')
                print('Input values for Efficiency for Iso in ROCK')
                ROCKEff, ROCKErr = Iso.setEff(ROCK.IsoDecay, Iso.ROCK, ROCK.IsoEff, ROCK.EffErr)
            if compEff[i].upper() == 'WATER':
                print('##########################################')
                print('Input values for Efficiency for Iso in WATER')
                WATEREff, WATERErr = Iso.setEff(WATER.IsoDecay, Iso.WATER, WATER.IsoEff, WATER.EffErr)
            if compEff[i].upper() == 'GD':
                print('##########################################')
                print('Input values for Efficiency for Iso in GD')
                GDEff, GDErr = Iso.setEff(GD.IsoDecay, Iso.GD, GD.IsoEff, GD.EffErr)
        #set to default
        EffDefault()
        clear()
        ans = menu()
    if ans.lower() == 'bgr':
        if ai == False:
            ActDefault()
        if ei == False:
            EffDefault()
        tot, totAcc, PMTBGrate, VETOBGrate, TANKBGrate, CONCBGrate, ROCKBGrate, WATERBGrate, GDBGrate = bgrate()
        clear()
        ans = menu()
    if ans.lower() == 'td':
        if ai == False:
            ActDefault()
        if ei == False:
            EffDefault()
        tot, totAcc, PMTBGrate, VETOBGrate, TANKBGrate, CONCBGrate, ROCKBGrate, WATERBGrate, GDBGrate = bgrate()
        timeD = tdcalc(totAcc) 
        clear()
        ans = menu()
    if ans.lower() == 'maxbg':
        i = maxBG()
        clear()
        ans = menu()
    if ans.lower() == 'cb':
        #check if activity has been changed
        if ai == False:
            ActDefault()
        #check if efficiency has been changed
        if ei == False:
            EffDefault()
        #calculate BG for comps
        tot, PMTBGrate, VETOBGrate, TANKBGrate, CONCBGrate, ROCKBGrate, WATERBGrate, GDBGrate = bgrate()
        #calculate the shares
        PMTShare = share(tot,  PMTBGrate)
        VETOShare = share(tot, VETOBGrate)
        TANKShare = share(tot, TANKBGrate)
        CONCShare = share(tot, CONCBGrate)
        ROCKShare = share(tot, ROCKBGrate)
        WATERShare = share(tot, WATERBGrate)
        GDShare = share(tot, GDBGrate)
        #calculate max BG for signal rate and td
        MBG = maxBG()
        ##revAct() calculations
        #PMT
        #print(PMTShare)
        print('##########################################')
        print('CB for PMT')
        PMT_CB_BG = revBG(PMTShare, MBG)
        PMT_CB_Act = PMT.revActivity(PMT_CB_BG, PMTEff)
        #print(PMT_CB_Act)
        CBOUT(PMT_CB_Act, PMT_CB_BG, PMT.IsoList)
        #VETO
        print('##########################################')
        print('CB for VETO')
        VETO_CB_BG = revBG(VETOShare, MBG)
        VETO_CB_Act = VETO.revActivity(VETO_CB_BG, VETOEff)
        CBOUT(VETO_CB_Act, VETO_CB_BG, VETO.IsoList)
        #TANK
        print('##########################################')
        print('CB for TANK')
        TANK_CB_BG = revBG(TANKShare, MBG)
        TANK_CB_Act = TANK.revActivity(TANK_CB_BG, TANKEff)
        CBOUT(TANK_CB_Act, TANK_CB_BG, TANK.IsoList)
        #CONC
        print('##########################################')
        print('CB for CONC')
        CONC_CB_BG = revBG(CONCShare, MBG)
        CONC_CB_Act = CONC.revActivity(CONC_CB_BG, CONCEff)
        CBOUT(CONC_CB_Act, CONC_CB_BG, TANK.IsoList)
        #ROCK
        print('##########################################')
        print('CB for ROCK')
        ROCK_CB_BG = revBG(ROCKShare, MBG)
        ROCK_CB_Act = ROCK.revActivity(ROCK_CB_BG, ROCKEff)
        CBOUT(ROCK_CB_Act, ROCK_CB_BG, ROCK.IsoList)
        #WATER
        print('##########################################')
        print('CB for WATERVOLUME')
        WATER_CB_BG = revBG(WATERShare, MBG)
        WATER_CB_Act = WATER.revActivity(WATER_CB_BG, WATEREff)
        CBOUT(WATER_CB_Act, WATER_CB_BG, WATER.IsoList)
        #GD
        print('##########################################')
        print('CB for GD')
        GD_CB_BG = revBG(GDShare, MBG)
        GD_CB_Act = GD.revActivity(GD_CB_BG, GDEff)
        CBOUT(GD_CB_Act, GD_CB_BG, GD.IsoList)
        #reset
        clear()
        ans = menu()

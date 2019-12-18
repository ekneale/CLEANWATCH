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
import os
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
PMTErr = PMT.EffErr
#VETO
VETOPPM = VETO.defPPM
VETOAct = VETO.defPPM
VETOEff = VETO.IsoEff
VETOErr = VETO.EffErr
#TANK
TANKPPM = TANK.defPPM
TANKAct = TANK.defPPM
TANKEff = TANK.IsoEff
TANKErr = TANK.EffErr
#CONC
CONCPPM = CONC.defPPM
CONCAct = CONC.defPPM
CONCEff = CONC.IsoEff
CONCErr = CONC.EffErr
#ROCK
ROCKPPM = ROCK.defPPM
ROCKAct = ROCK.defPPM
ROCKEff = ROCK.IsoEff
ROCKErr = ROCK.EffErr
#WATER
WATERPPM = WATER.defPPM
WATERAct = WATER.defPPM
WATEREff = WATER.IsoEff
WATERErr = WATER.EffErr
#GD
GDPPM = GD.defPPM
GDAct = GD.defPPM
GDEff = GD.IsoEff
GDErr = GD.EffErr
#input check
ai = False
ei = False
compAct = []
compEff = []
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
        print('Alex Healey, UoS, 2019')
        print('Options: ')
        print('- Input Values for Activity    [a]')
        print('- Input Values for Efficiency  [e]')
        print('- Calculate Background Rate    [bgr]')
        #print('- Calculate Time Detection     [td]')
        #print('- Calculate Maximum Background [maxbg]')
        #print('- Cleanliness Budget           [cb]')
        print('- Exit software                [exit]')
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
def ErrProp(EffErr, Eff, BG):
    """
    Returns error of BGR
    """
    err = 0
    if Eff != 0:
        err = BG*(EffErr/Eff)
        print(err, EffErr)
    else:
        err = 0
    return err
def bgrate():
    PMTBG = PMTEff
    PMTBGErr = PMTErr
    #PMTBGr = 0
    #PMTBGrErr = 0
    for i in range(len(Iso.PMT)):
        print('##########################################')
        print(Iso.PMT[i] + ' chain')
        for x in range(len(PMT.IsoDecay[i])):
            print(PMT.IsoDecay[i][x])
            if PMT.IsoDecay[i][x] == 'Tl210':
                PMTBG[i][x] *= (PMTEff[i][x]*0.002)
            else:
                PMTBG[i][x] *= PMTEff[i][x]
            PMTBGErr[i][x] = ErrProp(PMTErr[i][x], PMTEff[i][x], PMTBG[i][x])
            print('BG due to ' + PMT.IsoDecay[i][x] + ' = %.5e +/- %.5e' % (PMTBG[i][x], PMTBGErr[i][x]))
            if PMTEff[i][x] != 0:
                print('BG due to ' + PMT.IsoDecay[i][x] + ' = %.5e +/- %.5e' % (PMTBG[i][x], (PMTBG[i][x]*(PMTErr[i][x]/PMTEff[i][x]))))
    VETOBG = VETOEff
    VETOBGErr = VETOErr
    #VETOBGr = 0
    #VETOBGrErr = 0
    for i in range(len(Iso.VETO)):
        x = 0

#########################################################################################################
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
                PMTAct = (compAct[i].upper()).Activity(PMTPPM)
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
        bgrate()
        clear()
        ans = menu()

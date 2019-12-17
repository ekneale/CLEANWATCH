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
        #print('- Input Values for Efficiency  [e]')
        #print('- Calculate Background Rate    [bgr]')
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
def inputAct():
    iput = []
    a = input('What components would you like to input values for PPM for? [PMT/VETO/TANK?/CONC]')
    iput = a.split()
    return iput
ans = menu()
while ans.lower() != 'exit':
    if ans.lower() == 'a':
        #get list of compoents
        compAct = inputAct()
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
        if 'PMT' not in compAct:
            print('##########################################')
            print('Default values for PPM for Iso in PMT')
            Iso.disdefPPM(Iso.PMT, PMTPPM)
        elif 'VETO' not in compAct:
            print('##########################################')
            print('Default values for PPM for Iso in VETO')
            Iso.disdefPPM(Iso.VETO, VETOPPM)
        elif 'TANK' not in compAct:
            print('##########################################')
            print('Default values for PPM for Iso in TANK')
            Iso.disdefPPM(Iso.TANK, TANKPPM)
        elif 'CONC' not in compAct:
            print('##########################################')
            print('Default values for PPM for Iso in CONC')
            Iso.disdefPPM(Iso.CONC, CONCPPM)
        elif 'ROCK' not in compAct:
            print('##########################################')
            print('Default values for PPM for Iso in ROCK')
            Iso.disdefPPM(Iso.ROCK, ROCKPPM)
        elif 'WATER' not in compAct:
            print('##########################################')
            print('Default values for PPM for Iso in WATER')
            Iso.disdefPPM(Iso.WATER, WATERPPM)
        elif 'GD' not in compAct:
            print('##########################################')
            print('Default values for PPM for Iso in GD')
            Iso.disdefPPM(Iso.GD, GDPPM)

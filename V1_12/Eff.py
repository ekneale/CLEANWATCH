#imports
import ROOT
#dim vars
comp = ["PMT_", "VETO_", "TANK_", "ROCK_", "WaterVolume_", "GD_"]
iso = [["234Pa_CHAIN_238U_NA", "214Pb_CHAIN_238U_NA", "214Bi_CHAIN_238U_NA", "210Bi_CHAIN_238U_NA", "210Tl_CHAIN_238U_NA"], #U238 0
        ["228Ac_CHAIN_232Th_NA", "212Pb_CHAIN_232Th_NA","212Bi_CHAIN_232Th_NA", "208Tl_CHAIN_232Th_NA"], #Th232 1
        ["40K_40K_NA"], #K40 2
        ["214Pb_CHAIN_222Rn_NA", "214Bi_CHAIN_222Rn_NA", "210Bi_CHAIN_222Rn_NA","210Tl_CHAIN_222Rn_NA"], #Rn222 3
        ["60Co_STEEL_ACTIVITY"], #steel activity 4
        ["137Cs_STEEL_ACTIVITY"], #steel activity 5
        ["231Th_CHAIN_235U_NA", "223Fr_CHAIN_235U_NA", "211Pb_CHAIN_235U_NA", "211Bi_CHAIN_235U_NA", "207Tl_CHAIN_235U_NA"], #U235 6
        ["234Pa_CHAIN_238U_NA"], #U238_u 7
        ["228Ac_CHAIN_232Th_NA"], #Th232_u 8
        ["231Th_CHAIN_235U_NA"], #U235_u 9
        ["214Pb_CHAIN_238U_NA", "214Bi_CHAIN_238U_NA", "210Bi_CHAIN_238U_NA", "210Tl_CHAIN_238U_NA"], #U238_l 10 
        ["212Pb_CHAIN_232Th_NA","212Bi_CHAIN_232Th_NA", "208Tl_CHAIN_232Th_NA"], #Th232_l 11
        ["223Fr_CHAIN_235U_NA", "211Pb_CHAIN_235U_NA", "211Bi_CHAIN_235U_NA", "207Tl_CHAIN_235U_NA"]] #U235_l 12
#set file
outfile = ROOT.TFile("results.root", "READ")
def GetEff(compNum, chainNum):
    binNum = []
    binEff = []
    err = []
    for i in range(len(iso[chainNum])):
        hist = "histWatchman_" + comp[compNum] + iso[chainNum][i]
        binNum.append(outfile.Get(hist).FindBin(1.9, 8))
        #print(binNum[i])
        temp = outfile.Get(hist).GetBinContent(binNum[i])
        #print(temp)
        binEff.append(temp)
        err.append(outfile.Get(hist).GetBinError(binNum[i]))
    return binEff, err
#print('histWatchman_COMP_Iso_CHAIN_IsoChain_NA')
PMTU238, PMTU238Err = GetEff(0, 0)
#print('PMT U238', PMTU238)
PMTTh232, PMTTh232Err = GetEff(0, 1)
#print(PMTTh232)
PMTK40, PMTK40Err = GetEff(0, 2)
VETOU238, VETOU238Err = GetEff(1, 0)
VETOTh232, VETOTh232Err = GetEff(1, 1)
VETOK40, VETOK40Err = GetEff(1, 2)
TANKU238, TANKU238Err = GetEff(2, 0)
TANKTh232, TANKTh232Err = GetEff(2, 1)
TANKK40, TANKK40Err = GetEff(2, 2)
TANKCo60, TANKCo60Err = GetEff(2, 4)
TANKCs137, TANKCs137Err = GetEff(2,5)
#ROCKU238, ROCKU238Err = GetEff(3, 0)
#ROCKTh232, ROCKTh232Err = GetEff(3, 1)
#ROCKK40, ROCKK40Err = GetEff(3, 2)
WATERRn222, WATERRn222Err = GetEff(4, 3)
GDU238u, GDU238uErr = GetEff(5, 7)
GDTh232u, GDTh232uErr = GetEff(5, 8)
GDU235u, GDU235uErr = GetEff(5, 9)
GDU238l, GDU238lErr = GetEff(5, 10)
GDTh232l, GDTh232lErr = GetEff(5, 11)
GDU235l, GDU235lErr = GetEff(5, 12)
def ErrProp(IsoEffErr, IsoEff, BG):
    if IsoEff != 0:
        centErr = IsoEffErr/IsoEff
        IsoErr = BG*centErr
    else:
        IsoErr = 0
    return IsoErr

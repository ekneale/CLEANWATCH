#imports
import ROOT
#dim vars
comp = ["PMT_", "VETO_", "TANK_", "ROCK_", "WaterVolume_", "GD_"]
iso = [["234Pa_CHAIN_238U_NA", "214Pb_CHAIN_238U_NA", "214Bi_CHAIN_238U_NA", "210Bi_CHAIN_238U_NA", "210Tl_CHAIN_238U_NA"], #U238 
        ["228Ac_CHAIN_232Th_NA", "212Pb_CHAIN_232Th_NA","212Bi_CHAIN_232Th_NA", "208Tl_CHAIN_232Th_NA"], #Th232
        ["40K_40K_NA"], #K40
        ["214Pb_CHAIN_222Rn_NA", "214Bi_CHAIN_222Rn_NA", "210Bi_CHAIN_222Rn_NA","210Tl_CHAIN_222Rn_NA"], #Rn222
        ["60Co_STEEL_ACTIVITY", "137Cs_STEEL_ACTIVITY"], #steel activity
        ["231Th_CHAIN_235U_NA", "223Fr_CHAIN_235U_NA", "211Pb_CHAIN_235U_NA", "211Bi_CHAIN_235U_NA", "207Tl_CHAIN_235U_NA"]] #U235
#set file
outfile = ROOT.TFile("results.root", "READ")
def GetEff(compNum, chainNum):
    binNum = []
    binEff = []
    for i in range(len(iso[chainNum])):
        hist = "histWatchman_" + comp[compNum] + iso[chainNum][i]
        binNum.append(outfile.Get(hist).FindBin(1.9, 19))
        binEff.append(outfile.Get(hist).GetBinContent(binNum[i]))
    return binEff
PMTU238 = GetEff(0, 0)
PMTTh232 = GetEff(0, 1)
PMTK40 = GetEff(0, 2)
VETOU238 = GetEff(1, 0)
VETOTh232 = GetEff(1, 1)
VETOK40 = GetEff(1, 2)
TANKU238 = GetEff(2, 0)
TANKTh232 = GetEff(2, 1)
TANKK40 = GetEff(2, 2)
TANKSTEEL = GetEff(2, 4)
#ROCKU238 = GetEff(3, 0)
#ROCKTh232 = GetEff(3, 1)
#ROCKK40 = GetEff(3, 2)
WATERRn222 = GetEff(4, 3)
GDU238 = GetEff(5, 0)
GDTh232 = GetEff(5, 1)
GDU235 = GetEff(5, 5)

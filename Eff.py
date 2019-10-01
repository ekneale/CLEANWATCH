#imports
import ROOT
#dim vars
comp = ["PMT_", "VETO_", "TANK_", "ROCK_", "WaterVolume"]
iso = [["234Pa_CHAIN_238U_NA", "214Pb_CHAIN_238U_NA", "214Bi_CHAIN_238U_NA", "210Bi_CHAIN_238U_NA", "210Tl_CHAIN_238U_NA"], #U238 
        ["228Ac_CHAIN_232Th_NA", "212Pb_CHAIN_232Th_NA","212Bi_CHAIN_232Th_NA", "208Tl_CHAIN_232Th_NA"], #Th232
        ["40K_40K_NA"], #K40
        ["214Pb_CHAIN_222Rn_NA", "214Bi_CHAIN_222Rn_NA", "210Bi_CHAIN_222Rn_NA","210Tl_CHAIN_222Rn_NA"], #Rn222
        ["60Co_STEEL_ACTIVITY", "137Cs_STEEL_ACTIVITY"] ] #steel activity
binNum = []
binEff = []
#set file
outfile = ROOT.TFile("results.root", "READ")
#get bin number = outfile.Get(histname).GetBin(1.6, 13)
#get efficiency from number = outfile.Get(histname).GetBinContent(bin number)

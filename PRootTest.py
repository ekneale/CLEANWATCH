#imports
import ROOT
#read root file
outfile = ROOT.TFile("results.root", "READ")
hist = outfile.Get("histWatchman_TANK_60Co_STEEL_ACTIVITY")
binNum = outfile.Get("histWatchman_TANK_60Co_STEEL_ACTIVITY").FindBin(1.6, 13)
Eff = outfile.Get("histWatchman_TANK_60Co_STEEL_ACTIVITY").GetBinContent(binNum)
print('Bin Number = ', binNum)
print('Efficiency = ', Eff)

import Iso, Eff
from math import sqrt
mass = 1.4 #kg
n = 3258
defPPM = [0.043, 0.133, 36] #[U238, Th232, K40]
PPM = defPPM
IsoAct = defPPM
revIsoAct = defPPM
IsoList = Iso.PMT
IType = ['PPM' for i in range(len(IsoList))]
IsoDecay = [Iso.U238,
            Iso.Th232,
            Iso.K40]
IsoEff =   [Eff.PMTU238,
            Eff.PMTTh232,
            Eff.PMTK40]
#print(IsoEff)
EffErr =   [Eff.PMTU238Err,
            Eff.PMTTh232Err,
            Eff.PMTK40Err]
Err = EffErr
def Activity(PPM):
    IAct = []
    for i in range(len(PPM)):
        IAct.append(PPM[i]*((Iso.Lam[i]*Iso.Abs[i])/(Iso.Ms[i]*1e6))*mass*n)
        print('Activity due to ' + Iso.PMT[i] + ' = %.5e' % IAct[i])
    return IAct
def revActivity(BG, Eff,NEff):
    rIsoAct = [0 for i in range(len(IsoList))]
    for i in range(len(BG)):
        maxbg = max(BG[i])
        x = BG[i].index(maxbg)
        if Eff[i][x] != 0:
            rIsoAct[i] = BG[i][x]/Eff[i][x]/(mass*n)*(Iso.Ms[i]*1e6)/(Iso.Lam[i]*Iso.Abs[i])
            #print(rIsoAct[i][x])
        else:
            rIsoAct[i] = 0
    return rIsoAct
#defAct = Activity(defPPM)
#print('No Errors')

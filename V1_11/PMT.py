import Iso, Eff
mass = 1.4 #kg
n = 3258
defPPM = [0.043, 0.133, 36] #[U238, Th232, K40]
PPM = defPPM
IsoAct = defPPM
revIsoAct = defPPM
IsoList = Iso.PMT
IsoDecay = [Iso.U238,
            Iso.Th232,
            Iso.K40]
IsoEff =   [Eff.PMTU238,
            Eff.PMTTh232,
            Eff.PMTK40]
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
def revActivity(BG, Eff):
    rIsoAct = []
    for i in range(len(BG)):
        maxbg = max(BG[i])
        x = BG[i].index(maxbg)
        if Eff[i][x] != 0:
            rIsoAct.append(BG[i][x]/Eff[i][x])*(1/(mass*n))*((Iso.Ms[i]*1e6)/(Iso.Lam[i]*Iso.Abs[i]))
        else:
            revIsoAct.append(0)
    return rIsoAct
#defAct = Activity(defPPM)
#print('No Errors')

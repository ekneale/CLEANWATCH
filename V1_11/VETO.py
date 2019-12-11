import Iso, Eff
mass = 1.4
n = 296
PPM = [0.043, 0.133, 36]
IsoAct = PPM
revIsoAct = PPM
IsoList = Iso.VETO
IsoDecay = [Iso.U238,
            Iso.Th232,
            Iso.K40]
IsoEff =   [Eff.VETOU238,
            Eff.VETOTh232,
            Eff.VETOK40]
EffErr =   [Eff.VETOU238Err,
            Eff.VETOTh232Err,
            Eff.VETOK40Err]
Err = EffErr
def Actvity(PPM):
    for i in range(len(PPM)):
        IsoAct[i] = PPM[i]*((Iso.Lam[i]*Abs[i])/(Ms[i]*1e6))*mass*n
def revActivity(BG, Eff):
    for i in range(len(BG)):
        maxbg = max(BG[i])
        x = BG[i].index(maxbg)
        if Eff[i][x] != 0:
            revIsoAct[i] = (BG[i][x]/Eff[i][x])*(1/(mass*n))*((Iso.Ms[i]*1e6)/Iso.Lam[i]*Iso.Abs[i])
        else:
            revIsoAct[i] = 0
#print('No Errors')

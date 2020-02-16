import Iso, Eff
mass = 1.4
n = 296
defPPM = [0.043, 0.133, 36]
IsoAct = defPPM
revIsoAct = defPPM
IsoList = Iso.VETO
IType = ['PPM' for i in range(len(IsoList))]
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
def Activity(PPM):
    IAct = []
    for i in range(len(PPM)):
        IAct.append(PPM[i]*((Iso.Lam[i]*Iso.Abs[i])/(Iso.Ms[i]*1e6))*mass*n)
        print('Activity due to ' + Iso.VETO[i] + ' = %.5e' % IAct[i])
    return IAct
def revActivity(BG, Eff,NEff):
    rIsoAct = [0 for i in range(len(IsoList))]
    for i in range(len(BG)):
        maxbg = max(BG[i])
        x = BG[i].index(maxbg)
        if Eff[i][x] != 0:
            rIsoAct[i] = (BG[i][x]/Eff[i][x]*BG[i][x]/NEff[i][x])*(1/(mass*n))*((Iso.Ms[i]*1e6)/Iso.Lam[i]/Iso.Abs[i])
        else:
            rIsoAct[i] = 0
    return rIsoAct
#print('No Errors')

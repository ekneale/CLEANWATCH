from ast import literal_eval
#Properties
Ms = [3.953e-25, 3.853145e-25, 6.636286e-26] #Mass [kg] [U238, Th232, K40]
Lam = [4.916e-18, 1.57e-18, 1.842e-18] #decay constant [U238, Th232, K40]
Abs = [1, 1, 0.000117] #natural abundance [U238, Th232, K40]
#Component Isotopes
PMT =  ['U238', 'Th232', 'K40']
VETO = ['U238', 'Th232', 'K40']
TANK = ['U238', 'Th232', 'K40', 'Co60', 'Cs137']
CONC = ['U238', 'Th232', 'K40']
#TANK = ['U238', 'Th232', 'K40']
ROCK = ['U238', 'Th232', 'K40', 'Fn']
WATER= ['Rn222', 'Rn']
GD =   ['U238', 'Th232', 'U235', 'U238_l', 'Th232_l', 'U235_l']
#Decay Chains
U238 =  ['Pa234', 'Pb214', 'Bi214', 'Bi210', 'Tl210']
Th232 = ['Ac228', 'Pb212', 'Bi211', 'Tl208']
U235 =  ['Th231', 'Fr223', 'Pb211', 'Bi211', 'Tl207']
K40 =   ['K40']
Co60 =  ['Co60']
Cs137 = ['Cs137']
Rn222 = ['Pb214', 'Bi214', 'Bi210', 'Tl210']
FN =    ['Fn']
RN =    ['Rn']
def setPPM(Iso, PPM, Itype):
    output = []
    for i in range(len(Iso)):
        #try:
        #    a = literal_eval(input('Input PPM for ' + Iso[i] + ': '))
        #    a >= 0
        #    output.append(a)
        #    print('PPM for ' + Iso[i] + ' = %.5e' % output[i])
        #except:
        #    output.append(PPM[i])
        #    print('PPM for ' + Iso[i] + ' set to default value of = %.5e' % output[i])
        x = input('Input ' + Itype[i] + ' for ' + Iso[i] + ': ')
        if len(x) == 0:
            output.append(PPM[i])
            print(Itype[i] + ' for ' + Iso[i] + ' set to default value of = %.5e' % output[i])
        elif 'e' in x:
            x = literal_eval(x)
            if x >= 0:
                output.append(x)
                print(Itype[i] + ' for ' + Iso[i] + ' = %.5e' % output[i])
            else:
                output.append(PPM[i])
                print(Itype[i] + ' for ' + Iso[i] + ' set to default value of = %.5e' % PPM[i])
        else:
            x = x.lower()
            if x[-1] == 'x' and len(x) > 1:
                x = x.replace('x', '')
                x = int(x)
                if x >= 0:
                    output.append(x*PPM[i])
                    print(Itype[i] + ' for ' + Iso[i] + ' = %.5e' % output[i])
                    continue
                else:
                    output.append(PPM[i])
                    print(Itype[i] + ' for ' + Iso[i] + ' set to default value of = %.5e' % output[i])
                    continue
            else:
                try:
                    x = int(x)
                except:
                    output.append(PPM[i])
                    print(Itype[i] + ' for ' + Iso[i] + ' set to default value of = %.5e' % output[i])
                    continue #skips to next iteration?
            if x < 0 or type(x) != int:
                output.append(PPM[i])
                print(Itype[i] + ' for ' + Iso[i] + ' set to default value of = %.5e' % output[i])
            else:
                output.append(x)
                print(Itype + ' for ' + Iso[i] + ' = %.5e' % output[i])
    return output
def disdef(Iso, val, t):
    for i in range(len(Iso)):
        print(t + ' for ' + Iso[i] + ' set to default value = %.5e' % val[i])
def EffInput(Iso, IEff):
    #try:
    #    a = literal_eval(input('Input Efficiency for ' + Iso + ': '))
    #except:
    #    a = IEff
    #    print('Efficiency for ' + Iso + ' set to default value')
    a = input('Input Efficiency for ' + Iso + ': ')
    if len(a) == 0:
        a = IEff
        print('Efficiency for ' + Iso + ' set to default value %.5e' % a)
    elif 'e' in a:
        a = literal_eval(a)
        if a >= 0:
            print('Efficiency for ' + Iso + ' = %.5e' % a)
        else:
            a = IEff
            print('Efficiency for ' + Iso + ' set to default value %.5e' % a)
    else:
        a = a.lower()
        if a[-1] == 'x':
            a = a.replace('x', '')
            a = int(a)
            if a >= 0:
                a *= IEff
                print('Efficiency for ' + Iso + ' = %.5e' % a)
            else:
                a = IEff
                print('Efficiency for ' + Iso + ' set to default value %.5e' % a)
        else:
            try:
                a = int(a)
            except:
                a = IEff
                print('Efficiency for ' + Iso + ' set to default value %.5e' % a)
                #break
        if a < 0:
            a = IEff
            print('Efficiency for ' + Iso + ' set to default value %.5e' % a)
        else:
            pass
    return a
def ErrInput(Iso, Eff):
    b = input('Input Efficiency Error for ' + Iso + ': ')
    if len(b) == 0:
        b = Eff
        print('Efficiency for ' + Iso + ' set to default value of = %.5e' % b)
    elif 'e' in b:
        b = literal_eval(b)
        if b >= 0:
            print('Efficiency Error for ' + Iso + ' = %.5e' % b)
        else:
            b = Eff
            print('Efficiency Error for ' + Iso + ' set to default value of = %.5e' % b)

    else:
        b = b.lower()
        if b[-1] == 'x':
            b = b.replace('x', '')
            b = int(b)
            if b >= 0:
                b *= Eff
                print('Efficiency Error for ' + Iso + ' = %.5e' % b)
            else:
                b = Eff
                print('Efficiency Error for ' + Iso + ' set to default value of = %.5e' % b)
        else:
            try:
                b = int(b)
            except:
                b = Eff
                print('Efficiency Error for ' + Iso + ' set to default value of = %.5e' % b)
                #break
        if b < 0:
            b = Eff
            print('Efficiency Error for ' + Iso + ' set to default value of = %.5e' % b)
        else:
            pass
    return b
def setEff(IsoDecay, Iso, IsoEff, IsoErr):
    IEff = IsoEff
    IErr = IsoErr
    for i in range(len(IsoDecay)):
        print('##########################################')
        print(Iso[i] + ' chain')
        for x in range(len(IsoDecay[i])):
            IEff[i][x] = EffInput(IsoDecay[i][x], IEff[i][x])
            IErr[i][x] = ErrInput(IsoDecay[i][x], IEff[i][x])
        return IEff, IErr
def BGrate(Act, Eff, Decay):
    t = 0
    Err = Eff
    for i in range(len(IsoDecay)):
        for x in range(len(IsoDecay[i])):
            if IsoDecay[i][x] == 'Tl210':
                IsoBG[i].append(IsoAct[i]*IsoEff[i][x]*0.002)
            else:
                IsoBG[i].append(IsoAct[i]*IsoEff[i][x])
            Err[i].append(Eff.ErrProp(EffErr[i][x], IsoEff[i][x], IsoBG[i][x]))
            print('BG rate for ' + IsoDecay[i][x] + ' = %.5e +/- %.5e' % (IsoBG[i][x], Err[i][x]))
        t += sum(IsoBG[i])
    return t


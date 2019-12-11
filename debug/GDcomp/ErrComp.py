import matplotlib.pyplot as plt
from scipy.stats import linregress
IsoU238 = ['Pa234', 'Bi214', 'Bi210', 'Tl210']
IsoTh232 = ['Ac228', 'Bi212', 'Tl208']
ErrU238 = [1.01074e+2, 1.84121e+2, 1.18216e+0, 1.21467e+0]
ErrTh232 = [1.30037e+1, 8.42287e+1, 8.44060e+2]
ErrU238_l = [8.96144e+5, 1.63245e+6, 1.04812e+4, 2.15389e+1]
ErrTh232_l = [1.15293e+5, 7.46787e+5, 7.48359e+6]
yfitU238 = []
xfitU238 = []
yfitTh232 = []
xfitTh232 = []
U238_m, U238_i, U238_r, U238_p, U238_stderr = linregress(ErrU238, ErrU238_l)
Th232_m, Th232_i, Th232_r, Th232_p, Th232_stderr = linregress(ErrTh232, ErrTh232_l)
for i in range(int(min(ErrU238)), int(max(ErrU238)), 1000):
    xfitU238.append(i)
    yfitU238.append(U238_m*i + U238_i)
print('U238 Chains')
for i in range(len(IsoU238)):
    if IsoU238[i] != 'Tl210':
        print(IsoU238[i] + '_l / ' + IsoU238[i] + ' = %.5e' % (ErrU238_l[i]/ErrU238[i]))
    else:
        print(IsoU238[i] + '_l / ' + IsoU238[i] + ' = %.5e' % ((ErrU238_l[i]/ErrU238[i])/0.002))

print('U238_r = %.5e' % U238_r)    
#print('Tl210 / Tl210_l = %.5e' % (ErrU238[-1]/ ErrU238_l[-1]))
print('Th232 Chains')
for i in range(len(IsoTh232)):
    if ErrTh232[i] != 0:
        print(IsoTh232[i] + '_l / ' + IsoTh232[i] + ' = %.5e ' % (ErrTh232_l[i]/ErrTh232[i]))
    else:
        pass
print('Th232_r = %.5e' % Th232_r)
#plt.plot(ErrU238, ErrU238_l, label=r'/frac{U238_l}{U238}')
#plt.plot(xfitU238, yfitU238, label = 'fit')
#plt.legend(loc='best')
#plt.show()
#plt.plot(ErrTh232, ErrTh232_l, label=r'/frac{Th232_l}{Th232}')
#plt.plot(xfitTh232, yfitTh232, label = 'fit')
#plt.legend(loc='best')

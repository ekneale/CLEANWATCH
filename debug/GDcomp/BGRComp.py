import matplotlib.pyplot as plt
IsoU238 = ['Pa234', 'Pb214', 'Bi214', 'Bi210', 'Tl210']
IsoTh232 = ['Ac228', 'Pb212', 'Bi212', 'Tl208']
U238 = [1.44392, 0, 2.63030, 1.68880e-2, 1.73524e-2]
U238_l = [4.04298e-2, 0, 7.36484e-2, 4.72863e-4, 4.85867e-4]
Th232 = [3.71535e-3, 0, 2.40653e-2, 2.41160e-1]
Th232_l = [6.50186e-3, 0, 4.21143e-2, 4.22030e-1]
print('U238 chains')
for i in range(len(IsoU238)):
    if U238[i] != 0:
        print(IsoU238[i] + '/' + IsoU238[i] + '_l = %.5e ' % (U238[i]/U238_l[i]))
print('Th232 chains')
for i in range(len(IsoTh232)):
    if Th232[i] != 0:
        print(IsoTh232[i] + '/' + IsoTh232[i] + '_l = %.5e' % (Th232[i]/Th232_l[i]))

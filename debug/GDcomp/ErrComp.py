import matplotlib.pyplot as plt
IsoU238 = ['Pa234', 'Pb214', 'Bi214', 'Bi210', 'Tl210']
IsoTh232 = ['Ac228', 'Pb212', 'Bi212', 'Tl208']
ErrU238 = [1.44392, 0, 2.63030, 1.68880e-2, 1.73524e-2]
ErrTh232 = [3.71535e-3, 0, 2.40653e-2, 2.41160e-1]
ErrU238_l = [5.12082, 0, 9.32828, 5.98927e-2, 1.23079e-4]
ErrTh232_l = [1.64705e-2, 0, 1.06684e-1, 1.06908]
print('U238 Chains')
for i in range(len(IsoU238)):
    if ErrU238[i] != 0:
        print(IsoU238[i] + '_l / ' + IsoU238[i] + ' = %.5e' % (ErrU238_l[i]/ErrU238[i]))
    else:
        pass
#print('Tl210 / Tl210_l = %.5e' % (ErrU238[-1]/ ErrU238_l[-1]))
print('Th232 Chains')
for i in range(len(IsoTh232)):
    if ErrTh232[i] != 0:
        print(IsoTh232[i] + '_l / ' + IsoTh232[i] + ' = %.5e ' % (ErrTh232_l[i]/ErrTh232[i]))
    else:
        pass

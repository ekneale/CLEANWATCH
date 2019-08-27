import matplotlib.pyplot as plt
IsoVal = [1.79315e+4, 2.01216e+4, 3.65110e+3, 4.17627e+4, 3.62900e+2, 1.91087e+4, 5.64652e+4, 8.35142e+3, 4.16408e+4, 1.73059e+4]
IsoLab = ['Pa234', 'Ac228', 'Pb214', 'Bi214', 'Pb212', 'Bi212', 'Tl210', 'Bi210', 'Tl208', 'K40']
#plt.pie(IsoVal, labels = IsoLab, autopct = '%1.3e%%')
#plt.show()
#plt.bar(IsoLab, IsoVal)
#plt.show()
##percentage
tot = sum(IsoVal)
#output
for i in range(len(IsoVal)):
#    plt.bar(IsoLab[i], IsoVal[i]/tot)
    print(IsoLab[i] + ' = %.5e' % (IsoVal[i]/tot))
#plt.show()

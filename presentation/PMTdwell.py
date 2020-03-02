import matplotlib.pyplot as plt
time  = [8, 9, 10, 11, 12, 13, 14]
U238  = [3.15563, 4.33956, 5.48531, 6.66925, 7.81499, 8.96074, 1.01447e+1]
Th232 = [1.85434e+1, 2.55005e+1, 3.22333e+1, 3.91904e+1, 4.59232e+1, 5.26559e+1, 5.96131e+1]
K40   = [4.24129e-2, 5.83254e-2, 7.37247e-2, 8.96373e-2, 1.05037e-1, 1.20436e-1, 1.36348e-1]
plt.plot(time, U238, label='U238')
plt.plot(time, Th232, label='Th232')
plt.plot(time, K40, label='K40')
plt.legend()
plt.xticks(time)
plt.xlabel('Dwell times [months]')
plt.ylabel('PPM')
plt.title('PMT Radioactivity Budgets')
plt.savefig(r'PMTBudg.png')
plt.show()

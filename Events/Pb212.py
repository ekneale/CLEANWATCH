from statistics import mean
import matplotlib.pyplot as plt
PMT = [214, 173, 192, 199, 210, 198, 178, 197, 220, 216, 206, 185, 201, 193, 199, 179, 216, 181, 220, 226, 233, 214, 201, 211, 241, 196, 210, 183, 209, 195, 224, 164, 199, 216, 207, 210, 227, 194, 206, 203]
VETO = [153, 162, 173, 158, 165, 148, 164, 161, 172, 152, 166, 165, 148, 165, 125, 163, 163, 140, 184, 128, 172, 149, 134, 144, 171, 141, 185, 138, 165, 153, 156, 144, 164, 168, 170, 163, 173, 158, 175, 146]
TANK = [1, 3, 1, 3, 2, 3, 2, 2, 4, 3, 4, 1, 1, 2, 4, 3, 2, 3, 5, 3, 1, 4, 1, 2, 4, 1, 3, 2, 1, 2, 1, 0, 2, 2, 5, 0, 3, 0, 0, 0]
CONC = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ROCK = [0] #sim not finished yet 13/08/19
PMT_m = mean(PMT)
VETO_m = mean(VETO)
TANK_m = mean(TANK)
CONC_m = mean(CONC)
ROCK_m = mean(ROCK)
#plt.pie([PMT_m, VETO_m, TANK_m, CONC_m, ROCK_m], explode = [0.1, 0.1, 0.1, 0.1, 0.1], labels = ['PMT', 'VETO', 'TANK', 'CONC', 'ROCK'], autopct = '%1.3e%%')
#plt.title('using sim data')
#plt.show()
tot = PMT_m + VETO_m + TANK_m + CONC_m + ROCK_m
print('Pb212')
print('PMT = %.5e' % (PMT_m/tot))
print('VETO = %.5e' % (VETO_m/tot))
print('TANK = %.5e' % (TANK_m/tot))
print('CONC = %.5e' % (CONC_m/tot))
print('ROCK = %.5e' % (ROCK_m/tot))
print('Total Events = %.5e' % tot)

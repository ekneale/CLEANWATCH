import matplotlib.pyplot as plt
from math import pow
x = list(range(10))
print(x)
S = 0.387*0.9
sigma = 4.65
def calc(t):
    y = []
    for i in range(len(t)):
        y.append((S/20)*((12*t[i]*S - 27)/pow(sigma, 2)))
    return y
MBG = calc(x)
plt.plot(x, MBG)
plt.show()

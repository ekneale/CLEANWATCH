import matplotlib.pyplot as plt
signal = 0.387
tconst = 365/12
print(int(14*tconst)+1)
days = [i for i in range(100, int(14*tconst)+1)] #0-500 days, 10 day interval
bgr = [0 for i in range(len(days))]
ticks = [i*tconst for i in range(8, 15)]
#print('%.3e' % max(days))
sigma = 4.65
#y=mx+c
def mbg(days):
    S = signal*0.9
    B = (1.5*days*pow(S, 2))/(2.5*pow(sigma, 2)) - S/2.5
    MBG = B - (S*1.15)
    return MBG
#generate y points
for i in range(len(days)):
    bgr[i] = mbg(days[i])
#print(min(bgr)) - doesnt work bc of -ve values in list
minval = 1
for i in range(len(bgr)):
    if bgr[i] > 0 and minval > bgr[i]:
        minval = bgr[i]
        break
xlim = days[bgr.index(minval)]
print(xlim)
xax = []
yax = []
for i in range(len(days)):
    yax.append(0)
    xax.append(xlim)
#plot data
plt.plot(days, bgr)
#format axis
plt.xlabel('Dwell time [days]')
plt.ylabel('Max BG allowed [Hz]')
#axis lines
plt.plot(days, yax, color='k')
plt.plot(xax, bgr, color='k')
#tick where bgr = 0
plt.xticks(ticks + [xlim])
#show plot
plt.show() 

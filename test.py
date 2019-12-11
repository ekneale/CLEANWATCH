import numpy as np
from math import pow
import Eff
PPM = [1, 1, 1, 1, 1, 1]
Iso = ['U238', 'Th232', 'U235', 'U238_l', 'Th232_l', 'U235_l']
IsoDecay = [[], #U238
            [], #Th232
            [], #U235
            [], #U238_l
            [], #Th232_l
            []] #U235_l
GDIsoEff = [Eff.GDU238,   #U238
            Eff.GDTh232,  #Th232
            Eff.GDU235,   #U235
            Eff.GDU238,   #U238_l
            Eff.GDTh232,  #Th232_l
            Eff.GDU235]   #U235_l

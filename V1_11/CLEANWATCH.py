import GD
BGtot = 0
argstring = """
    Usage: CLEANWATCH.py [options]
    Arguments:
    Options:
        --PPM=<component> #Enter values of PPM for GD component
        --Eff=<component> #Enter values of Efficiency for GD component
    """
import docopt
arguments = docopt.docopt(argstring)
#if (arguments['--PPM']=='GD'):
Iso.setPPM(GD.IsoList, GD.PPM)
#if (arguments['--Eff']=='GD'):
#   GD.setEff()
#GD.Activity()
#BGtot += GD.BGrate()
#do for all components then do reverse calculation
#share()
#revAct()

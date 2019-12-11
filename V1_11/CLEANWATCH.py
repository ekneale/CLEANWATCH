import docopt
import GD
BGtot = 0
argstring = """
    Usage: CLEANWATCH.py [options]
    Arguments:
    Options:
        --PPM=<GD> #Enter values of PPM for GD component
        --Eff=<GD> #Enter values of Efficiency for GD component
    """
arguments = docopt.docopt(argstring)
#if (arguments['--PPM']=='GD'):
#   GD.setPPM()
#if (arguments['--Eff']=='GD'):
#   GD.setEff()
#GD.Activity()
#BGtot += GD.BGrate()

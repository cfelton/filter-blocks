import myhdl as hdl
from myhdl import Signal, intbv, StopSimulation
from filter_blocks.support import Clock, Reset, Global, Samples
from filter_blocks.fir import fir_df1
from filter_blocks.fda import FilterFIR
import matplotlib.pyplot as pl
import numpy as np

def main():

    hdlfilter = FilterFIR(0,0)
    b=[1,2,3,1]
    hdlfilter.set_coefficients(b)
    hdlfilter.set_stimulation(np.ones(100))
    testfil = hdlfilter.filter_block()
    testfil.run_sim()
    
if __name__ == '__main__':
    main()

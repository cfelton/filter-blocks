import myhdl as hdl
from filter_blocks.support import Samples
from .filter_hw import FilterHardware
from ..fir import fir_df1

from myhdl import Signal, intbv, StopSimulation
from filter_blocks.support import Clock, Reset, Global, Samples
from filter_blocks.fda import fir_test as ft
import matplotlib.pyplot as pl
import numpy as np

class FilterFIR(FilterHardware):
    def __init__(self, b, a):
        super().__init__(b, a)
        self.filter_type = 'direct_form'
        self.n_cascades = 0
        self.direct_form_type = 1
        self.sigin = np.array([])
        self.response = []

    def set_cascade(self, n_cascades):
        self.n_cascades = n_cascades
    
    def set_coefficients(self, coefficients):
        self.b = coefficients

    def set_stimulation(self, sigin):
        self.sigin = sigin.tolist()

    def get_response(self):
        return self.response

    def runsim(self):
        pass
        
    @hdl.block
    def filter_block(self):
        # this elaboration code will select the different structure and implementations
        # x = Signal(intbv(0)[20:])
        # y = Signal(intbv(0)[20:])
        w = (25,24,0)
        ymax = 2**(w[0]-1)
        vmax = 2**(2*w[0])
        xt = Samples(-vmax, vmax)
        yt = Samples(-vmax, vmax)
        xt.valid = bool(1)
        clock = Clock(0, frequency=50e6)
        reset = Reset(1, active=0, async=True)
        glbl = Global(clock, reset)
        
        tbclk = clock.process()

        numsample = 0

        for k in self.sigin:
            numsample += 1 
        
        rec_insts = yt.process_record(clock, num_samples=numsample)


        if self.filter_type == 'direct_form':
            if self.direct_form_type == 1:
                # all filters will need the same interface ports, this should be do able
                dfilter = fir_df1.filter_fir

            if self.n_cascades > 0:
                filter_insts = [None for _ in range(self.n_cascades)]
                for ii in range(self.n_cascades):
                    pass
 #                   filter_insts[ii] = fir_df1.filter_fir(
 #                       glbl, sigin[ii], sigout[ii], b
 #                   )
            else:
                filter_insts = dfilter(glbl, xt, yt, self.b, self.word_format)
                



        @hdl.instance
        def stimulus():
            "input for test bench taken from text file test.txt"
            for k in self.sigin:
                xt.data.next = int(k)
                #print(k)
                xt.valid = bool(1)

                yt.record = True
                yt.valid = True 
                yield clock.posedge 
                #Collect a sample from each filter
                yt.record = False
                yt.valid = False

            print(yt.sample_buffer)
            self.response = yt.sample_buffer
            # pl.plot(yt.sample_buffer)
            # pl.show()   
            
            raise StopSimulation()
    
        return hdl.instances()        
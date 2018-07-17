import myhdl as hdl
import numpy as np
from .filter_hw import FilterHardware
from ..fir import fir_df1
from filter_blocks.support import Clock, Reset, Global, Samples
from myhdl import Signal, intbv, StopSimulation


class FilterFIR(FilterHardware):
    """Contains FIR filter parameters. Parent Class : FilterHardware
        Args:
            b (list of int): list of numerator coefficients.
            a (list of int): list of denominator coefficients. 
            word format (tuple of int): (W, WI, WF)
            filter_type:
            filter_form_type:
            response(list): list of filter output in int format.
        """
    def __init__(self, b = None, a = None, w = (24,0,23)):
        super(FilterFIR, self).__init__(b, a, w)
        self.filter_type = 'direct_form'
        self.direct_form_type = 1
        self.response = []

    def get_response(self):
        """Return filter output.

        returns:
            response(numpy int array) : returns filter output as numpy array
        """
        return self.response

    def run_sim(self):
        """Run filter simulation"""

        testfil = self.filter_block()
        testfil.run_sim()


    def convert(self, **kwargs):
        """Convert the HDL description to Verilog and VHDL.
        """
        w = self.input_word_format
        imax = 2**(w[0]-1)

        # small top-level wrapper
        def filter_fir_top(hdl , clock, reset, x, xdv, y, ydv):
            sigin = Samples(x.min, x.max)
            sigin.data, sigin.data_valid = x, xdv
            sigout = Samples(y.min, y.max)
            sigout.data, sigout.data_valid = y, ydv
            clk = clock
            rst = reset
            glbl = Global(clk, rst)
            
            #choose appropriate filter
            fir_hdl = fir_df1.filter_fir

            fir = fir_hdl(glbl, sigin, sigout, self.b, self.coef_word_format,
                          shared_multiplier=self._shared_multiplier)
            
            fir.convert(**kwargs)


        clock = Clock(0, frequency=50e6)
        reset = Reset(1, active=0, async=True)
        x = Signal(intbv(0, min=-imax, max=imax))
        y = Signal(intbv(0, min=-imax, max=imax))
        xdv, ydv = Signal(bool(0)), Signal(bool(0))
        

        if self.hdl_target.lower() == 'verilog':
            filter_fir_top(hdl, clock, reset, x, xdv, y, ydv)
 
        elif self.hdl_target.lower() == 'vhdl':
            filter_fir_top(hdl, clock, reset, x, xdv, y, ydv)
        else:
            raise ValueError('incorrect target HDL {}'.format(self.hdl_target))



    @hdl.block
    def filter_block(self):
        """ this elaboration code will select the different structure and implementations"""

        w = self.input_word_format
        #print(self.input_word_format)
        #print(self.coef_word_format)
        ymax = 2**(w[0]-1)
        vmax = 2**(2*w[0])
        xt = Samples(-ymax, ymax, self.input_word_format)
        yt = Samples(-vmax, vmax)
        xt.valid = bool(1)
        clock = Clock(0, frequency=50e6)
        reset = Reset(1, active=0, async=True)
        glbl = Global(clock, reset)
        tbclk = clock.process()
        numsample = 0
        
        # set numsample 
        numsample = len(self.sigin)
        #process to record output in buffer
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
                filter_insts = dfilter(glbl, xt, yt, self.b, self.coef_word_format)




        @hdl.instance
        def stimulus():
            "record output in numpy array yt.sample_buffer"
            for k in self.sigin:
                xt.data.next = int(k)
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
         
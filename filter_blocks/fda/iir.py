import myhdl as hdl
import numpy as np
from .filter_hw import FilterHardware
from ..iir import iir_df1
from filter_blocks.support import Clock, Reset, Global, Samples
from myhdl import Signal, intbv, StopSimulation


class FilterIIR(FilterHardware):
    """Contains IIR filter parameters. Parent Class : FilterHardware
        Args:
            b (list of int): list of numerator coefficients.
            a (list of int): list of denominator coefficients. 
            word format (tuple of int): (W, WI, WF)
            filter_type:
            filter_form_type:
            response(list): list of filter output in int format.
        """
    def __init__(self, b = None, a = None):
        super(FilterIIR, self).__init__(b, a)
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

    @hdl.block
    def filter_block(self):
        """ this elaboration code will select the different structure and implementations"""

        w = self.input_word_format
        w_out = self.output_word_format
        
        ymax = 2**(w[0]-1)
        vmax = 2**(2*w[0])
        omax = 2**(w_out[0]-1)
        xt = Samples(min=-ymax, max=ymax, word_format=self.input_word_format)
        yt = Samples(min=-omax, max=omax, word_format=self.output_word_format)
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
                dfilter = iir_df1.filter_iir

            if self.n_cascades > 0:
                filter_insts = [None for _ in range(self.n_cascades)]
                for ii in range(self.n_cascades):
                    pass
 #                   filter_insts[ii] = fir_df1.filter_fir(
 #                       glbl, sigin[ii], sigout[ii], b
 #                   )
            else:
                filter_insts = dfilter(glbl, xt, yt, self.b, self.a, self.coef_word_format)




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
         
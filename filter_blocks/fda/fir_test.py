import myhdl as hdl
from myhdl import Signal, always_seq
from filter_blocks.support import Samples
from .filter_hw import FilterHardware
from ..fir import fir_df1

class FIRFilter(FilterHardware):
    def __init__(self,b,a):
        super().__init__(b, a)
        self.filter_type = 'direct_form'
        self.n_cascades = 0
        self.direct_form_type=1

    def set_cascade(self, n_cascades):
        self.n_cascades = n_cascades

    @hdl.block
    def filter_block(self, glbl, sigin, sigout,b,w):
        # this elaboration code will select the different structure and implementations
        xt= Samples(sigin.min, sigin.max)
        yt= Samples(sigout.min, sigout.max)
        xt.data=sigin.val
        xt.valid=bool(1)
        if self.filter_type == 'direct_form':
            if self.direct_form_type == 1:
                # all filters will need the same interface ports, this should be do able
                dfilter = fir_df1.filter_fir

            if self.n_cascades > 0:
                filter_insts = [None for _ in range(self.n_cascades)]
                # for ii in range(self.n_cascades):
                #     filter_insts[ii] = fir_df1.filter_fir(
                #         glbl, sigin[ii], sigout[ii],b
                #     )
            else:
                filter_inst = fir_df1.filter_fir(glbl, xt, yt,b)
            # return filter_inst

                @hdl.always(glbl.clock.posedge)
                def seq():
                   pass

                return seq,filter_inst
import myhdl as hdl
from filter_blocks.support import Samples
from .filter_hw import FilterHardware
from ..iir import iir_parallel
from ..iir import iir_df1

class IIRFilter(FilterHardware):
    def __init__(self, b, a):
        super().__init__(b, a)
        self.filter_type = 'parallel_form'
        self.n_cascades = 0
        self.direct_form_type = 1

    def set_cascade(self, n_cascades):
        self.n_cascades = n_cascades
    
    def set_filter_type(self, filter_type):
        self.filter_type = filter_type

    @hdl.block
    def filter_block(self, glbl, sigin, sigout, b, a, w):
        # this elaboration code will select the different structure and implementations
        xt = Samples(sigin.min, sigin.max)
        yt = Samples(sigout.min, sigout.max)
        xt.data = sigin.val
        xt.valid = bool(1)
        if self.filter_type == 'parallel_form':
           # if self.direct_form_type == 1:
                # all filters will need the same interface ports, this should be do able
            dfilter = iir_parallel.filter_iir_parallel

            if self.n_cascades > 0:
                filter_insts = [None for _ in range(self.n_cascades)]
                for ii in range(self.n_cascades):
                    filter_insts[ii] = iir_parallel.filter_iir_parallel(
                        glbl, sigin[ii], sigout[ii], b, a, w
                    )
            else:
                filter_insts = iir_parallel.filter_iir_parallel(glbl, xt, yt, b, a, w)

        if self.filter_type == 'direct_form':
            filter_insts = iir_df1.filter_iir(glbl, xt, yt, b, a)


        return filter_insts

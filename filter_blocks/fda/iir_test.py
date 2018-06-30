import myhdl as hdl
from filter_blocks.support import Samples
from .filter_hw import FilterHardware
from ..iir import iir_parallel


class FIRFilter(FilterHardware):
    def __init__(self, b, a):
        """
        TODO: DESCRIPTION
        Args:
          b:
          a:
        """
        super().__init__(b, a)
        self.filter_type = 'parallel_form'
        self.n_cascades = 0
        self.direct_form_type = 1

    def set_cascade(self, n_cascades):
        self.n_cascades = n_cascades

    @hdl.block
    def filter_block(self, glbl, sigin, sigout, b, a, w):
        """
        TODO: DESCRIPTION

        TODO: Arguments
        Args:
            glbl:
            sigin:
            sigout:
            b:
            a:
            w:

        Returns:

        """
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
                        glbl, sigin[ii], sigout[ii], b, a
                    )
            else:
                filter_insts = dfilter(glbl, xt, yt, b, a)

            return filter_insts

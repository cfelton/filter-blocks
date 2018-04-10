
import myhdl as hdl
from myhdl import Signal, always_seq

from filter_blocks.support import Samples
from .filter_hw import FilterHardware


class FilterFIR(FilterHardware):
    def __init__(self, b, a):
        super(FilterFIR, self).__init__(b, a)

    @hdl.block
    def process(self, glbl, smpi, smpo):
        """FIR filter model.

        Args:
            glbl:
            smpi: sample stream input
            smpo: sample stream output

        Not convertible
        """
        assert isinstance(smpi, Samples)
        assert isinstance(smpo, Samples)

        clock, reset = glbl.clock, glbl.reset
        x, y = smpi, smpo
        ntaps = len(self.b)
        h = tuple(self.b)

        xd = [0 for _ in range(len(h))]

        @hdl.instance
        def beh_proc():
            while True:
                yield clock.posedge

                if x.valid:
                    xd.insert(0, int(smpi.data))
                    xd.pop(-1)

                    sop = 0
                    for ii in range(ntaps):
                        sop = sop + (h[ii] * xd[ii])

                    y.data.next = sop
                    y.valid.next = True
                else:
                    y.valid.next = False

        return hdl.instances()


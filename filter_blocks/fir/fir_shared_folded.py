
from math import log, ceil

import myhdl as hdl
from myhdl import Signal, intbv, always_seq

from filter_blocks.support import Samples


@hdl.block
def filter_fir_shared_folded(clock, reset, x, y, b):
    """Foldered FIR filter with shared multiplier.

    Args:
        clock, reset: sync circuit globals.
        x (Samples): input sample stream.
        y (Samples): output sample stream.
        b (tuple, list,): filter coefficients.
    """
    assert isinstance(x, Samples)
    assert isinstance(y, Samples)

    ntaps = len(b)
    scnt = Signal(intbv(ntaps+1, min=0, max=ntaps+2))
    pmax = x.data.max * x.data.max
    sop = Signal(intbv(0, min=-pmax, max=pmax))
    scale = int(len(x.data)-1)

    xd = [Signal(intbv(0, min=x.data.min, max=x.data.max))
          for _ in range(len(b))]

    @always_seq(clock.posedge, reset=reset)
    def beh_sop():
        y.valid.next = False
        if scnt == ntaps+1 and x.valid:
            # tap update loop
            xd[0].next = x.data
            for ii in range(1, len(b)-1):
                xd[ii].next = xd[ii-1]
            # compute the first product 
            c = b[0]
            sop.next = c * x.sig
            scnt.next = 1
        elif scnt == ntaps:
            assert not x.valid
            y.data.next = sop >> scale
            y.valid.next = True
            scnt.next = scnt + 1
        elif scnt < ntaps:
            assert not x.vld
            c = b[scnt]
            sop.next = sop + c * xd[scnt]
            scnt.next = scnt + 1

    return beh_sop


import math
import myhdl as hdl
from myhdl import Signal, intbv, always_seq

from filter_blocks.support import Samples, Signals
import math


@hdl.block
def filter_iir(glbl, sigin, sigout, b, a, coef_w, shared_multiplier=False):
    """Basic FIR direct-form I filter.
    Ports:
        glbl (Global): global signals.
        sigin (SignalBus): input digital signal.
        sigout (SignalBus): output digitla signal.
    Args:
        b (tuple): numerator coefficents.
        b (tuple): numerator coefficents.
    Returns:
        inst (myhdl.Block, list):
    """
    assert isinstance(sigin, Samples)
    assert isinstance(sigout, Samples)
    assert isinstance(b, tuple)
    assert isinstance(a, tuple)

    # All the coefficients need to be an `int`

    rb = [isinstance(bb, int) for bb in b]
    ra = [isinstance(aa, int) for aa in a]
    assert all(rb)
    assert all(ra)

    w = sigin.word_format
    w_out = sigout.word_format

    ymax = 2 ** (w[0] - 1)
    vmax = 2 ** (2 * w[0])  # top bit is guard bit
    # max without guard bit. Value at which output will saturate
    amax = 2 ** (2 * w[0] - 1)

    q, qd = w[0], 2 * w[0]  # guard bit not fed back

    # guard bit not passed to output
    o, od = 2 * w[0] - w_out[0], 2 * w[0]
    o = 0 if o < 0 else o

    N = len(b) - 1
    clock, reset = glbl.clock, glbl.reset
    xdv = sigin.valid
    y, ydv = sigout.data, sigout.valid
    x, xdv = sigin.data, sigin.valid

    # Delay elements, list-of-signals
    ffd = Signals(intbv(0, min=-ymax, max=ymax), N)
    fbd = Signals(intbv(0, min=-ymax, max=ymax), N)
    yacc = Signal(intbv(0, min=-vmax, max=vmax))  # verify the length of this

    dvd = Signal(bool(0))
    #print(len(yacc))

    # print(len(yacc))

    @hdl.always(clock.posedge)
    def beh_direct_form_one():
        if sigin.valid:
            # print(x)

            for i in range(N - 1):
                ffd[i + 1].next = ffd[i]
                fbd[i + 1].next = fbd[i]

            ffd[0].next = x
            fbd[0].next = yacc[qd:q].signed()

    @hdl.always_comb
    def beh_acc():
        c = b[0]
        sop = x * c

        for ii in range(N):
            c = b[ii + 1]  # first element in list in b0
            d = a[ii + 1]  # first element in list is a0 =1
            sop = sop + (c * ffd[ii]) - (d * fbd[ii])

        yacc.next = sop

    @always_seq(clock.posedge, reset=reset)
    def beh_output():
        dvd.next = xdv
        # y.next = yacc[od:o].signed()

        if (yacc[qd] == 1 and yacc[qd - 1] == 1) or (yacc[qd] == 0 and yacc[qd - 1] == 0):
            ydv.next = dvd
            y.next = yacc[od:o].signed()

        elif yacc[qd + 1] == 1 and yacc[qd] == 0:
            y.next = -amax
            ydv.next = dvd

        elif yacc[qd] == 0 and yacc[qd - 1] == 1:
            y.next = amax - 1
            ydv.next = dvd

    return hdl.instances()

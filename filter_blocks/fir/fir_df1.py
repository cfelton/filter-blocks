import myhdl as hdl
from myhdl import Signal, intbv, always_seq

from filter_blocks.support import Samples, Signals
import math

@hdl.block
def filter_fir(glbl, sigin, sigout, b, coef_w, shared_multiplier=False):
    """Basic FIR direct-form I filter.

    Ports:
        glbl (Global): global signals.
        sigin (Samples): input digital signal.
        sigout (Samples): output digitla signal.

    Args:
        b (tuple): numerator coefficents.

    Returns:
        inst (myhdl.Block, list):
    """
    assert isinstance(sigin, Samples)
    assert isinstance(sigout, Samples)
    assert isinstance(b, tuple)
    #All the coefficients need to be an `int`
    rb = [isinstance(bb, int) for bb in b]
    assert all(rb)

    w = sigin.word_format
    ymax = 2**(w[0]-1)
    #vmax = 2**(2*w[0])  # double width max and min

    N = len(b)-1


    acc_bits = w[0] + coef_w[0] + int(math.log(N, 2))
    amax = 2**(acc_bits)
    print(acc_bits)


    clock, reset = glbl.clock, glbl.reset
    xdv = sigin.valid
    y, ydv = sigout.data, sigout.valid
    x = Signal(intbv(0, min = - ymax, max = ymax))
    # Delay elements, list-of-signals
    ffd = Signals(intbv(0, min = -ymax, max = ymax), N)
    yacc = Signal(intbv(0, min = - amax, max = amax)) #verify the length of this
    dvd = Signal(bool(0))

    @hdl.always(clock.posedge)
    def beh_direct_form_one():
        if sigin.valid:
            x.next = sigin.data

            for i in range(N-1):
                ffd[i+1].next = ffd[i]

            ffd[0].next = x
            # sum-of-products loop
            c = b[0]
            sop = x*c

            for ii in range(N):
                c = b[ii+1]
                sop = sop + (c * ffd[ii])
            yacc.next = sop
            #print(yacc)

    @always_seq(clock.posedge, reset=reset)
    def beh_output():
        dvd.next = xdv
        y.next = yacc.signed()
        ydv.next = dvd

    return beh_direct_form_one, beh_output

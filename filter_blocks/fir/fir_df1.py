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
    w_out = sigout.word_format

    #print(sigin.word_format)
    print(sigout.word_format)


    ymax = 2**(w[0]-1)
    #vmax = 2**(2*w[0])  # double width max and min

    N = len(b)-1


    sum_abs_b = (sum([abs(x) for x in b]))/2**coef_w[0]
    #acc_bits = w[0] + coef_w[0] + int(math.log(N, 2))
    #print(w[0] + coef_w[0] + int(math.log(N, 2)))
    print(w[0] + coef_w[0] + int(math.log(sum_abs_b, 2)))
    acc_bits = w[0] + coef_w[0] + int(math.log(sum_abs_b, 2))
    amax = 2**(acc_bits)
    
    #print(acc_bits)

    qd = acc_bits
    q = acc_bits-w_out[0]

    if q<0:
        q=0

    #print(qd-q)
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
        y.next = yacc[qd:q].signed()
        #print(y)
        #y.next = yacc.signed()
        ydv.next = dvd

    return beh_direct_form_one, beh_output

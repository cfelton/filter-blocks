import myhdl as hdl
from myhdl import Signal, intbv, always_seq
from filter_blocks.support import Samples, Signals

@hdl.block
def filter_iir(glbl, sigin, sigout, b, a, shared_multiplier=False):
    """Basic FIR direct-form I filter.

    Ports:
        glbl (Global): global signals.
        sigin (SignalBus): input digital signal.
        sigout (SignalBus): output digitla signal.

    Args:
        b (tuple, list): numerator coefficents.

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
    ymax = 2**(w[0]-1)
    vmax = 2**(2*w[0])  # double width max and min
    vmin = -vmax
    ymin = -ymax
    N = len(b)-1
    clock, reset = glbl.clock, glbl.reset
    xdv = sigin.valid
    y, ydv = sigout.data, sigout.valid
    x = Signal(intbv(0, min=vmin, max=vmax))
    # Delay elements, list-of-signals
    ffd = Signals(intbv(0, min=ymin, max=ymax), N)
    fbd = Signals(intbv(0, min=ymin, max=ymax), N)
    yacc = Signal(intbv(0, min=vmin, max=vmax)) #verify the length of this
    dvd = Signal(bool(0))

    @hdl.always(clock.posedge)
    def beh_direct_form_one():
        if sigin.valid:
            x.next = sigin.data

            for i in range(N-1):
                ffd[i+1].next = ffd[i]
                fbd[i+1].next = fbd[i]

            ffd[0].next = x
            fbd[0].next = yacc.signed()
            # sum-of-products loop
            c = b[0]
            sop = x*c

            for ii in range(N):
                c = b[ii+1] #first element in list in b0
                d = a[ii] #first element in list is a1
                sop = sop + (c * ffd[ii]) - (d * fbd[ii])
            yacc.next = sop
            print(yacc)

    @always_seq(clock.posedge, reset=reset)
    def beh_output():
        dvd.next = xdv
        y.next = yacc.signed()
        ydv.next = dvd

    return beh_direct_form_one, beh_output


from math import ceil, log
import myhdl as hdl
from myhdl import Signal, intbv, always_seq, ConcatSignal
from filter_blocks.support import Global, Samples, Signals


@hdl.block
def filter_iir(glbl, sigin, sigout, b, a, shared_multiplier=False):
    """Parallel IIR filter.

    Ports:
        glbl (Global): global signals.
        sigin (Samples): input digital signal.
        sigout (SignalBus): output digital signal.

    Args:
        b (tuple, list): numerator coefficents.

    Returns:
        inst (myhdl.Block, list):
    """
    assert isinstance(sigin, Samples)
    assert isinstance(sigout, Samples)
    assert isinstance(b, tuple)
    assert isinstance(a, tuple)

    rb = [isinstance(bb, int) for bb in b]
    ra = [isinstance(aa, int) for aa in a]
    assert all(ra)
    assert all(rb)

    w = sigin.word_format
    vmax = 2**(2*w[0])  # double width max and min
    vmin = -vmax
    N = len(b)-1
    # Quantized IIR coefficients
    b0, b1, b2 = b
    a1, a2 = a

    # Locally reference the interface signals
    clock, reset = glbl.clock, glbl.reset
    xdv = sigin.valid
    y = sigout
    x = Signal(intbv(0, min=vmin, max=vmax))

    # Delay elements, list-of-signals (double length for all)
    ffd = Signals(intbv(0, min=vmin, max=vmax), N)
    fbd = Signals(intbv(0, min=vmin, max=vmax), N)
    yacc = Signal(intbv(0, min=vmin, max=vmax))
    dvd = Signal(bool(0))

    @hdl.always(clock.posedge)
    def beh_direct_form_one():
        if sigin.valid:
            x.next = sigin.data
            ffd[1].next = ffd[0]
            ffd[0].next = x

            fbd[1].next = fbd[0]
            fbd[0].next = yacc.signed()
            
    @hdl.always_comb
    def beh_acc():
        # double precision accumulator
        yacc.next = (b0 * x) + (b1 * ffd[0]) + (b2 * ffd[1]) \
                    - (a1 * fbd[0]) - (a2 * fbd[1])

    @hdl.always_seq(clock.posedge, reset=reset)
    def beh_output():
        # Delay slot in the above calculation
        dvd.next = xdv
        y.data.next = yacc.signed()
        y.valid.next = dvd

    return beh_direct_form_one, beh_acc, beh_output


@hdl.block
def filter_iir_parallel(glbl, x, y, b, a):
    """structural model of parallel filters ...
    Args:
        glbl: global interface, clock, reset, etc.
        x:
    """
    assert isinstance(glbl, Global)
    assert isinstance(x, Samples)
    assert isinstance(y, Samples)

    assert len(b) == len(a)
    number_of_sections = len(b)
    list_of_insts = [None for _ in range(number_of_sections)]

    # y_i = Signals(intbv(0)[20:], number_of_sections)
    yi = [Samples(x.imin, x.imax) for _ in range(number_of_sections)]

    for ii in range(len(b)):
        bp = tuple(map(int, b[ii]))  # pass a tuple of ints
        ap = tuple(map(int, a[ii]))  # pass a tuple of ints
        # Create an IIR filter instance for each
        list_of_insts[ii] = filter_iir(glbl, x, yi[ii], b=bp,  a=ap)

    insts = parallel_sum(glbl, yi, y)

    return list_of_insts, insts


@hdl.block
def parallel_sum(glbl, yins, yout):

    """Sum of all the individual parallel outputs.
    Args:
        glbl: global siganls, clock, reset, etc.
        yins: the parallel IIR outputs
        yout: the combined output
    """
    assert isinstance(yins, list)
    assert isinstance(yout, Samples)
    clock, reset = glbl.clock, glbl.reset
    nsums = len(yins)
    scale = len(yins[0].data) + ceil(log(nsums, 2)) - len(yout.data)
    ydata = [yy.data for yy in yins]

    @hdl.always_seq(clock.posedge, reset=reset)
    def output():
        psum = 0
        for ii in range(nsums):
            psum = psum + ydata[ii]
        yout.data.next = psum >> scale
        # TODO: this is incorrect, the input valids were lost!
        yout.valid.next = True

    return output

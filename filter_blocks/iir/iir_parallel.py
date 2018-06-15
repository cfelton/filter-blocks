import myhdl as hdl
from myhdl import Signal, intbv, always_seq, ConcatSignal
from filter_blocks.support import Samples, Signals


@hdl.block
def filter_iir(glbl, sigin, sigout, b, a, shared_multiplier=False):
    """Parallel IIR filter.

    Ports:
        glbl (Global): global signals.
        sigin (Samples): input digital signal.
        sigout (SignalBus): output digitla signal.

    Args:
        b (tuple, list): numerator coefficents.

    Returns:
        inst (myhdl.Block, list):
    """
    assert isinstance(sigin, Samples)
    #assert isinstance(sigout, Samples)
    assert isinstance(b, tuple)
    assert isinstance(a, tuple)

    rb = [isinstance(bb, int) for bb in b]
    ra = [isinstance(aa, int) for aa in a]
    assert all(ra)
    assert all(rb)

    w = sigin.word_format
    ymax = 2**(w[0]-1)
    vmax = 2**(2*w[0])  # double width max and min
    vmin = -vmax
    N = len(b)-1
    # Quantized IIR coefficients
    b0, b1, b2 = b
    a1, a2 = a
    q, qd = w[0]-1, 2*w[0]

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

    print(glbl.clock)


    @hdl.always(clock.posedge)
    def beh_direct_form_one():
        if sigin.valid:
            x.next=sigin.data       
            ffd[1].next = ffd[0]
            ffd[0].next = x

            fbd[1].next = fbd[0]
            fbd[0].next = yacc.signed()
            print(fbd[0])
            
    @hdl.always_comb
    def beh_acc():
         #double precision accumulator 
        yacc.next = (b0 * x) + (b1 * ffd[0]) + (b2 * ffd[1]) \
                    - (a1 * fbd[0]) - (a2 * fbd[1])
       
       
    @hdl.always_seq(clock.posedge, reset=reset)
    def beh_output():
        dvd.next = xdv
        y.next = yacc.signed()

    return beh_direct_form_one, beh_acc, beh_output



@hdl.block
def parallel_sum(glbl, b, yin, yout):

    """sum of all the individial parallel outputs ...
    """
    clock, reset = glbl.clock, glbl.reset
    k= Signal(intbv(0)[8:])
    yout = Samples(k.min, k.max)
    
    @hdl.always_seq(clock.posedge, reset=reset)
    def output():
        yout.data = 0
        for ii in range(len(b)):
            yout.data=yout.data+yin[(ii+1)*20:ii*20]

        print(yout.data)

    return output

@hdl.block
def filter_iir_parallel(glbl, x, y, b, a, w):
    """structural model of parallel filters ...
    """
    assert len(b) == len(a)
    number_of_sections = len(b)
    list_of_insts = [None for _ in range(number_of_sections)]

    #y_i = Signal[(intbv(0)[20:])for _ in range(number_of_sections)]
    y_i = Signals(intbv(0)[20:], number_of_sections)
    yvector = ConcatSignal(*reversed(y_i))

    for ii in range(len(b)):    
        list_of_insts[ii] = filter_iir(
            glbl, x, y_i[ii],
            b=tuple(map(int, b[ii])),  a=tuple(map(int, a[ii])))

    insts = parallel_sum(glbl, b, yvector, y)

    return list_of_insts, insts

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
    
    ymax = 2**(w[0]-1)
    vmax = 2**(2*w[0])  # top bit is guard bit
    amax = 2**(2*w[0]-1) #max without guard bit. Value at which output will saturate  
    #print(2**(2*w[0]-1))

    q, qd = w[0], 2*w[0]   #guard bit not fed back

    o, od = 2*w[0]-w_out[0], 2*w[0]      # guard bit not passed to output

    #print("od-o",od-o)

    if o<0:
        o=0


    N = len(b)-1
    clock, reset = glbl.clock, glbl.reset
    xdv = sigin.valid
    y, ydv = sigout.data, sigout.valid
    x = Signal(intbv(0, min=-ymax, max=ymax))

    # Delay elements, list-of-signals
    ffd = Signals(intbv(0, min=-ymax, max=ymax), N)
    fbd = Signals(intbv(0, min=-ymax, max=ymax), N)
    yacc = Signal(intbv(0, min=-vmax, max=vmax)) #verify the length of this
    dvd = Signal(bool(0))
    overflow = Signal(bool(0))
    underflow = Signal(bool(0))
    #print(len(yacc))

    @hdl.always(clock.posedge)
    def beh_direct_form_one():
        if sigin.valid:
            x.next = sigin.data

            for i in range(N-1):
                ffd[i+1].next = ffd[i]
                fbd[i+1].next = fbd[i]

            ffd[0].next = x
            fbd[0].next = yacc[qd:q].signed()
            # sum-of-products loop
            c = b[0]
            sop = x*c

            for ii in range(N):
                c = b[ii+1] #first element in list in b0
                d = a[ii+1] #first element in list is a1
                sop = sop + (c * ffd[ii]) - (d * fbd[ii])
            #yacc.next = sop    # from the earlier implementation without saturation
            if (yacc[qd]==1 and yacc[qd-1]==1) or (yacc[qd]==0 and yacc[qd-1]==0):
                yacc.next = sop

            elif yacc[qd+1]==1 and yacc[qd]==0:
                #print('underflow') # and change y as well
                yacc.next == -amax

            elif yacc[qd]==0 and yacc[qd-1]==1:
                #print('overflow')
                yacc.next == amax-1

        print("yacc" , yacc)


    @hdl.always_comb
    def beh_acc():

        if (yacc[qd]==1 and yacc[qd-1]==1) or (yacc[qd]==0 and yacc[qd-1]==0):
            #y.next = yacc[od+1:o].signed()
            #ydv.next = dvd
            pass
        elif yacc[qd+1]==1 and yacc[qd]==0:
            #print('underflow2') # and change y as well
            underflow.next = bool(1)

        elif yacc[qd]==0 and yacc[qd-1]==1:
            #print('overflow2')
            overflow.next = bool(1)

        #print("yacc" , yacc)

    @always_seq(clock.posedge, reset=reset)
    def beh_output():
        dvd.next = xdv
        if overflow == 1 :
            y.next = amax-1
            ydv.next = dvd
            overflow.next == bool(0)
        elif underflow == 1:
            y.next = -amax
            ydv.next = dvd
            underflow.next == bool(0)
        else:
            y.next = yacc[od:o].signed()
            y.next = yacc.signed()
            ydv.next = dvd

        #print("y" , y)

    return hdl.instances()

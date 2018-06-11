import myhdl as hdl
from myhdl import Signal, intbv, always_seq
from filter_blocks.support import Samples, Signals


@hdl.block
def filter_fir(glbl, sigin,sigout, b, shared_multiplier=False):
    """Basic IIR direct-form I filter.

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
    #assert isinstance(sigout, Samples)
    assert isinstance(b, tuple)

    # All the coefficients need to be an `int`, the
    # class (`???`) handles all the float to fixed-poit
    # conversions.
    rb = [isinstance(bb, int) for bb in b]
    assert all(rb)

    w = sigin.word_format
    ymax = 2**(w[0]-1)
    vmax = 2**(2*w[0])  # double width max and min
    vmin = -vmax

    # Quantized IIR coefficients
    b0, b1, b2 = b

    # Locally reference the interface signals
    clock, reset = glbl.clock, glbl.reset
    xdv = sigin.valid
    y, ydv = sigout.data, sigout.valid 
    x = Signal(intbv(0, min=vmin, max=vmax))  
             #note changes made even makin x a signal does not work
    
    # Delay elements, list-of-signals (double length for all)
    ffd = [Signal(intbv(0, min=vmin, max=vmax)) for _ in range(2)]
    yacc = Signal(intbv(0, min=vmin, max=vmax))
    dvd = Signal(bool(0))

    @hdl.always(clock.posedge)
    def beh_direct_form_one():
        #if sigin.valid:
        x.next=sigin.data
        #print("hello from inside")
        #print(sigin.data)
        
        ffd[1].next = ffd[0]
        ffd[0].next = x

        # x.next = sigin.data
        # for i in range(N-1):
        #     ffd[i+1].next = ffd[i]

        # ffd[0].next = x
        #     # sum-of-products loop
        # c = b[0]
        # sop = x*c

        # for ii in range(N):
        #     c = b[ii+1]
        #     sop = sop + (c * ffd[ii])
        # yacc.next = sop
        # print(yacc)


        #multiplication doesnt work if b0*x
        #f= open("filterFIRoutput.txt","a+")
        #f.write(str(yacc.val))
        #f.write("\r\n")
        #f.close()
        #print (yacc.val)
            


    @hdl.always_comb
    def beh_acc():
         #double precision accumulator 
         yacc.next = (b0 * x) + (b1 * ffd[0]) + (b2 * ffd[1]) 

       
       
    @hdl.always_seq(clock.posedge, reset=reset)
    def beh_output():
        dvd.next = xdv
        y.next = yacc.signed()
        ydv.next = dvd
        #print(y)

    # @todo add shared multiplier version ...

    return beh_direct_form_one,beh_acc,beh_output

@hdl.block
def summer(glbl, b, y_i ):

    """IIR sum of sections ...
    """
    yfinal=y_i.data
    clock, reset = glbl.clock, glbl.reset
    @hdl.always(clock.posedge)
    def pls():
        yfinal=y_i.data
        for ii in range(len(b)):
            yfinal=yfinal+y_i.data[ii]
            print(y_i.data)

        #print(y_i.data)

    return pls


@hdl.block
def filter_fir_sos(glbl, x, y, b, w):
    """IIR sum of sections ...
    """
    number_of_sections = len(b)
    list_of_insts = [None for _ in range(number_of_sections)]
    list_of_insts2 = [None for _ in range(number_of_sections)]
    y= Signal(intbv(0)[20:])


    k= Signal(intbv(0)[8:])
    y_i = [Samples(k.min, k.max) for _ in range(number_of_sections+1)]
   
    xb = [Samples(k.min, k.max) for _ in range(number_of_sections+1)]  #added +1 otherwise out of bounds
    xb[0] = x  #check why this is happening
    #xb[number_of_sections-1] = y


    for ii in range(len(b)):    #cehck if it should be +1 or nor
        list_of_insts[ii] = filter_fir(
            glbl, x, y_i[ii],
            b=tuple(map(int, b[ii])))

    for ii in range(len(b)):    #cehck if it should be +1 or nor
        list_of_insts2 = summer(glbl, b, y_i[ii] )

    return list_of_insts, list_of_insts2

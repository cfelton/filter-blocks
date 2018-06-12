import myhdl as hdl
from myhdl import Signal, intbv, StopSimulation, delay, traceSignals, ResetSignal
from filter_blocks.support import Clock, Reset, Global, Samples
from filter_blocks.iir.iir_parallel import filter_iir_parallel


@hdl.block
def test_iir_parallel():
    
    # clock = Clock(0, frequency=50e6)
    # reset = Reset(0, active=0, async=True)
    # glbl = Global(clock, reset)
    # tbclk = clock.process()
    glbl = Global()
    glbl.clock = Signal(bool(1))
    glbl.reset = ResetSignal(bool(1),bool(0),True)

    x= Signal(intbv(0)[8:])
    y= Signal(intbv(0)[20:])

    b=[[1, 0, 1] ,[0, 0, 1]]
    a=[[1, 0],[1, 0]]
    w=(24,0)

    xt= Samples(x.min, x.max)
    yt= Samples(y.min, y.max)

    
    inst=filter_iir_parallel(glbl, xt, y, b, a, w) 
    
    @hdl.always(delay(10))
    def clkgen():
        glbl.clock.next = not glbl.clock

    @hdl.instance
    def stimulus():
        "input for test bench taken from text file test.txt"
        for line in open('test.txt'):
            x.next=int(line)
            xt.data=x.next
            xt.valid=bool(1) 
            yield delay(20)
        raise StopSimulation

    return inst, stimulus, clkgen

def main():
    # tb = test_iir_parallel()
    # tb.run_sim()

   tb = traceSignals(test_iir_parallel())
   tb.run_sim()



if __name__ == '__main__':
    main()


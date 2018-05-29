import myhdl as hdl
from myhdl import Signal, intbv, delay, traceSignals, StopSimulation
from filter_blocks.support import Clock, Reset, Global, Samples,ResetSignal
from filter_blocks.fir import fir_df1 

@hdl.block
def testBenchFIR():
    
    glbl=Global
    glbl.clock=Signal(bool(1))
    glbl.reset=ResetSignal(bool(1),bool(0),True)
    x= Signal(intbv(1)[8:])
    y= Signal(intbv(0)[8:])
   
    xt= Samples(x.min, x.max)
    yt= Samples(y.min, y.max)
    b=(1,2,1)
    w=(24,23)

    fir=fir_df1.filter_fir(glbl, xt, yt, b,w)
    
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
        
    return fir, clkgen, stimulus

def main():
   tb = traceSignals(testBenchFIR())
   tb.run_sim()


if __name__ == '__main__':
    main()


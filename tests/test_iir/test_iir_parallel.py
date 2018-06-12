import myhdl as hdl
from myhdl import Signal, intbv, StopSimulation, delay, ResetSignal, traceSignals
from filter_blocks.support import Clock, Reset, Global, Samples
from filter_blocks.iir.iir_parallel import filter_fir_sos


@hdl.block
def testBenchFIR():
    
    glbl=Global
    glbl.clock=Signal(bool(1))
    glbl.reset=ResetSignal(bool(1),bool(0),True)
    x= Signal(intbv(0)[8:])
    y= Signal(intbv(0)[20:])
     #if using sos
    b=[[1, 0, 1] ,[0, 0, 1]]
    a=[[1, 0],[1, 0]]
 
    w=(24,0)
    
    xt= Samples(x.min, x.max)
    yt= Samples(y.min, y.max)
    
    #b=(1,2,1)
    w=(24,23)
    

    mov=filter_fir_sos(glbl, xt, y, b, a, w) # use when calling sos
    #mov=filter_fir(glbl, xt, yt, b,w) # use when sirectly calling iir
    
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
        
    return mov, clkgen, stimulus

def main():
#    tb = testBenchFIR()
#    tb.run_sim()

   tb = traceSignals(testBenchFIR())
   tb.run_sim()



if __name__ == '__main__':
    main()


import myhdl as hdl
from myhdl import Signal, intbv, StopSimulation, delay
from filter_blocks.support import Clock, Reset, Global, Samples
from filter_blocks.fir.iir_parallel import filter_fir_sos
from filter_blocks.fda import fir_test as ft


@hdl.block
def testBenchFIR():
    
    clock = Clock(0, frequency=50e6)
    reset = Reset(0, active=0, async=True)
    glbl = Global(clock, reset)
    x= Signal(intbv(0)[8:])
    y= Signal(intbv(0)[20:])
     #if using sos
    b=[[1,0,1] ,[0,0,1]]
 
    w=(24,0)
    
    xt= Samples(x.min, x.max)
    yt= Samples(y.min, y.max)
    
    #b=(1,2,1)
    w=(24,23)
    

    mov=filter_fir_sos(glbl, xt, yt, b,w) # use when calling sos
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
   tb = testBenchFIR()
   tb.run_sim()



if __name__ == '__main__':
    main()


import myhdl as hdl
from myhdl import Signal, intbv, StopSimulation
from filter_blocks.support import Clock, Reset, Global, Samples
from filter_blocks.fir import fir_df1
from filter_blocks.fda import fir_test as ft
import matplotlib.pyplot as pl

@hdl.block
def test_fir_df1():
    clock = Clock(0, frequency=50e6)
    reset = Reset(1, active=0, async=True)
    glbl = Global(clock, reset)
    tbclk = clock.process()
    #x = Signal(intbv(0)[8:])
    y = Signal(intbv(0)[8:])
    xt = Samples(y.min, y.max)
    yt = Samples(y.min, y.max)
    a = (1)
    b = (1, 2, 1)
    w = (24, 23, 0)
    numsample = 0

    #note: the filter interface has been bypassed for the purpose 
    #of plotting the output. Will have to include this in future
    
    #fir_test = ft.FIRFilter(b, a)
    #fir = fir_test.filter_block(glbl, x, y, b, w)


    fir = fir_df1.filter_fir(glbl, xt, yt, b, w)
    

    for line in open('test.txt'):
        numsample += 1 

    rec_insts = yt.process_record(clock, num_samples=numsample)

    @hdl.instance
    def stimulus():
        "input for test bench taken from text file test.txt"
        for line in open('test.txt'):
            xt.data.next = int(line)
            xt.valid = bool(1)

            yt.record = True
            yt.valid = True 
            yield clock.posedge 
            #Collect a sample from each filter
            yt.record = False
            yt.valid = False

        print(yt.sample_buffer)
        pl.plot(yt.sample_buffer)
        pl.show()   
            
        raise StopSimulation()
    
    return hdl.instances()

def main():
    test_bench = test_fir_df1()
    test_bench.run_sim()


if __name__ == '__main__':
    main()

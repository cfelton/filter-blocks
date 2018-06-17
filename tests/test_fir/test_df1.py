import myhdl as hdl
from myhdl import Signal, intbv, delay, StopSimulation
from filter_blocks.support import Clock, Reset, Global, ResetSignal
from filter_blocks.fir import fir_df1
from filter_blocks.fda import fir_test as ft

@hdl.block
def test_fir_df1():
    clock = Clock(0, frequency=50e6)
    reset = Reset(0, active=0, async=True)
    glbl = Global(clock, reset)
    tbclk = clock.process()
    # glbl.clock = Signal(bool(1))
    # glbl.reset = ResetSignal(bool(1), bool(0), True)
    x = Signal(intbv(0)[8:])
    y = Signal(intbv(0)[8:])
    # xt= Samples(x.min, x.max)
    # yt= Samples(y.min, y.max)
    a_coef = (1)
    b = (1, 2, 1)
    w = (24, 23, 0)
    hello = ft.FIRFilter(b, a_coef)
    fir = hello.filter_block(glbl, x, y, b, w)


    @hdl.instance
    def stimulus():
        "input for test bench taken from text file test.txt"
        for line in open('test.txt'):
            x.next = int(line)
            # xt.valid=bool(1)
            #print(x)
            yield clock.posedge
        raise StopSimulation
    return fir, stimulus

def main():
    testBench = test_fir_df1()
    testBench.run_sim()


if __name__ == '__main__':
    main()

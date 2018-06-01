import myhdl as hdl
from myhdl import Signal, intbv, delay, StopSimulation
from filter_blocks.support import Clock, Reset, Global, ResetSignal
from filter_blocks.fir import fir_df1
from filter_blocks.fda import fir_test as ft

@hdl.block
def testBenchFIR():
    glbl = Global
    glbl.clock = Signal(bool(1))
    glbl.reset = ResetSignal(bool(1), bool(0), True)
    x = Signal(intbv(0)[8:])
    y = Signal(intbv(0)[8:])
    # xt= Samples(x.min, x.max)
    # yt= Samples(y.min, y.max)
    a_coef = (1)
    B = (1, 2, 1)
    w = (24, 23, 0)
    hello = ft.FIRFilter(B, a_coef)
    fir = hello.filter_block(glbl, x, y, B, w)

    @hdl.always(delay(10))
    def clkgen():
        "just testing"
        glbl.clock.next = not glbl.clock

    @hdl.instance
    def stimulus():
        "input for test bench taken from text file test.txt"
        for line in open('test.txt'):
            x.next = int(line)
            # xt.valid=bool(1)
            #print(x)
            yield delay(20)
        raise StopSimulation
    return fir, clkgen, stimulus

def main():
    testBench = testBenchFIR()
    testBench.run_sim()


if __name__ == '__main__':
    main()

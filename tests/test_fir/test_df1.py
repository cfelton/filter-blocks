import myhdl as hdl
from myhdl import Signal, intbv, StopSimulation
from filter_blocks.support import Clock, Reset, Global
from filter_blocks.fir import fir_df1
from filter_blocks.fda import fir_test as ft

@hdl.block
def test_fir_df1():
    clock = Clock(0, frequency=50e6)
    reset = Reset(0, active=0, async=True)
    glbl = Global(clock, reset)
    tbclk = clock.process()
    x = Signal(intbv(0)[8:])
    y = Signal(intbv(0)[8:])
    a = (1)
    b = (1, 2, 1)
    w = (24, 23, 0)
    fir_test = ft.FIRFilter(b, a)
    fir = fir_test.filter_block(glbl, x, y, b, w)

    @hdl.instance
    def stimulus():
        "input for test bench taken from text file test.txt"
        for line in open('test.txt'):
            x.next = int(line)
            yield clock.posedge
        raise StopSimulation

    return fir, stimulus, tbclk

def main():
    test_bench = test_fir_df1()
    test_bench.run_sim()


if __name__ == '__main__':
    main()

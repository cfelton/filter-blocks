
import pytest
import myhdl as hdl
from myhdl import Signal, intbv, StopSimulation, delay, traceSignals, ResetSignal

from filter_blocks.support import Clock, Reset, Global, Samples
from filter_blocks.iir import iir_parallel
from filter_blocks.fda import FilterIIR


# TODO: fix these, they should not be failing!
@pytest.mark.xfail
@hdl.block
def test_iir_api():
    
    clock = Clock(0, frequency=50e6)
    reset = Reset(1, active=0, async=True)
    glbl = Global(clock, reset)
    tbclk = clock.process()

    x = Signal(intbv(0)[8:])
    y = Signal(intbv(0)[20:])

    b = [[1, 0, 1], [0, 0, 1]]
    a = [[0, 1], [0, 0]]
    w = (24, 0)

    iir_test = FilterIIR(b, a)
    iir = iir_test.filter_block(glbl, x, y, b, a, w)

    @hdl.instance
    def stimulus():
        """Input for test bench taken from text file test.txt"""
        for line in open('test.txt'):
            x.next = int(line)
            yield clock.posedge
        raise StopSimulation

    return iir, stimulus, tbclk


@pytest.mark.xfail
def test_iir_par_sim():
    tb = traceSignals(test_iir_api())
    tb.run_sim()

    # tb = test_iir_parallel()
    # tb.run_sim()


if __name__ == '__main__':
    test_iir_par_sim()


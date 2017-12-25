
import numpy as np

import myhdl as hdl
from myhdl import Signal, intbv, delay

from filter_blocks.support import Clock, Reset, Samples
from filter_blocks.testing import DDSine


def test_filters(args=None):
    if args is None:
        ntaps, nbands, fs, imax = 86, 20, 1e5, 2**7
        nsmps = 3*ntaps
    # @todo: get the following from args

    clock = Clock(0, frequency=50e6)
    reset = Reset(0, active=0, async=True)

    # Input to the filters
    xi = Samples(min=-imax, max=imax)
    xf = Samples(min=-1, max=1, dtype=float)

    # Output of the filters
    ylist = [Samples(min=-1, max=1, dtype=float) for _ in range(4)]
    ym, y1, y2, y3 = ylist
    rlist = [xi, xf] + ylist

    dibv = intbv(0, min=-imax, max=imax)
    dds1 = DDSine(1e3, fs, 0.8, 0, dibv)

    # @todo: get coefficients
    # bi, b = get_fir_coef()
    # h = tuple(bi)

    # Frequency sweep
    fsn = fs/2
    flist = np.linspace(0, fsn, nbands)

    @hdl.block
    def bench_fir():
        tbclk = clock.process()
        tbsin = dds1.process(clock, reset, xi, xf)

        # The collection of FIR filter implementations.

        # Create "records" for each sample stream.
        rec_insts = [None for _ in rlist]
        for ii, sc in enumerate(rlist):
            rec_insts[ii] = sc.process_record(clock, num_samples=nsmps)

        @hdl.instance
        def tbstim():
            yield reset.pulse(clock)
            yield clock.posedge

            for ff in flist:
                # Avoid the transitions
                dds1.set_frequency(ff)
                for ii in range(ntaps+7):
                    yield xi.valid.posedge
                dds1.set_zero(False)
                yield clock.posedge

                # Enable recording
                for sr in rlist:
                    sr.record = True

                for sr in rlist:
                    sr.record = False

            yield delay(1100)
            raise hdl.StopSimulation

        return hdl.instances()

    tb = bench_fir()
    tb.config_sim(trace=True)
    tb.run_sim()


if __name__ == '__main__':
    test_filters()




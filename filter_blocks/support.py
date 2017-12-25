
import numpy as np

import myhdl as hdl
from myhdl import Signal, SignalType, ResetSignal, intbv, delay


class Clock(SignalType):
    def __init__(self, val=bool(0), frequency=1):
        self.frequency = frequency
        super(Clock, self).__init__(val)

    @hdl.block
    def process(self, hticks=None):
        if hticks is None:
            nts = 1e-9
            period = 1 / self.frequency
            hticks = self._hticks = int(round((period / nts) / 2))

        @hdl.instance
        def beh_clock():
            self.next = False
            yield delay(hticks)
            self.next = not self.val

        return beh_clock


class Reset(ResetSignal):
    def __init__(self, val=0, active=0, async=True):
        super(Reset, self).__init__(val, active, async)

    def pulse(self, clock=None, pulse_width=77):
        yield delay(10)
        self.next = self.active
        yield delay(pulse_width)
        if clock is not None:
            yield clock.posedge
        self.next = not self.active
        yield delay(10)


def check_word_fomat(w):
    if len(w) == 2:
        fwl = w[0] - w[1] - 1
        assert fwl >= 0
        wf = (w[0], w[1], )
    elif len(w) == 3:
        wf = w
    else:
        raise Exception("Invalid word format")
    return wf


class Samples(object):
    def __init__(self, min, max, res=0, dtype=intbv, sample_rate=1):
        """Sample streams, input and output to filters.

        """
        # @todo: fixed-point support ...
        word_format = (24, 23, 0)
        # The fixed-point word format is described by a tuple, the
        # tuple defines the number of integer bits and fractional bits:
        # (word, int, frac) where: word = int + frac + 1
        self.word_format = check_word_fomat(word_format)
        wl, iwl, fwl = word_format
        # imax = 2**(wl-1)

        # The sample integer range
        self.imax = imax = max
        self.imin = imin = min

        # @todo: use the dtype
        self.data = Signal(intbv(0, min=imin, max=imax))
        self.valid = Signal(bool(0))

        self.sample_rate = sample_rate
        self.clock = None

        self.record = False
        self.sample_buffer = []
        self.sample_count = 0

    @hdl.block
    def process_record(self, clock, num_samples=10):
        self.clock = clock
        self.sample_buffer = np.zeros(num_samples)
        self.sample_count = 0

        @hdl.instance
        def beh_record():
            sb = self.sample_buffer
            sc = self.sample_count
            while True:
                yield clock.posedge

                if self.record:
                    if self.valid:
                        sb[sc] = int(self.data.val)
                        sc += 1

        return beh_record

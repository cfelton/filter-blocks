
from myhdl import Signal, SignalType


class Clock(SignalType):
    def __init__(self, val=bool(0), frequency=1):
        self.frequency = frequency
        super(Clock, self).__init__(val)


class SignalBus(object):
    def __init__(self, stype):
        self.data = Signal(stype)
        self.dv = Signal(bool(0))



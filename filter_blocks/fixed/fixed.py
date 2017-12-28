
import myhdl as hdl
from myhdl import Signal, always, always_comb

from .fixbv import fixbv
from .construct import Construct


class Fixed(fixbv):
    def __init__(self, val, min=-1, max=-1, res=None,
                 round_mode='convergent', overflow_mode='saturate'):
        """

        Args:
            val: initial value
            min: minimum value of the type
            max: maximum value of the type
            res: resolution of the fixed-point type
            round_mode:
            overflow_mode:
        """
        self.imin = min
        self.imax = max
        self.res = res
        self.round_mode = round_mode
        self.overflow_mode = overflow_mode
        super(Fixed, self).__init__(val, min, max, res)

    def __add__(self, other):
        assert isinstance(other, (Fixed, Signal, int))
        ctr = Construct.get_context()
        assert ctr is None or isinstance(ctr, Construct)

        # align, round, handle overflow

        # When in a `clock_domain` context, generate hardware
        if ctr is not None:
            clock = ctr.clock
            load = ctr.load_when

            # Get the signals
            v = Signal()
            w = Signal()
            z = Signal()

            # z = v + w
            # @todo: assign and align
            # @todo: determine comb or latch
            inst = fx_add(v, w, z, clock=clock, load=load)
            # @todo: handle rounding and overflow
            ctr.gens.append(inst)


@hdl.block
def fx_add(v, w, z, clock=None, load=None):

    load = True if load is None else load

    if clock is None:
        @always_comb
        def beh_add():
            z.next = v + w

    else:
        @always(clock.posedge)
        def beh_add():
            if load:
                z.next = v + w

    return beh_add


@hdl.block
def fx_rshift(x, y, shift_by=1):
    @always_comb
    def beh_shift():
        y.next = x >> shift_by
    return fx_rshift


@hdl.block
def fx_lshift(x, y, shift_by=1):
    @always_comb
    def beh_shift():
        y.next = x << shift_by

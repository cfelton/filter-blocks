"""
Context aware constrained integer type.
"""
import myhdl as hdl
from myhdl import Signal, SignalType, intbv
from myhdl import always, always_comb

# @todo: import from crux
# from crux.construct import Construct, CBase
from .construct import Construct, CBase


# Basic construct type, intended as a simple example, mainly for testing
class CInt(CBase):
    def __init__(self, val=0, min=None, max=None):
        """Constrained integer construct type.
        This is a basic construct type, intended as a simple example,
        mainly for testing.  This works like the `myhdl.intbv`.

        Args:
            val: initial value.
            min: minimum value for the integer range.
            max: maximum value for the integer range.
        """
        super(CInt, self).__init__()

        if isinstance(val, SignalType) and isinstance(val.val, intbv):
            itype = val.val
            sig = val
        elif isinstance(val, intbv):
            itype = val
        elif isinstance(val, int) and (min is None or max is None):
            imax = val + 1 if val > 0 else 0
            imin = val if val < 0 else 0
            itype = intbv(val, min=imin, max=imax)
            sig = Signal(itype)
        elif isinstance(val, int):
            itype = intbv(val, min=min, max=max)
            sig = Signal(itype)
        else:
            raise TypeError

        # Save the initial type and value.
        self._itype = itype
        self.sig = sig

    def __add__(self, other):
        x = self.sig
        y = CInt.check_other(other)
        imin = x.min + y.min
        imax = x.max + y.max
        res = CInt((int(x) + int(y)), min=imin, max=imax)
        z = res.sig
        ctx = Construct.get_context()
        clock, _, load = ctx.get_controls()
        ctx.add_block(self.logic_add, x=x, y=y, z=z,
                      clock=clock, load=load)
        return res

    # @todo: add the rest of the operators ...

    @hdl.block
    def logic_add(self, x=None, y=None, z=None, clock=None, load=None):
        """ z = x + y """
        assert isinstance(x, SignalType)
        assert isinstance(y, SignalType)
        assert isinstance(z, SignalType)

        if load is None or not isinstance(load, SignalType):
            load = True

        if clock is None:
            @always_comb
            def beh_add():
                z.next = x + y
        else:
            @always(clock.posedge)
            def beh_add():
                if load:
                    z.next = x + y

        return beh_add

    # @todo: add the rest of the operator logic handlers ...



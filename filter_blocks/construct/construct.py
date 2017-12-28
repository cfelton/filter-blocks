"""
HDL construction via context aware types.  Note, the *construct*
context and objects will be imported from `crux` in the future.
"""
import myhdl as hdl
from myhdl import SignalType, Signal, intbv, always, always_comb

# This is kind-of-wonky, the objects that construct should occur
# behind the scenes adding generators to the current domains generator
# list, only one domain can be active at a time (non-threaded).
active = None


class Block:
    def __init__(self, func, ports):
        self.func = func
        self.ports = ports


class Construct:
    def __init__(self):
        """
        Construction context manager.
        """
        global active
        self.clock = None
        self.reset = None
        self.load_when = None   # additional control signal
        self.latch_ops = None   # operations are latched / registered
        self._blocks = []
        # self._gens = []
        self._insts = None
        # There should only be a single *construct* context
        # active at a time.
        assert active is None
        active = self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        global active
        assert active is self
        active = None

    @staticmethod
    def get_context():
        global active
        return active

    def get_controls(self):
        clock = self.clock if self.latch_ops else None
        reset = self.reset
        load = self.latch_ops
        return clock, reset, load

    def add_block(self, func, **ports):
        self._blocks.append(Block(func, ports))

    @hdl.block
    def blocks(self):
        # @todo: there is a problem if this is called more than once
        #        maybe deleting each item in self._insts would solve
        #        it?
        # A bunch of *blocks* where created with signals going
        # to them, now call each block to get the generators
        # (myhdl._Block).

        # Delete the instances if they exists (blocks called more
        # than once)
        if self._insts is not None:
            for blk in self._insts:
                del blk
            self._insts = None

        # Create an instance for all the blocks added
        insts = [None for _ in self._blocks]
        for ii, blk in enumerate(self._blocks):
            assert isinstance(blk, Block)
            blk_inst = blk.func(**blk.ports)
            # @todo: fix this in the myhdl 0.10dev ...
            # This is a total hack, but there is a name collision for
            # some reason ...
            blk_inst.name += str(ii)
            insts[ii] = blk_inst
        self._insts = insts
        return insts


def clock_domain(clock, reset=None, latch_ops=True):
    c = Construct()
    c.clock = clock
    c.reset = reset
    c.latch_ops = latch_ops
    return c


class when(object):
    def __init__(self, *eli, **ekw):
        """ An event decorator
        The `when` decorator provides some flow control in a
        construct context, this will create

        Example
        =======
        The following example demonstrates how to define an
        event-oriented segment in the construct context, the `when`
        decorated will add the `do_add` generator to the collection
        of generators (logic defining segments).

            with clock_domain(clock) as cd:
                @when(load)
                def do_add():
                   z.next = v + w
            insts = cd.instances()

        """
        self.ctx = Construct.get_context()
        self.events = dict()
        self.events.update(ekw)
        keys = ['e{}'.format(ii) for ii in range(len(eli))]
        for key, evt in zip(keys, eli):
            for _ in range(10):
                if key in self.events:
                    key += 'e'
                assert key not in self.events
            self.events[key] = eli

        for key, sig in self.events.items():
            assert isinstance(sig, SignalType)

    def __call__(self, func):
        """ function wrapper
        """
        self.func = func

        # Create the logic for the when ...
        load = Signal(bool(0))
        assert self.ctx.load_when is None
        self.ctx.load_when = load
        self.ctx.add_block(self.logic_load, **self.events)

        # The function needs to be called in the construct context
        # foreach of the constructors to be generated, the function
        # being called will add more blocks to the context.
        func()

        # Done with the load in this context
        self.ctx.load_when = None

        return None

    @hdl.block
    def logic_load(self, load, **events):
        nev = len(events)
        evt = events.items()

        @always_comb
        def beh_load():
            ld = False
            for ii in range(nev):
                if evt[ii]:
                    ld = True
            load.next = ld

        return beh_load


class CBase(object):
    def __init__(self):
        """Base construction type."""
        self._itype = None
        self._next = None
        self.sig = None

    def __str__(self):
        return str(self.sig)

    @property
    def next(self):
        return None

    @next.setter
    def next(self, nval):
        ctx = Construct.get_context()
        clock, _, load = ctx.get_controls()

        x = type(self).check_other(nval)
        y = self.sig
        ctx.add_block(self.logic_assign, x=x, y=y, clock=clock, load=load)

    @classmethod
    def check_other(cls, other):
        if isinstance(other, cls):
            x = other.sig
        elif isinstance(other, (SignalType, intbv)):
            x = other
        else:
            x = cls(other).sig
        return x

    @hdl.block
    def logic_assign(self, x=None, y=None, clock=None, load=None):
        """ y = x """
        assert isinstance(x, SignalType)
        assert isinstance(y, SignalType)

        if load is None or not isinstance(load, SignalType):
            load = True

        if clock is None:
            @always_comb
            def beh_assign():
                y.next = x
        else:
            @always(clock.posedge)
            def beh_assign():
                if load:
                    y.next = x

        return beh_assign



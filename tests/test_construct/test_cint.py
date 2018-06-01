
import myhdl as hdl
from myhdl import Signal, intbv, always_comb

from filter_blocks.support import Clock, Signals
from filter_blocks.construct import clock_domain
from filter_blocks.construct import CInt


@hdl.block
def block_with_construct(clock, a, b, c):

    # Perform the "math" example in a construct context.
    y = CInt(0, min=c.min, max=c.max)
    with clock_domain(clock) as ctx:
        x = CInt(a) + CInt(b)
        y.next = x + 1
    inst = ctx.blocks()

    @always_comb
    def beh_assign():
        c.next = y.sig

    # insts = [beh_assign] + insts
    # hdl.instances
    return beh_assign, inst


def test_construct_cint():
    clock = Clock(0, frequency=50e6)
    y = CInt(0, min=-8, max=8)

    # Elaboration definitions, the results are evaluated
    # in simulation not the explicit code below - the
    # following *constructs* the HDL (generators) that are
    # simulated and converted.
    with clock_domain(clock) as ctx:
        # Create a new CInt: `x`, create generators for
        # the addition operations.
        x = CInt(2) + CInt(4)
        # Assign to the CInt: `y`, create a generator for
        # the assignment.
        y.next = x + 1
    inst = ctx.blocks()

    # Get a reference ot the output of the construct context
    yy = y.sig

    tbclk = clock.process()

    @hdl.instance
    def tbstim():
        print("[{:8d}] 1a: ".format(hdl.now()), x, y, yy)
        yield hdl.delay(10)
        yield clock.posedge
        yield clock.posedge
        print("[{:8d}] 2a: ".format(hdl.now()), x, y, yy)
        assert yy == 7
        raise hdl.StopSimulation

    # Run a simulation of the above myhdl.generators
    hdl.Simulation([tbclk, tbstim, inst]).run()


def test_construct_block():
    clock = Clock(0, frequency=50e6)
    a, b, c = Signals(intbv(0, min=0, max=8), 3)

    @hdl.block
    def bench_cwb():
        global tbdut

        tbdut = block_with_construct(clock, a, b, c)
        tbclk = clock.process()

        @hdl.instance
        def tbstim():
            print("[{:8d}] 1b: ".format(hdl.now()), a, b, c)
            a.next = 2
            b.next = 4
            yield hdl.delay(10)
            for ii in range(6):
                print("[{:8d}] {}b: ".format(hdl.now(), ii), a, b, c)
                yield clock.posedge
            assert c == 7
            raise hdl.StopSimulation

        # instances doesn't work ??? hdl.instances()
        return tbdut, tbclk, tbstim

    inst = bench_cwb()
    inst.config_sim(trace=True)
    inst.run_sim()


def test_construct_block_conversion():
    clock = Clock(0, frequency=50e6)
    a, b, c = Signals(intbv(0, min=0, max=8), 3)

    # Check the block converts
    block_with_construct(clock, a, b, c).convert(testbench=False)

    @hdl.block
    def bench_cint_convert():
        tbdut = block_with_construct(clock, a, b, c)
        tbclk = clock.process()

        @hdl.instance
        def tbstim():
            a.next = 2
            b.next = 4

            # flush the non-initialized
            for ii in range(7):
                yield clock.posedge

            for ii in range(7):
                print("%d  %d  %d" % (a, b, c))
                yield clock.posedge
            assert c == 7

            a.next = 2
            b.next = 1
            for ii in range(7):
                print("%d  %d  %d" % (a, b, c))
                yield clock.posedge
            assert c == 4

            raise hdl.StopSimulation

        # instances doesn't work ??? hdl.instances()
        return tbdut, tbclk, tbstim

    inst = bench_cint_convert()
    inst.config_sim()
    inst.convert()
    # TODO: this needs to be fixed, in myhdl base
    # inst.analyze_convert()
    # inst.verify_convert()


if __name__ == '__main__':
    test_construct_cint()
    test_construct_block()
    test_construct_block_conversion()

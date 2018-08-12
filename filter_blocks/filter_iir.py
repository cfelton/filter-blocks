"""
Simple IIR Filter
=================
The following is a straight forward HDL description of a
direct-form-I IIR filter.  This module can be used to
generate synthesizable Verilg/VHDL.
:Author: Christopher Felton <chris.felton@gmail.com>
"""

import myhdl as hdl
from myhdl import Signal, intbv, always, always_comb, always_seq
from .support import Samples


@hdl.block
def filter_iir(glbl, sigin, sigout, b, a, shared_multiplier=False):
    """Basic IIR direct-form I filter.
    Ports:
        glbl (Global): global signals.
        sigin (SignalBus): input digital signal.
        sigout (SignalBus): output digitla signal.
    Args:
        b (tuple, list): numerator coefficents.
        a (tuple, list): denominator coefficents.
    Returns:
        inst (myhdl.Block, list):
    """
    assert isinstance(sigin, Samples)
    assert isinstance(sigout, Samples)
    assert isinstance(a, tuple)
    assert isinstance(b, tuple)

    # All the coefficients need to be an `int`, the
    # class (`???`) handles all the float to fixed-poit
    # conversions.
    ra = [isinstance(aa, int) for aa in a]
    rb = [isinstance(bb, int) for bb in b]
    assert all(ra)
    assert all(rb)

    w = sigin.word_format
    ymax = 2**(w[0]-1)
    vmax = 2**(2*w[0])  # double width max and min
    vmin = -vmax

    # Quantized IIR coefficients
    b0, b1, b2 = b
    a1, a2 = a
    q, qd = w[0]-1, 2*w[0]

    # Locally reference the interface signals
    clock, reset = glbl.clock, glbl.reset
    x, xdv = sigin.data, sigin.data_valid
    y, ydv = sigout.data, sigout.data_valid

    # Delay elements, list-of-signals (double length for all)
    ffd = [Signal(intbv(0, min=vmin, max=vmax)) for _ in range(2)]
    fbd = [Signal(intbv(0, min=vmin, max=vmax)) for _ in range(2)]
    yacc = Signal(intbv(0, min=vmin, max=vmax))
    dvd = Signal(bool(0))

    @always(clock.posedge)
    def beh_direct_form_one():
        if sigin.valid:
            ffd[1].next = ffd[0]
            ffd[0].next = x

            fbd[1].next = fbd[0]
            fbd[0].next = yacc[qd:q].signed()

    @always_comb
    def beh_acc():
        # double precision accumulator
        yacc.next = (b0 * x) + (b1 * ffd[0]) + (b2 * ffd[1]) \
                    - (a1 * fbd[0]) - (a2 * fbd[1])

    @always_seq(clock.posedge, reset=reset)
    def beh_output():
        dvd.next = xdv
        y.next = yacc[qd:q].signed()
        ydv.next = dvd

    # @todo add shared multiplier version ...

    return hdl.instance()


@hdl.block
def filter_iir_sos(glbl, x, y, b, a, w):
    """IIR sum of sections ...
    """
    assert len(b) == len(a)
    number_of_sections = len(b)
    list_of_insts = [None for _ in range(number_of_sections)]

    xb = [Samples(x.val) for _ in range(number_of_sections)]
    xb[0] = x
    xb[number_of_sections-1] = y

    for ii in range(len(b)):
        list_of_insts[ii] = filter_iir(
            glbl, xb[ii], xb[ii+1],
            b=tuple(map(int, b[ii])), a=tuple(map(int, a[ii])),
        )

    return list_of_insts
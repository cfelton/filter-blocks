"""
Simple IIR Filter
=================
The following is a straight foward HDL description of a
direct-form I IIR filter.  This module can be used to
generate synthesizable Verilg/VHDL.
How to use this module
----------------------
 1. Instantiate an instance of the iir_filter, pass the
    desired low-pass frequency cutoff (`fc`) and the
    sample rate (`fs`).
 2. Test the frequency response with a random input simulation.
    Collect the random inputs and the filter outputs, compute
    the FFT of each and H(w) = Y(w) / X(w).
 3. If all looks good create the Verilog and VHDL.
This code is discussed in the following:
http://www.fpgarelated.com/showarticle/7.php
http://dsp.stackexchange.com/questions/1605/designing-butterworth-filter-in-matlab-and-obtaining-filter-a-b-coefficients-a
:Author: Christopher Felton <chris.felton@gmail.com>
"""

import myhdl as hdl
from myhdl import Signal, intbv, always, always_comb, SignalType, traceSignals, block, delay, instance, Simulation, StopSimulation
import numpy as np


def filter_iir(clk,reset, x, y, b, w=(24,0)):
    """Basic IIR direct-form I filter.
    Ports:
        glbl (Global): global signals.
        x (SignalBus): input digital signal.
        y (SignalBus): output digitla signal.
    Args:
        b (tuple, list): numerator coefficents.
        a (tuple, list): denominator coefficents.
    Returns:
        inst (myhdl.Block, list):
    """
    assert isinstance(x, SignalBus)
    assert isinstance(y, SignalBus)
    assert isinstance(b, tuple)

    # All the coefficients need to be an `int`, the
    # class (`???`) handles all the float to fixed-poit
    # conversions.
    rb = [isinstance(bb, int) for bb in b]
   # assert all(ra)
   # assert all(rb)

    ymax = 2**(w[0]-1)
    vmax = 2**(2*w[0])  # double widht max and min
    vmin = -vmax

    # Quantized IIR coefficients
    b0, b1, b2= b
    q, qd = w[0]-1, 2*w[0]
   

   # print(b0,b1,b2,a1,a2)
   # print(x.data, x.valid, b0,b1, reset)

    # Delay elements, list-of-signals (double length for all)
    ffd = [Signal(intbv(0, min=vmin, max=vmax)) for _ in range(2)]

    yacc = Signal(intbv(0, min=vmin, max=vmax))
    ys = Signal(intbv(0, min=-ymax, max=ymax))

    #clock, reset = glbl.clock, glbl.reset

    @always(clk.posedge)
    def beh_direct_form_one():
        print (x.valid)
        if x.valid:
            ffd[1].next = ffd[0]
            ffd[0].next = x.data
        

        # double precision accumulator
        y.data.next = yacc[qd:q].signed()
        y.valid.next = True if x.valid else False

    return beh_direct_form_one
    @always_comb
    def beh_acc():
        # double precision accumulator
        yacc.next = (b0*x.data) + (b1*ffd[0]) + (b2*ffd[1]) 

    return beh_acc

<<<<<<< HEAD
from filter_blocks.fda import FilterFIR
import numpy as np

def main():
    """Meant to emulate how pyfda will pass parameters to filters"""
=======

from filter_blocks.fda import FilterFIR
import numpy as np


def test_fda_fir():
    """Test basic API parameter passing
    """
>>>>>>> master
    coef = np.empty(100)
    coef.fill(8388607)
    hdlfilter = FilterFIR()
    b = [8388607, 8388607, 8388607, 8388607, 8388607]
<<<<<<< HEAD
    hdlfilter.set_coefficients(coeff_b = b)
    hdlfilter.set_word_format(coeff_w = (24, 23, 0), input_w = (24,23,0), output_w = (50,23,0))
    hdlfilter.set_stimulus(coef)
    hdlfilter.run_sim()
    hdlfilter.convert(hdl = 'VHDL')
=======
    hdlfilter.set_coefficients(coeff_b=b)
    hdlfilter.set_word_format(
        coeff_w=(24, 23, 0), input_w=(24, 23, 0), output_w=(50, 23, 0)
    )
    hdlfilter.set_stimulus(coef)
    hdlfilter.run_sim()
    hdlfilter.convert(hdl='Verilog')


>>>>>>> master
if __name__ == '__main__':
    test_fda_fir()

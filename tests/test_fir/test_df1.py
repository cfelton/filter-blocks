from filter_blocks.fda import FilterFIR
import numpy as np

def main():
    """Meant to emulate how pyfda will pass parameters to filters"""
    coef = np.empty(100)
    coef.fill(2)
    hdlfilter = FilterFIR()
    b = [23424, 2434, 1, 1, 1]
    hdlfilter.set_coefficients(coeff_b = b)
    hdlfilter.set_word_format((26, 24, 0),(40,23,0))
    hdlfilter.set_stimulus(coef)
    hdlfilter.run_sim()
    hdlfilter.convert(hdl = 'vhdl')
if __name__ == '__main__':
    main()

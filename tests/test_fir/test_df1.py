from filter_blocks.fda import FilterFIR
import numpy as np

def main():
    """Meant to emulate how pyfda will pass parameters to filters"""
    coef = np.empty(100)
    coef.fill(8388607)
    hdlfilter = FilterFIR()
    b = [8388607, 8388607, 8388607, 8388607, 8388607]
    hdlfilter.set_coefficients(coeff_b = b)
    hdlfilter.set_word_format(coeff_w = (24, 23, 0), input_w = (24,23,0), output_w = (50,23,0))
    hdlfilter.set_stimulus(coef)
    hdlfilter.run_sim()
    hdlfilter.convert(hdl = 'VHDL')
if __name__ == '__main__':
    main()

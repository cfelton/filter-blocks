from filter_blocks.fda import FilterIIR
import numpy as np

def main():
    """Meant to emulate how pyfda will pass parameters to filters"""
    stim = np.empty(15)
    stim.fill(1)
    hdlfilter = FilterIIR()
    b = [1, 2, 1]
    a = [1,2,1]
    hdlfilter.set_coefficients(coeff_b = b, coeff_a = a)
    hdlfilter.set_word_format((24, 23, 0),(24,23,0),(54,53,0))
    hdlfilter.set_stimulus(stim)
    hdlfilter.run_sim()
    hdlfilter.convert(hdl = 'verilog')
if __name__ == '__main__':
    main()

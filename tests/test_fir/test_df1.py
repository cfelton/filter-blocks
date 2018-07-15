from filter_blocks.fda import FilterFIR
import numpy as np

def main():
    """Meant to emulate how pyfda will pass parameters to filters"""
    coef = np.empty(100)
    coef.fill(8388607)
    hdlfilter = FilterFIR()
    b = [1, 2, 3, 1, 0]
    hdlfilter.set_word_format((24, 23, 0))
    hdlfilter.set_coefficients(coeff_b = b)
    hdlfilter.set_stimulus(coef, (24,23,0))
    hdlfilter.run_sim()
    #hdlfilter.convert()
if __name__ == '__main__':
    main()

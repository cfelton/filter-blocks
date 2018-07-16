from filter_blocks.fda import FilterIIR
import numpy as np

def main():
    """Meant to emulate how pyfda will pass parameters to filters"""
    coef = np.empty(100)
    coef.fill(2)
    hdlfilter = FilterIIR()
    b = [8388607, 8388607, 1, 1, 1]
    a = [1,2,1,1,1]
    hdlfilter.set_word_format((24, 23, 0))
    hdlfilter.set_coefficients(coeff_b = b, coeff_a = a)
    hdlfilter.set_stimulus(coef, (24,23,0))
    hdlfilter.run_sim()
    #hdlfilter.convert()
if __name__ == '__main__':
    main()

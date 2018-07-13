from filter_blocks.fda import FilterFIR
import numpy as np

def main():
    """Meant to emulate how pyfda will pass parameters to filters"""

    hdlfilter = FilterFIR()
    b = (1, 2, 3, 1)
    hdlfilter.set_coefficients(coeff_b = b)
    hdlfilter.set_stimulus(np.ones(100))
    hdlfilter.run_sim()
    hdlfilter.convert()
if __name__ == '__main__':
    main()

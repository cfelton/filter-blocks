from filter_blocks.fda import FilterFIR
import numpy as np

def main():

    hdlfilter = FilterFIR(0, 0)
    b = [1, 2, 3, 1]
    hdlfilter.set_coefficients(b)
    hdlfilter.set_stimulation(np.ones(100))
    testfil = hdlfilter.filter_block()
    testfil.run_sim()

if __name__ == '__main__':
    main()

from filter_blocks.fda import FilterIIR
import numpy as np
import matplotlib.pyplot as plt

def main():
    """Meant to emulate how pyfda will pass parameters to filters"""
    stim = np.empty(15)
    stim.fill(-8388607)
    hdlfilter = FilterIIR()
    b = [8388607, 8388607, 8388607]
    a = [1,2,1]
    hdlfilter.set_coefficients(coeff_b = b, coeff_a = a)
    hdlfilter.set_word_format((24, 23, 0),(24,23,0),(54,53,0))
    hdlfilter.set_stimulus(stim)
    hdlfilter.run_sim()
    hdlfilter.convert(hdl = 'verilog')
    y = hdlfilter.get_response()
    print(y)
    hdlfilter.convert(hdl = 'verilog')
    plt.plot(y, 'b')
    plt.show()
if __name__ == '__main__':
    main()

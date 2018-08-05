from filter_blocks.fda import FilterIIR
import numpy as np
import matplotlib.pyplot as plt

def main():
    """Meant to emulate how pyfda will pass parameters to filters"""
    stim = np.empty(15)
    stim.fill(32767)
    hdlfilter = FilterIIR()
    b = [1287, 5148, 7722, 5148, 1287]
    a = [1, -22954, 14021, -3702, 459]
    hdlfilter.set_coefficients(coeff_b = b, coeff_a = a)
    hdlfilter.set_word_format((16, 23, 0),(16,23,0),(26,53,0))
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

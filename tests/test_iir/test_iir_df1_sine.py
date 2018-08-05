<<<<<<< HEAD
from filter_blocks.fda import FilterIIR
import numpy as np
import scipy.signal as signal
import math
import matplotlib.pyplot as plt



def fixp_sine(bsc_int, asc_int, B1, L1):

=======


import math
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

from filter_blocks.fda import FilterIIR


def fixp_sine(bsc_int, asc_int, B1, L1):
>>>>>>> master
    # N=20
    # sig = [np.sin(0.1*np.pi*i) for i in np.arange(0,N,1)]

    sig = signal.unit_impulse(20)

<<<<<<< HEAD
    B2 = 12 # Number of bits
    L2 = math.floor(math.log((2**(B2-1)-1)/max(sig), 2))  # Round towards zero to avoid overflow

    sig = np.multiply(sig, 2**L2)
=======
    B2 = 12  # Number of bits
    L2 = math.floor(math.log((2 ** (B2 - 1) - 1) / max(sig), 2))  # Round towards zero to avoid overflow

    sig = np.multiply(sig, 2 ** L2)
>>>>>>> master
    sig = sig.round()
    sig = sig.astype(int)
    print(sig)

<<<<<<< HEAD

    hdlfilter = FilterIIR()
    hdlfilter.set_coefficients(coeff_b = bsc_int, coeff_a= asc_int)
    hdlfilter.set_word_format((B1, B1-1, 0),(B2, B2-1 ,0),(1000 , 39 , 0))
=======
    hdlfilter = FilterIIR()
    hdlfilter.set_coefficients(coeff_b=bsc_int, coeff_a=asc_int)
    hdlfilter.set_word_format((B1, B1 - 1, 0), (B2, B2 - 1, 0), (1000, 39, 0))
>>>>>>> master
    hdlfilter.set_stimulus(sig)
    hdlfilter.run_sim()
    y = hdlfilter.get_response()

<<<<<<< HEAD
    yout = np.divide(y,2**B1)
    print(yout)
    #hdlfilter.convert(hdl = 'verilog')
    #plt.plot(yout, 'b')
    #plt.show()
=======
    yout = np.divide(y, 2 ** B1)
    print(yout)
    # hdlfilter.convert(hdl = 'verilog')
    # TODO: plotting should not be included in the tests,
    #       create simple scripts in filter-blocks/scripts
    #       for plotting ...
    # plt.plot(yout, 'b')
    # plt.show()
>>>>>>> master

    return yout


<<<<<<< HEAD


def floatp_sine(b, a, B1, L1):

    #sig = [np.sin(0.1*np.pi*i) for i in np.arange(0,x,1)]
    sig = signal.unit_impulse(10)
    #print(sig)


    B2 = 12 # Number of bits
    L2 = math.floor(math.log((2**(B2-1)-1)/max(sig), 2))  # Round towards zero to avoid overflow
    #print(L)
    sig = np.multiply(sig, 2**L2)
=======
def floatp_sine(b, a, B1, L1):
    # sig = [np.sin(0.1*np.pi*i) for i in np.arange(0,x,1)]
    sig = signal.unit_impulse(10)
    # print(sig)

    B2 = 12  # Number of bits
    L2 = math.floor(math.log((2 ** (B2 - 1) - 1) / max(sig), 2))  # Round towards zero to avoid overflow
    # print(L)
    sig = np.multiply(sig, 2 ** L2)
>>>>>>> master
    sig = sig.round()
    sig = sig.astype(int)

    y_tf = signal.lfilter(b, a, sig)

    print(y_tf)
<<<<<<< HEAD
    
    return y_tf




def main():
    """Meant to emulate how pyfda will pass parameters to filters"""
    
=======

    return y_tf


def test_iir_df1_sine():
    """Meant to emulate how pyfda will pass parameters to filters"""

>>>>>>> master
    # fs = 1000.
    # f1 = 45.
    # f2 = 95.
    # b = signal.firwin(3,[f1/fs*2,f2/fs*2])    #3 taps
<<<<<<< HEAD
    #b, a = signal.iirfilter(3, [0.4, 0.7], rs=60, btype='band', ftype='cheby2')
=======
    # b, a = signal.iirfilter(3, [0.4, 0.7], rs=60, btype='band', ftype='cheby2')
>>>>>>> master
    # print(len(b))
    # print(len(a))
    # print(b)
    # print(a)

<<<<<<< HEAD
    #print(max([max(b),max(a)]))
    #convert floating point to fixed point 

=======
    # print(max([max(b),max(a)]))
    # convert floating point to fixed point
>>>>>>> master

    b, a = signal.ellip(3, 0.009, 80, 0.05, output='ba')

    print(b)
    print(a)
<<<<<<< HEAD
    
    #y_sos = signal.sosfilt(sos, x)
=======

    # y_sos = signal.sosfilt(sos, x)
>>>>>>> master
    # plt.plot(y_tf, 'r', label='TF')
    # plt.plot(y_sos, 'k', label='SOS')
    # plt.legend(loc='best')
    # plt.show()

<<<<<<< HEAD




    B1 = 12 # Number of bits
    L1 = math.floor(math.log((2**(B1-1)-1)/max([max(b),max(a)]), 2))  # Round towards zero to avoid overflow
    bsc = b*(2**B1)
    asc = a*(2**B1)
=======
    B1 = 12  # Number of bits
    L1 = math.floor(math.log((2 ** (B1 - 1) - 1) / max([max(b), max(a)]), 2))  # Round towards zero to avoid overflow
    bsc = b * (2 ** B1)
    asc = a * (2 ** B1)
>>>>>>> master
    bsc_int = [int(x) for x in bsc]
    asc_int = [int(x) for x in asc]
    print(bsc_int)
    print(asc_int)

    y1 = fixp_sine(bsc_int, asc_int, B1, L1)
<<<<<<< HEAD
    #print(y1/2**B1)
    y2 = floatp_sine(b, a, B1, L1)
    #y = edge(B1, L1)

    #print(y1)
    #print(y2)
    #y1 = y1[6:19] #hardcoded presently. Needs to be 
    #y2 = y2[:13]

    #print(y1)
    #print(y2)
    #print( ((y1 - y2) ** 2).mean(axis=None))


   
if __name__ == '__main__':
    main()
=======
    # print(y1/2**B1)
    y2 = floatp_sine(b, a, B1, L1)
    # y = edge(B1, L1)

    # print(y1)
    # print(y2)
    # y1 = y1[6:19] #hardcoded presently. Needs to be
    # y2 = y2[:13]

    # print(y1)
    # print(y2)
    # print( ((y1 - y2) ** 2).mean(axis=None))


if __name__ == '__main__':
    test_iir_df1_sine()
>>>>>>> master

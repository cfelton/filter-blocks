from filter_blocks.fda import FilterIIR
import numpy as np
import scipy.signal as signal
import math
import matplotlib.pyplot as plt



def fixp_sine(bsc_int, asc_int, B1, L1):

    N=20
    sig = [np.sin(0.1*np.pi*i) for i in np.arange(0,N,1)]

    B2 = 12 # Number of bits
    L2 = math.floor(math.log((2**(B2-1)-1)/max(sig), 2))  # Round towards zero to avoid overflow

    sig = np.multiply(sig, 2**L2)
    sig = sig.round()
    sig = sig.astype(int)
    print(sig)


    hdlfilter = FilterIIR()
    hdlfilter.set_coefficients(coeff_b = bsc_int, coeff_a= asc_int)
    hdlfilter.set_word_format((B1, B1-1, 0),(B2, B2-1 ,0),(1000 , 999 , 0))
    hdlfilter.set_stimulus(sig)
    hdlfilter.run_sim()
    y = hdlfilter.get_response()

    yout = np.divide(y,2**B1)
    print(yout)
    hdlfilter.convert(hdl = 'verilog')
    plt.plot(yout, 'b')
    plt.show()

    return yout


def edge(B1, L1):


    B2 = 12
    N = 10 # number of coefficients

    max_coef = 2**(B1-1)-1 
    min_coef = -2**(B1-1)

    b_max = [max_coef] * N

    max_in = 2**(B2-1)-1
    min_in = -2**(B2-1)

    coef = np.empty(100)
    coef.fill(max_in)

    hdlfilter = FilterFIR()
    hdlfilter.set_coefficients(coeff_b = b_max)
    hdlfilter.set_word_format((B1, B1-1, 0),(B2, B2-1, 0),(40, 39, 0))
    hdlfilter.set_stimulus(coef)
    hdlfilter.run_sim()
    y = hdlfilter.get_response()

    # yout = np.divide(y,2**L1)
    # hdlfilter.convert(hdl = 'VHDL')
    # plt.plot(yout, 'b')
    # plt.show()

    return y


def floatp_sine(b, a, B1, L1):

    x=20
    sig = [np.sin(0.1*np.pi*i) for i in np.arange(0,x,1)]
    #print(sig)


    B2 = 12 # Number of bits
    L2 = math.floor(math.log((2**(B2-1)-1)/max(sig), 2))  # Round towards zero to avoid overflow
    #print(L)
    sig = np.multiply(sig, 2**L2)
    sig = sig.round()
    sig = sig.astype(int)

    y = []
    w = []
    N = len(b)

    for n in range(N,len(sig)):
        sop = 0
        for i in range(N):
            sop = sop + sig[n-i]*b[i] 
        w.append(sop)

    for n in range(N,len(sig)):
        sop = 0
        for i in range(N):
            sop = w[n] - w[n-i]*a[i] 
        w.append(sop)
    
    return y




def main():
    """Meant to emulate how pyfda will pass parameters to filters"""
    
    # fs = 1000.
    # f1 = 45.
    # f2 = 95.
    # b = signal.firwin(3,[f1/fs*2,f2/fs*2])    #3 taps
    b, a = signal.iirfilter(3, [0.4, 0.7], rs=60, btype='band', ftype='cheby2')
    # print(len(b))
    # print(len(a))
    # print(b)
    # print(a)

    #print(max([max(b),max(a)]))
    #convert floating point to fixed point 

    B1 = 12 # Number of bits
    L1 = math.floor(math.log((2**(B1-1)-1)/max([max(b),max(a)]), 2))  # Round towards zero to avoid overflow
    bsc = b*(2**B1)
    asc = a*(2**B1)
    bsc_int = [int(x) for x in bsc]
    asc_int = [int(x) for x in asc]
    print(bsc_int)
    print(asc_int)

    y1 = fixp_sine(bsc_int, asc_int, B1, L1)
    #print(y1/2**B1)
    y2 = floatp_sine(b, a, B1, L1)
    #y = edge(B1, L1)

    #print(y1)
    #print(y2)
    y1 = y1[6:19] #hardcoded presently. Needs to be 
    y2 = y2[:13]

    #print(y1)
    #print(y2)
    #print( ((y1 - y2) ** 2).mean(axis=None))


   
if __name__ == '__main__':
    main()
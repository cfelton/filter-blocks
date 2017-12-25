

import numpy as np
from scipy import signal


def get_fir_coefs(ntaps, hmax, ftype):
    """
    Get a set of FIR filter coefficients for 
    Args:
        ntaps:
        hmax:
        ftype:

    Returns:
        b (list): return a list of fixed-point coefficients
    """
    assert ftype in ('low', 'high', 'band', 'stop', 'rand')




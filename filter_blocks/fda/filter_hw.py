import numpy as np

class FilterHardware(object):
    """Top level class. Contains filter parameters."""
    def __init__(self, b, a, w):
        """
        Args:
            b (list of int): list of numerator coefficients.
            a (list of int): list of denominator coefficients. 
            word_format (tuple of int): word format (W,WI,WF).
            n_cascades(int):
            sigin(numpy int array):
            nfft(int):
            hdl_name(str):
            hdl_directory(str):
            hdl_target(str):
        """
        self.b = b  # numerator coefficients
        self.a = a  # denominator coefficients
        self.word_format = w

        self.n_cascades = 0
        self.sigin = np.array([])
        self._shared_multiplier = False
        self._sample_rate = 1
        self._clock_frequency = 1

        self.nfft = 1024

        self.hdl_name = 'name'
        self.hdl_directory = 'directory'
        self.hdl_target = 'verilog'

        # A reference to the HDL block
        self.hardware = None

    def set_coefficients(self, coeff_b, coeff_a = None):
        """Set filter coefficients.

        Args:
            coefficients (list): list of filter coefficients
            param2 (str): The second parameter.
        """
        self.b = coeff_b
        self.a = coeff_a

    def set_stimulus(self, sigin):
        """Set filter stimulus

        Args:
            sigin (np array int): numpy array of filter stimulus 
        """
        self.sigin = sigin.tolist()
    
    def set_cascade(self, n_cascades):
        """Set number of filter cascades

        Args:
            n_cascades (int): no of filter sections connected together
        """
        self.n_cascades = n_cascades

    def set_word_format(self, w):
        """Set word format

        Args:
            word_format (tuple of int): word format (W,WI,WF)
        """
        self.word_format = w

    def get_fixed_coefficients(self):
        raise NotImplementedError

    def get_single_coefficients(self):
        raise NotImplementedError

    def convert(self):
        raise NotImplementedError

    def process(self, glbl, smpi, smpo):
        raise NotImplementedError

    def filter_instance(self, glbl, smpi, smpo):
        raise NotImplementedError


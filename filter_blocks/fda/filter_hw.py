import numpy as np

class FilterHardware(object):
    """Top level class. Contains filter parameters."""
    def __init__(self, b, a):
        """
        Args:
            b (list of int): list of numerator coefficients.
            a (list of int): list of denominator coefficients. 
            coef_word_format (tuple of int): word format (W,WI,WF).
            n_cascades(int):
            sigin(numpy int array):
            nfft(int):
            hdl_name(str):
            hdl_directory(str):
            hdl_target(str):
        """
        #numerator coefficient
        if b is not None:
            self.b = tuple(b)

        # denominator coefficients
        if a is not None:
            self.a = tuple(a)
        

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
            coeff_b (list): list of numerator filter coefficients
            coeff_a (list): list of denominator filter coefficients
        """
        self.b = tuple(coeff_b)
        if coeff_a is not None:
            self.a = tuple(coeff_a)

    def set_stimulus(self, sigin):
        """Set filter stimulus

        Args:
            sigin (np array int): numpy array of filter stimulus 
            bits (int) : no of bits
        """
        self.sigin = sigin.tolist()
    
    def set_cascade(self, n_cascades):
        """Set number of filter cascades

        Args:
            n_cascades (int): no of filter sections connected together
        """
        self.n_cascades = n_cascades

    def set_word_format(self, coeff_w, input_w, output_w = (24,23,0)):
        """Set word format

        Args:
            coef_word_format (tuple of int): word format (W,WI,WF)
            input_word_format (tuple of int): word format (W,WI,WF)
            output_word_format (tuple of int): word format (W,WI,WF)
        """
        self.coef_word_format = coeff_w
        self.input_word_format = input_w
        self.output_word_format = output_w

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




class FilterHardware(object):
    def __init__(self, b, a):
        self.b = b  # numerator coefficients
        self.a = a  # denominator coefficients

        self.word_format = (24, 0, 23)
        self._shared_multiplier = False
        self._sample_rate = 1
        self._clock_frequency = 1

        self.nfft = 1024

        self.hdl_name = 'name'
        self.hdl_directory = 'directory'
        self.hdl_target = 'verilog'

        # A reference to the HDL block
        self.hardware = None

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


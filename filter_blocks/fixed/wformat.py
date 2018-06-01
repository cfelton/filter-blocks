

class FixedPointFormat(object):
    def __init__(self, wl, iwl, fwl=None):
        """
        Keep track of the fractional point position.
        Args:
            wl (int): word length
            iwl (int): integer word length
            fwl (int): fractional word length
        """
        if fwl is None:
            fwl = wl - iwl - 1
        assert wl == iwl + fwl + 1
        self._wl = None    # total word length
        self._iwl = None   # integer word length
        self._fwl = None   # fractional word length
        self.word_format = wl, iwl, fwl

    @property
    def word_format(self):
        return self._wl, self._iwl, self._fwl

    @word_format.setter
    def word_format(self, fmt):
        self._wl, self._iwl, self._fwl = fmt

    def __len__(self):
        return 3

    def __str__(self):
        s = "({}, {}. [{}])".format(*self.word_format)
        return s

    def __getitem__(self, ii):
        val = self.word_format[ii]
        return val

    def __setitem__(self, key, val):
        if isinstance(key, int):
            keys, vals = [key], [val]
        elif isinstance(key, slice):
            keys = list(range(*key.indices(3)))
            vals = val
        else:
            raise TypeError

        for k, v in zip(keys, vals):
            if k == 0:
                self._wl = v
            elif k == 1:
                self._iwl = v
            elif k == 2:
                self._fwl = v
            else:
                raise IndexError

    def __eq__(self, other):
        cmp = True
        if isinstance(other, FixedPointFormat):
            for s, o in zip(self[:], other[:]):
                if s != 0:
                    cmp = False
        else:
            cmp = False

        return cmp

    def __addsub__(self, other):
        """ Addition or Subtraction grows the format by one
        """
        assert isinstance(other, FixedPointFormat), \
            "Invalid type for other {}".format(type(other))

        iwl = max(self._iwl, other._iwl) + 1
        fwl = max(self._fwl, other._fwl)
        wl = iwl + fwl + 1
        return FixedPointFormat(wl, iwl, fwl)

    def __muldiv__(self, other):
        """ Multiplication and Division double the word size
        """
        assert isinstance(other,FixedPointFormat), \
            "Invalid type for other {}".format(type(other))
        wl = self._wl + other._wl
        fwl = self._fwl + other._fwl
        iwl = wl - fwl - 1
        return FixedPointFormat(wl, iwl, fwl)

    def __add__(self, other):
        return self.__addsub__(other)

    def __sub__(self, other):
        return self.__addsub__(other)

    def __mul__(self, other):
        return self.__muldiv__(other)

    def __div__(self, other):
        return self.__muldiv__(other)






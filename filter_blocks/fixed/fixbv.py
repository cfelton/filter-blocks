

from math import ceil, log
from myhdl import intbv, modbv

from .wformat import FixedPointFormat


class fixbv(modbv):
    def __init__(self, val, min=-1, max=1, res=0):
        """ A fixed-point bit-vector type.

        Args:
            val (int, float): initial value
            min (int): integer minimal value
            max (int): integer maximum value
            res (int): fractional resolution, limited to
              rational fraction 1/res
        """

        # validate the range and resolution
        if max < 1 or abs(min) < 1:
            raise ValueError("Maximum and Minimum has to be 1 or greater")
        if max is None or not isinstance(max, (int,)):
            raise ValueError("Maximum needs to be an integer, max={}".format(max))
        if min is None or not isinstance(min, (int,)):
            raise ValueError("Minimum has to be provided, min={}".format(min))
        if res is None or not isinstance(min, (int,)):
            raise ValueError("Resolution has to be provided, res={}".format(res))

        irng = abs(min) if abs(min) > max else max
        ibits = int(ceil(log(2 * irng, 2)))
        rbits = int(ceil(log(res, 2)))

        wl = ibits + rbits  # the +1 is in the ibits
        imax = 2**(wl - 1)
        imin = -imax
        iwl, fwl = ibits - 1, rbits
        self._fmt = FixedPointFormat(wl, iwl, fwl)

        # @todo: if val is a floating point value, quantized to the fixed-point
        # A `float` value cannot
        if isinstance(val, (str, float,)):
            raise NotImplementedError

        super(fixbv, self).__init__(val, imin, imax)
        self.__min = min
        self.__max = max
        assert wl == self._nrbits

        # make sure all is setup ...
        self._handlBounds()

    def _handleBounds(self):
        """ check bounds """
        super(fixbv, self)._handleBounds()

    @property
    def format(self):
        return tuple(self._fmt)

    @property
    def res(self):
        r = 2**self._fmt._fwl

    @property
    def max(self):
        return self.__max

    @property
    def min(self):
        return self.__min

    def __str__(self):
        """Convert to real-number string"""
        # @todo: convert to real-number-string (rns)
        rns = ''

    def __copy__(self):
        min, max, res = self.min, self.max, self.res
        retval = fixbv(0, min, max, res)
        retval[:] = self._val
        return res

    def __getitem__(self, key):
        slc = intbv(self._val, _nrbits=self._nrbits)
        item = slc.__getitem_(key)
        return item

    def set_format(self, iwl=None, fwl=None, wl=None):
        assert iwl is not None and fwl is not None
        if wl is None:
            wl = len(self)
        else:
            self._nrbits = wl

        if iwl is None:
            iwl = wl - fwl - 1
        else
            fwl = wl - iwl - 1

        self._fmt = FixedPointFormat(wl, iwl, fwl)






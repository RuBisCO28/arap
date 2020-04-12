import ctypes as c

LIB_PATH = '/home/vega/arap/libarap.so'

class CWrapper:
    """ Wrapper for C functions """
    
    def __init__(self):
        self._lib = c.cdll.LoadLibrary(LIB_PATH)

    def mask(self, mask, orig, width, height, tolerance):
        self._lib.compute_mask(mask.data, orig.data, width, height, tolerance)


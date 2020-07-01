from gmplot.color import _get_hex_color
from gmplot.utility import _get_value

from gmplot.drawables.symbols.circle import _Circle
from gmplot.drawables.symbols.plus import _Plus
from gmplot.drawables.symbols.x import _X

class _Symbol(object):
    _SHAPES = {
        'o': _Circle,
        '+': _Plus,
        'x': _X
    }

    @staticmethod
    def is_valid(shape):
        '''
        Return whether or not a shape is valid.

        Args:
            shape (str): Shape of a symbol.
        
        Returns:
            bool: True if the shape is valid, False otherwise.
        '''
        return shape in _Symbol._SHAPES

    def __init__(self, shape, lat, lng, size, **kwargs):
        '''
        Args:
            shape (str): Shape of the symbol, as 'o', 'x', or '+'.
            lat (float): Latitude of the center of the symbol.
            lng (float): Longitude of the center of the symbol.
            size (int): Size of the symbol, in meters.

        Optional:

        Args:
            edge_alpha/ea (float): Opacity of the symbol's edge, ranging from 0 to 1. Defaults to 1.0.
            edge_width/ew (int): Width of the symbol's edge, in pixels. Defaults to 1.
            face_alpha/alpha (float): Opacity of the symbol's face, ranging from 0 to 1. Defaults to 0.5.
            color/c/face_color/fc (str): Color of the symbol's face.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            color/c/edge_color/ec (str): Color of the symbol's edge.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.
        '''
        kwargs.setdefault('edge_color', _get_hex_color(_get_value(kwargs, ['color', 'c', 'edge_color', 'ec'], '#000000')))
        kwargs.setdefault('edge_alpha', _get_value(kwargs, ['edge_alpha', 'ea'], 1.0))
        kwargs.setdefault('edge_width', _get_value(kwargs, ['edge_width', 'ew'], 1))
        kwargs.setdefault('face_alpha', _get_value(kwargs, ['face_alpha', 'alpha'], 0.5))
        kwargs.setdefault('face_color', _get_hex_color(_get_value(kwargs, ['color', 'c', 'face_color', 'fc'], '#000000')))
        kwargs.setdefault('precision', _get_value(kwargs, ['precision'], 6))

        self._symbol = self._SHAPES[shape](lat, lng, size, **kwargs)

    def write(self, w):
        '''
        Write the symbol.

        Args:
            w (_Writer): Writer used to write the symbol.
        '''
        self._symbol.write(w)

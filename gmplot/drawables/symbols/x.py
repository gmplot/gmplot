import math

from gmplot.color import _get_hex_color
from gmplot.utility import _get_value
from gmplot.drawables.polyline import _Polyline

_EARTH_RADIUS_IN_KM = 6378.8 # TODO: Avoid duplicating this constant.

class _X(object):
    def __init__(self, lat, lng, size, **kwargs):
        '''
        Args:
            lat (float): Latitude of the center of the 'x'.
            lng (float): Longitude of the center of the 'x'.
            size (int): Size of the 'x', in meters.

        Optional:

        Args:
            color/c/edge_color/ec (str): Color of the 'x''s edge.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            alpha/edge_alpha/ea (float): Opacity of the 'x''s edge, ranging from 0 to 1. Defaults to 1.0.
            edge_width/ew (int): Width of the 'x''s edge, in pixels. Defaults to 1.
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.
        '''
        kwargs.setdefault('edge_color', _get_hex_color(_get_value(kwargs, ['color', 'c', 'edge_color', 'ec'], 'black')))
        kwargs.setdefault('edge_alpha', _get_value(kwargs, ['alpha', 'edge_alpha', 'ea'], 1.0))
        kwargs.setdefault('edge_width', _get_value(kwargs, ['edge_width', 'ew'], 1))
        kwargs.setdefault('precision', _get_value(kwargs, ['precision'], 6))

        # TODO: The following generates a 'x' in Cartesian frame rather than in lat/lng; avoid this.
        delta_lat = (size / 1000.0 / _EARTH_RADIUS_IN_KM / math.sqrt(2)) * (180.0 / math.pi)
        delta_lng = delta_lat / math.cos(math.pi * lat / 180.0)

        self._down_right_stroke = _Polyline([lat - delta_lat, lat + delta_lat], [lng + delta_lng, lng - delta_lng], **kwargs)
        self._up_right_stroke = _Polyline([lat - delta_lat, lat + delta_lat], [lng - delta_lng, lng + delta_lng], **kwargs)

    def write(self, w):
        '''
        Write the 'x'.

        Args:
            w (_Writer): Writer used to write the 'x'.
        '''
        self._down_right_stroke.write(w)
        self._up_right_stroke.write(w)       
        w.write()

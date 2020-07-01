import math

from gmplot.color import _get_hex_color
from gmplot.utility import _get_value
from gmplot.drawables.polyline import _Polyline

_EARTH_RADIUS_IN_KM = 6378.8 # TODO: Avoid duplicating this constant.

class _Plus(object):
    def __init__(self, lat, lng, size, **kwargs):
        '''
        Args:
            lat (float): Latitude of the center of the '+'.
            lng (float): Longitude of the center of the '+'.
            size (int): Size of the '+', in meters.

        Optional:

        Args:
            edge_alpha/ea (float): Opacity of the '+''s edge, ranging from 0 to 1. Defaults to 1.0.
            edge_width/ew (int): Width of the '+''s edge, in pixels. Defaults to 1.
            color/c/edge_color/ec (str): Color of the '+''s edge.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
        ''' # TODO: Pass in precision as well.
        kwargs.setdefault('edge_color', _get_hex_color(_get_value(kwargs, ['color', 'c', 'edge_color', 'ec'], '#000000')))
        kwargs.setdefault('edge_alpha', _get_value(kwargs, ['edge_alpha', 'ea'], 1.0))
        kwargs.setdefault('edge_width', _get_value(kwargs, ['edge_width', 'ew'], 1))

        # TODO: The following generates a '+' in Cartesian frame rather than in lat/lng; avoid this.
        delta_lat = (size / 1000.0 / _EARTH_RADIUS_IN_KM) * (180.0 / math.pi)
        delta_lng = delta_lat / math.cos(math.pi * lat / 180.0)

        self._horizontal_stroke = _Polyline([lat, lat], [lng - delta_lng, lng + delta_lng], **kwargs)
        self._vertical_stroke = _Polyline([lat - delta_lat, lat + delta_lat], [lng, lng], **kwargs)

    def write(self, w):
        '''
        Write the '+'.

        Args:
            w (_Writer): Writer used to write the '+'.
        '''
        self._horizontal_stroke.write(w)
        self._vertical_stroke.write(w)       
        w.write()

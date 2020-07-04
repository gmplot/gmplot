import math

from gmplot.drawables.polyline import _Polyline

_EARTH_RADIUS_IN_KM = 6378.8 # TODO: Avoid duplicating this constant.

class _X(object):
    def __init__(self, lat, lng, size, precision, **kwargs):
        '''
        Args:
            lat (float): Latitude of the center of the 'x'.
            lng (float): Longitude of the center of the 'x'.
            size (int): Size of the 'x', in meters.
            precision (int): Number of digits after the decimal to round to for lat/lng values.

        Optional:

        Args:
            color (str): Color of the 'x'. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c').
            alpha (float): Opacity of the 'x', ranging from 0 to 1.
            width (int): Width of the 'x''s edge, in pixels.
        '''
        # TODO: The following generates a 'x' in Cartesian frame rather than in lat/lng; avoid this.
        delta_lat = (size / 1000.0 / _EARTH_RADIUS_IN_KM / math.sqrt(2)) * (180.0 / math.pi)
        delta_lng = delta_lat / math.cos(math.pi * lat / 180.0)

        self._down_right_stroke = _Polyline([lat - delta_lat, lat + delta_lat], [lng + delta_lng, lng - delta_lng], precision, **kwargs)
        self._up_right_stroke = _Polyline([lat - delta_lat, lat + delta_lat], [lng - delta_lng, lng + delta_lng], precision, **kwargs)

    def write(self, w):
        '''
        Write the 'x'.

        Args:
            w (_Writer): Writer used to write the 'x'.
        '''
        self._down_right_stroke.write(w)
        self._up_right_stroke.write(w)       
        w.write()

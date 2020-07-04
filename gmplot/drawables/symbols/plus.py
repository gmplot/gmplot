import math

from gmplot.drawables.polyline import _Polyline

_EARTH_RADIUS_IN_KM = 6378.8 # TODO: Avoid duplicating this constant.

class _Plus(object):
    def __init__(self, lat, lng, size, precision, **kwargs):
        '''
        Args:
            lat (float): Latitude of the center of the '+'.
            lng (float): Longitude of the center of the '+'.
            size (int): Size of the '+', in meters.
            precision (int): Number of digits after the decimal to round to for lat/lng values.

        Optional:

        Args:
            color (str): Color of the '+'. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c').
            alpha (float): Opacity of the '+', ranging from 0 to 1.
            width (int): Width of the '+''s edge, in pixels.
        '''
        # TODO: The following generates a '+' in Cartesian frame rather than in lat/lng; avoid this.
        delta_lat = (size / 1000.0 / _EARTH_RADIUS_IN_KM) * (180.0 / math.pi)
        delta_lng = delta_lat / math.cos(math.pi * lat / 180.0)

        self._horizontal_stroke = _Polyline([lat, lat], [lng - delta_lng, lng + delta_lng], precision, **kwargs)
        self._vertical_stroke = _Polyline([lat - delta_lat, lat + delta_lat], [lng, lng], precision, **kwargs)

    def write(self, w):
        '''
        Write the '+'.

        Args:
            w (_Writer): Writer used to write the '+'.
        '''
        self._horizontal_stroke.write(w)
        self._vertical_stroke.write(w)       
        w.write()

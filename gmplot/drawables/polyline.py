from gmplot.color import _get_hex_color
from gmplot.utility import _format_LatLng

class _Polyline(object):
    def __init__(self, lats, lngs, precision, **kwargs):
        '''
        Args:
            lats ([float]): Latitudes.
            lngs ([float]): Longitudes.
            precision (int): Number of digits after the decimal to round to for lat/lng values.

        Optional:

        Args:
            color (str): Color of the polyline. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c').
            alpha (float): Opacity of the polyline, ranging from 0 to 1.
            width (int): Width of the polyline, in pixels.
        '''
        self._points = [_format_LatLng(lat, lng, precision) for lat, lng in zip(lats, lngs)]
        color = kwargs.get('color')
        self._color = _get_hex_color(color) if color is not None else None
        self._alpha = kwargs.get('alpha')
        self._width = kwargs.get('width')

    def write(self, w):
        '''
        Write the polyline.

        Args:
            w (_Writer): Writer used to write the polyline.
        '''
        w.write('new google.maps.Polyline({')
        w.indent()
        w.write('clickable: false,')
        w.write('geodesic: true,')
        if self._color is not None: w.write('strokeColor: "%s",' % self._color)
        if self._alpha is not None: w.write('strokeOpacity: %f,' % self._alpha)
        if self._width is not None: w.write('strokeWeight: %d,' % self._width)
        w.write('map: map,')
        w.write('path: [')
        w.indent()
        [w.write('%s,' % point) for point in self._points]            
        w.dedent()
        w.write(']')
        w.dedent()
        w.write('});')
        w.write()

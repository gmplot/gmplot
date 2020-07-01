from gmplot.color import _get_hex_color
from gmplot.utility import _get_value, _format_LatLng

class _Polyline(object):
    def __init__(self, lats, lngs, **kwargs):
        '''
        Args:
            lats ([float]): Latitudes.
            lngs ([float]): Longitudes.

        Optional:

        Args:
            color/c/edge_color/ec (str): Color of the polyline.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            alpha/edge_alpha/ea (float): Opacity of the polyline, ranging from 0 to 1. Defaults to 1.0.
            edge_width/ew (int): Width of the polyline, in pixels. Defaults to 1.
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.
        '''
        self._color = _get_hex_color(_get_value(kwargs, ['color', 'c', 'edge_color', 'ec'], '#000000'))
        self._edge_alpha = _get_value(kwargs, ['alpha', 'edge_alpha', 'ea'], 1.0)
        self._edge_width = _get_value(kwargs, ['edge_width', 'ew'], 1)

        precision = _get_value(kwargs, ['precision'], 6)

        self._points = [_format_LatLng(lat, lng, precision) for lat, lng in zip(lats, lngs)]

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
        w.write('strokeColor: "%s",' % self._color)
        w.write('strokeOpacity: %f,' % self._edge_alpha)
        w.write('strokeWeight: %d,' % self._edge_width)
        w.write('map: map,')
        w.write('path: [')
        w.indent()
        [w.write('%s,' % point) for point in self._points]            
        w.dedent()
        w.write(']')
        w.dedent()
        w.write('});')
        w.write()

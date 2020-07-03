from gmplot.color import _get_hex_color
from gmplot.utility import _get_value, _format_LatLng

class _Polygon(object):
    def __init__(self, lats, lngs, **kwargs):
        '''
        Args:
            lats ([float]): Latitudes.
            lngs ([float]): Longitudes.

        Optional:

        Args:
            color/c/edge_color/ec (str): Color of the polygon's edge.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            alpha/edge_alpha/ea (float): Opacity of the polygon's edge, ranging from 0 to 1. Defaults to 1.0.
            edge_width/ew (int): Width of the polygon's edge, in pixels. Defaults to 1.
            color/c/face_color/fc (str): Color of the polygon's face.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            alpha/face_alpha/fa (float): Opacity of the polygon's face, ranging from 0 to 1. Defaults to 0.3.
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.
        '''
        self._edge_color = _get_hex_color(_get_value(kwargs, ['color', 'c', 'edge_color', 'ec'], 'black'))
        self._edge_alpha = _get_value(kwargs, ['alpha', 'edge_alpha', 'ea'], 1.0)
        self._edge_width = _get_value(kwargs, ['edge_width', 'ew'], 1)
        self._face_alpha = _get_value(kwargs, ['alpha', 'face_alpha', 'fa'], 0.3)
        self._face_color = _get_hex_color(_get_value(kwargs, ['color', 'c', 'face_color', 'fc'], 'black'))

        precision = _get_value(kwargs, ['precision'], 6)

        self._points = [_format_LatLng(lat, lng, precision) for lat, lng in zip(lats, lngs)]

    def write(self, w):
        '''
        Write the polygon.

        Args:
            w (_Writer): Writer used to write the polygon.
        '''
        w.write('new google.maps.Polygon({')
        w.indent()
        w.write('clickable: false,')
        w.write('geodesic: true,')
        w.write('fillColor: "%s",' % self._face_color)
        w.write('fillOpacity: %f,' % self._face_alpha)
        w.write('strokeColor: "%s",' % self._edge_color)
        w.write('strokeOpacity: %f,' % self._edge_alpha)
        w.write('strokeWeight: %d,' % self._edge_width)
        w.write('map: map,')
        w.write('paths: [')
        w.indent()
        [w.write('%s,' % point) for point in self._points]            
        w.dedent()
        w.write(']')
        w.dedent()
        w.write('});')
        w.write()

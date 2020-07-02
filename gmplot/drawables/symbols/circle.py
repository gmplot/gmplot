from gmplot.color import _get_hex_color
from gmplot.utility import _get_value, _format_LatLng

class _Circle(object):
    def __init__(self, lat, lng, radius, **kwargs):
        '''
        Args:
            lat (float): Latitude of the center of the circle.
            lng (float): Longitude of the center of the circle.
            radius (int): Radius of the circle, in meters.

        Optional:

        Args:
            edge_alpha/ea (float): Opacity of the circle's edge, ranging from 0 to 1. Defaults to 1.0.
            edge_width/ew (int): Width of the circle's edge, in pixels. Defaults to 1.
            face_alpha/alpha (float): Opacity of the circle's face, ranging from 0 to 1. Defaults to 0.5.
            color/c/face_color/fc (str): Color of the circle's face.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            color/c/edge_color/ec (str): Color of the circle's edge.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.
        '''
        precision = _get_value(kwargs, ['precision'], 6)
        self._center = _format_LatLng(lat, lng, precision)
        self._radius = radius
        self._edge_color = _get_hex_color(_get_value(kwargs, ['color', 'c', 'edge_color', 'ec'], 'black'))
        self._edge_alpha = _get_value(kwargs, ['edge_alpha', 'ea'], 1.0)
        self._edge_width = _get_value(kwargs, ['edge_width', 'ew'], 1)
        self._face_alpha = _get_value(kwargs, ['face_alpha', 'alpha'], 0.5)
        self._face_color = _get_hex_color(_get_value(kwargs, ['color', 'c', 'face_color', 'fc'], 'black'))

    def write(self, w):
        '''
        Write the circle.

        Args:
            w (_Writer): Writer used to write the circle.
        '''
        w.write('''
            new google.maps.Circle({{
                clickable: false,
                geodesic: true,
                strokeColor: '{edge_color}',
                strokeOpacity: {edge_alpha},
                strokeWeight: {edge_width},
                fillColor: '{face_color}',
                fillOpacity: {face_alpha},
                center: {center},
                radius: {radius},
                map: map
            }});
        '''.format(
            edge_color=self._edge_color,
            edge_alpha=self._edge_alpha,
            edge_width=self._edge_width,
            face_color=self._face_color,
            face_alpha=self._face_alpha,
            center=self._center,
            radius=self._radius
        ))
        w.write()

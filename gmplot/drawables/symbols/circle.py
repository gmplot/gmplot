from gmplot.color import _get_hex_color
from gmplot.utility import _format_LatLng

class _Circle(object):
    def __init__(self, lat, lng, radius, precision, **kwargs):
        '''
        Args:
            lat (float): Latitude of the center of the circle.
            lng (float): Longitude of the center of the circle.
            radius (int): Radius of the circle, in meters.
            precision (int): Number of digits after the decimal to round to for lat/lng values.

        Optional:

        Args:
            edge_color (str): Color of the circle's edge. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c').
            edge_alpha (float): Opacity of the circle's edge, ranging from 0 to 1.
            edge_width (int): Width of the circle's edge, in pixels.
            face_color (str): Color of the circle's face. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c').
            face_alpha (float): Opacity of the circle's face, ranging from 0 to 1.
        '''
        self._center = _format_LatLng(lat, lng, precision)
        self._radius = radius

        edge_color = kwargs.get('edge_color')
        self._edge_color = _get_hex_color(edge_color) if edge_color is not None else None

        self._edge_alpha = kwargs.get('edge_alpha')
        self._edge_width = kwargs.get('edge_width')

        face_color = kwargs.get('face_color')
        self._face_color = _get_hex_color(face_color) if face_color is not None else None

        self._face_alpha = kwargs.get('face_alpha')

    def write(self, w):
        '''
        Write the circle.

        Args:
            w (_Writer): Writer used to write the circle.
        '''
        w.write('new google.maps.Circle({')
        w.indent()
        w.write('clickable: false,')
        w.write('geodesic: true,')
        if self._edge_color is not None: w.write('strokeColor: "%s",' % self._edge_color)
        if self._edge_alpha is not None: w.write('strokeOpacity: %s,' % self._edge_alpha)
        if self._edge_width is not None: w.write('strokeWeight: %s,' % self._edge_width)
        if self._face_color is not None: w.write('fillColor: "%s",' % self._face_color)
        if self._face_alpha is not None: w.write('fillOpacity: %s,' % self._face_alpha)
        w.write('center: %s,' % self._center)
        w.write('radius: %s,' % self._radius)
        w.write('map: map')
        w.dedent()
        w.write('});')
        w.write()

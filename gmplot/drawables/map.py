import json

from gmplot.utility import _INDENT_LEVEL, _get_value, _format_LatLng

class _Map(object):
    def __init__(self, lat, lng, zoom, **kwargs):
        '''
        Args:
            lat (float): Latitude of the center of the map.
            lng (float): Longitude of the center of the map.
            zoom (int): `Zoom level`_, where 0 is fully zoomed out.

        Optional:

        Args:
            map_type (str): `Map type`_.
            map_styles ([dict]): `Map styles`_. Requires `Maps JavaScript API`_.
            tilt (int): `Tilt`_ of the map upon zooming in.
            scale_control (bool): Whether or not to display the `scale control`_. Defaults to False.
            fit_bounds (dict): Fit the map to contain the given bounds, as a dict of the form
                ``{'north': float, 'south': float, 'east': float, 'west': float}``.
            precision (int): Number of digits after the decimal to round to for the lat/lng center. Defaults to 6.

        .. _Zoom level: https://developers.google.com/maps/documentation/javascript/tutorial#zoom-levels
        .. _Map type: https://developers.google.com/maps/documentation/javascript/maptypes
        .. _Map styles: https://developers.google.com/maps/documentation/javascript/style-reference
        .. _Maps JavaScript API: https://console.cloud.google.com/marketplace/details/google/maps-backend.googleapis.com
        .. _Tilt: https://developers.google.com/maps/documentation/javascript/reference/map#MapOptions.tilt
        .. _scale control: https://developers.google.com/maps/documentation/javascript/reference/map#MapOptions.scaleControl
        '''
        precision = _get_value(kwargs, ['precision'], 6)
        self._center = _format_LatLng(lat, lng, precision)
        self._zoom = zoom
        self._map_type = _get_value(kwargs, ['map_type'])
        self._map_styles = _get_value(kwargs, ['map_styles'], [])
        self._tilt = _get_value(kwargs, ['tilt'])
        self._scale_control = _get_value(kwargs, ['scale_control'], False)
        self._fit_bounds = _get_value(kwargs, ['fit_bounds'])

    def write(self, w):
        '''
        Write the map.

        Args:
            w (_Writer): Writer used to write the map.
        '''
        w.write('var map = new google.maps.Map(document.getElementById("map_canvas"), {')
        w.indent()
        if self._map_styles: w.write('styles: %s,' % json.dumps(self._map_styles, indent=_INDENT_LEVEL))
        if self._map_type: w.write('mapTypeId: "%s",' % self._map_type.lower())
        if self._tilt is not None: w.write('tilt: %d,' % self._tilt)
        if self._scale_control: w.write('scaleControl: true,')
        w.write('zoom: %d,' % self._zoom)
        w.write('center: %s' % self._center)
        w.dedent()
        w.write('});')
        w.write()
        if self._fit_bounds:
            w.write('map.fitBounds(%s);' % json.dumps(self._fit_bounds))
            w.write()

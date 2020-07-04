import json

from gmplot.utility import _INDENT_LEVEL, _format_LatLng

class _Map(object):
    def __init__(self, lat, lng, zoom, precision, **kwargs):
        '''
        Args:
            lat (float): Latitude of the center of the map.
            lng (float): Longitude of the center of the map.
            zoom (int): `Zoom level`_, where 0 is fully zoomed out.
            precision (int): Number of digits after the decimal to round to for the lat/lng center.

        Optional:

        Args:
            map_type (str): `Map type`_.
            map_styles ([dict]): `Map styles`_. Requires `Maps JavaScript API`_.
            tilt (int): `Tilt`_ of the map upon zooming in.
            scale_control (bool): Whether or not to display the `scale control`_.
            fit_bounds (dict): Fit the map to contain the given bounds, as a dict of the form
                ``{'north': float, 'south': float, 'east': float, 'west': float}``.

        .. _Zoom level: https://developers.google.com/maps/documentation/javascript/tutorial#zoom-levels
        .. _Map type: https://developers.google.com/maps/documentation/javascript/maptypes
        .. _Map styles: https://developers.google.com/maps/documentation/javascript/style-reference
        .. _Maps JavaScript API: https://console.cloud.google.com/marketplace/details/google/maps-backend.googleapis.com
        .. _Tilt: https://developers.google.com/maps/documentation/javascript/reference/map#MapOptions.tilt
        .. _scale control: https://developers.google.com/maps/documentation/javascript/reference/map#MapOptions.scaleControl
        '''
        self._center = _format_LatLng(lat, lng, precision)
        self._zoom = zoom
        self._map_type = kwargs.get('map_type')
        self._map_styles = kwargs.get('map_styles')
        self._tilt = kwargs.get('tilt')
        self._scale_control = kwargs.get('scale_control')
        self._fit_bounds = kwargs.get('fit_bounds')

    def write(self, w):
        '''
        Write the map.

        Args:
            w (_Writer): Writer used to write the map.
        '''
        w.write('var map = new google.maps.Map(document.getElementById("map_canvas"), {')
        w.indent()
        if self._map_styles: w.write('styles: %s,' % json.dumps(self._map_styles, indent=_INDENT_LEVEL))
        if self._map_type is not None: w.write('mapTypeId: "%s",' % self._map_type.lower())
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

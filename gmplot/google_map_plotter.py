from __future__ import absolute_import

import json
import requests

from collections import namedtuple

from gmplot.context import _Context
from gmplot.utility import StringIO, _get_value
from gmplot.writer import _Writer

from gmplot.drawables.grid import _Grid
from gmplot.drawables.ground_overlay import _GroundOverlay
from gmplot.drawables.heatmap import _Heatmap
from gmplot.drawables.map import _Map
from gmplot.drawables.marker_dropper import _MarkerDropper
from gmplot.drawables.marker import _Marker
from gmplot.drawables.polygon import _Polygon
from gmplot.drawables.polyline import _Polyline
from gmplot.drawables.route import _Route
from gmplot.drawables.symbol import _Symbol
from gmplot.drawables.symbols.circle import _Circle
from gmplot.drawables.text import _Text

_ArgInfo = namedtuple('ArgInfo', ['arguments', 'default'])

class InvalidSymbolError(Exception):
    pass

class GoogleAPIError(Exception):
    pass

class GoogleMapPlotter(object):
    '''
    Plotter that draws on a Google Map.
    '''

    def __init__(self, lat, lng, zoom, **kwargs):
        '''
        Args:
            lat (float): Latitude of the center of the map.
            lng (float): Longitude of the center of the map.
            zoom (int): `Zoom level`_, where 0 is fully zoomed out.

        Optional:

        Args:
            map_type (str): `Map type`_.
            apikey (str): Google Maps `API key`_.
            title (str): Title of the HTML file (as it appears in the browser tab).
            map_styles ([dict]): `Map styles`_. Requires `Maps JavaScript API`_.
            tilt (int): `Tilt`_ of the map upon zooming in.
            scale_control (bool): Whether or not to display the `scale control`_. Defaults to False.
            fit_bounds (dict): Fit the map to contain the given bounds, as a dict of the form
                ``{'north': float, 'south': float, 'east': float, 'west': float}``.
            precision (int): Number of digits after the decimal to round to for the lat/lng center. Defaults to 6.

        .. _Zoom level: https://developers.google.com/maps/documentation/javascript/tutorial#zoom-levels
        .. _Map type: https://developers.google.com/maps/documentation/javascript/maptypes
        .. _API key: https://developers.google.com/maps/documentation/javascript/get-api-key
        .. _Map styles: https://developers.google.com/maps/documentation/javascript/style-reference
        .. _Maps JavaScript API: https://console.cloud.google.com/marketplace/details/google/maps-backend.googleapis.com
        .. _Tilt: https://developers.google.com/maps/documentation/javascript/reference/map#MapOptions.tilt
        .. _scale control: https://developers.google.com/maps/documentation/javascript/reference/map#MapOptions.scaleControl

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.7670, -122.4385, 13, apikey=apikey, map_type='hybrid')
            gmap.draw("map.html")

        .. image:: GoogleMapPlotter.png

        Further customization and `styling`_::

            import gmplot

            apikey = '' # (your API key here)
            bounds = {'north': 37.967, 'south': 37.567, 'east': -122.238, 'west': -122.638}
            map_styles = [
                {
                    'featureType': 'all',
                    'stylers': [
                        {'saturation': -80},
                        {'lightness': 30},
                    ]
                }
            ]

            gmplot.GoogleMapPlotter(
                37.766956, -122.438481, 13,
                apikey=apikey,
                map_styles=map_styles,
                scale_control=True,
                fit_bounds=bounds
            ).draw("map.html")

        .. _styling: https://developers.google.com/maps/documentation/javascript/styling

        .. image:: GoogleMapPlotter_Styled.png
        '''
        self._apikey = _get_value(kwargs, ['apikey'], '', pop=True)
        self._title = _get_value(kwargs, ['title'], 'Google Maps - gmplot', pop=True)

        self._map = _Map(lat, lng, zoom, **kwargs)
        self._drawables = []
        self._markers = []
        self._marker_dropper = None

    @classmethod
    def from_geocode(cls, location, **kwargs):
        '''
        Initialize a GoogleMapPlotter object using a location string (instead of a specific lat/lng location).

        Requires `Geocoding API`_.

        Args:
            location (str): Location or address of interest, as a human-readable string.

        Optional:

        Args:
            zoom (int): `Zoom level`_, where 0 is fully zoomed out. Defaults to 13.
            map_type (str): `Map type`_.
            apikey (str): Google Maps `API key`_.
            title (str): Title of the HTML file (as it appears in the browser tab).
            map_styles ([dict]): `Map styles`_. Requires `Maps JavaScript API`_.
            tilt (int): `Tilt`_ of the map upon zooming in.
            scale_control (bool): Whether or not to display the `scale control`_. Defaults to False.
            fit_bounds (dict): Fit the map to contain the given bounds, as a dict of the form
                ``{'north': float, 'south': float, 'east': float, 'west': float}``.
            precision (int): Number of digits after the decimal to round to for the lat/lng center. Defaults to 6.

        Returns:
            :class:`GoogleMapPlotter`

        .. _Geocoding API: https://console.cloud.google.com/marketplace/details/google/geocoding-backend.googleapis.com
        .. _Zoom level: https://developers.google.com/maps/documentation/javascript/tutorial#zoom-levels
        .. _Map type: https://developers.google.com/maps/documentation/javascript/maptypes
        .. _API key: https://developers.google.com/maps/documentation/javascript/get-api-key
        .. _Map styles: https://developers.google.com/maps/documentation/javascript/style-reference
        .. _Maps JavaScript API: https://console.cloud.google.com/marketplace/details/google/maps-backend.googleapis.com
        .. _Tilt: https://developers.google.com/maps/documentation/javascript/reference/map#MapOptions.tilt
        .. _scale control: https://developers.google.com/maps/documentation/javascript/reference/map#MapOptions.scaleControl

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter.from_geocode('Chiyoda City, Tokyo', apikey=apikey)
            gmap.draw("map.html")

        .. image:: GoogleMapPlotter.from_geocode.png
        '''
        zoom = _get_value(kwargs, ['zoom'], 13, pop=True)
        apikey = _get_value(kwargs, ['apikey'], '')
        return cls(*GoogleMapPlotter.geocode(location, apikey=apikey), zoom=zoom, **kwargs)

    @staticmethod
    def geocode(location, **kwargs):
        '''
        Return the lat/lng coordinates of a location string.

        Requires `Geocoding API`_.

        Args:
            location (str): Location or address of interest, as a human-readable string.

        Optional:

        Args:
            apikey (str): Google Maps `API key`_.

        .. _Geocoding API: https://console.cloud.google.com/marketplace/details/google/geocoding-backend.googleapis.com
        .. _API key: https://developers.google.com/maps/documentation/javascript/get-api-key

        Returns:
            (float, float): Latitude/longitude coordinates of the given location string.

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            location = gmplot.GoogleMapPlotter.geocode('Versailles, France', apikey=apikey)
            print(location)

        .. code-block::

            -> (48.801408, 2.130122)
        '''
        apikey = _get_value(kwargs, ['apikey'], '')
        geocode = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address="%s"&key=%s' % (location, apikey))
        geocode = json.loads(geocode.text)
        if geocode.get('error_message', ''):
            raise GoogleAPIError(geocode['error_message'])

        latlng_dict = geocode['results'][0]['geometry']['location']
        return latlng_dict['lat'], latlng_dict['lng']

    def text(self, lat, lng, text, **kwargs):
        '''
        Write a text label.

        Args:
            lat (float): Latitude of the text label.
            lng (float): Longitude of the text label.
            text (str): Text to display.

        Optional:

        Args:
            color/c (str): Text color. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)

            gmap.text(37.793575, -122.464334, 'Presidio')
            gmap.text(37.766942, -122.441472, 'Buena Vista Park', color='blue')

            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.text.png
        '''
        self._drawables.append(_Text(lat, lng, text, **kwargs))

    def grid(self, bounds, lat_increment, lng_increment):
        '''
        Plot a grid.

        Args:
            bounds (dict): Grid bounds, as a dict of the form
                ``{'north': float, 'south': float, 'east': float, 'west': float}``.
            lat_increment (float): Distance between latitudinal divisions.
            lng_increment (float): Distance between longitudinal divisions.

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.425, -122.145, 16, apikey=apikey)
            bounds = {'north': 37.43, 'south': 37.42, 'east': -122.14, 'west': -122.15}        
            gmap.grid(bounds, 0.002, 0.0025)
            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.grid.png
        '''
        self._drawables.append(_Grid(bounds, lat_increment, lng_increment))

    def marker(self, lat, lng, **kwargs):
        '''
        Display a marker.

        Args:
            lat (float): Latitude of the marker.
            lng (float): Longitude of the marker.

        Optional:

        Args:
            color/c (str): Marker color. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to red.
            title (str): Hover-over title of the marker.
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.
            label (str): Label displayed on the marker.
            info_window (str): HTML content to be displayed in a pop-up `info window`_.
            draggable (bool): Whether or not the marker is `draggable`_. Defaults to False.

        .. _info window: https://developers.google.com/maps/documentation/javascript/infowindows
        .. _draggable: https://developers.google.com/maps/documentation/javascript/markers#draggable

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)

            gmap.marker(37.793575, -122.464334, label='H', info_window="<a href='https://www.presidio.gov/'>The Presidio</a>")
            gmap.marker(37.768442, -122.441472, color='green', title='Buena Vista Park')
            gmap.marker(37.783333, -122.439494, precision=2, color='#FFD700')

            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.marker.png
        '''
        self._markers.append(_Marker(lat, lng, **kwargs))

    def directions(self, origin, destination, **kwargs):
        '''
        Display directions from an origin to a destination.

        Requires `Directions API`_.

        Args:
            origin ((float, float)): Origin, in latitude/longitude.
            destination ((float, float)): Destination, in latitude/longitude.

        Optional:

        Args:
            travel_mode (str): `Travel mode`_. Defaults to 'DRIVING'.
            waypoints ([(float, float)]): Waypoints to pass through.
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.

        .. _Directions API: https://console.cloud.google.com/marketplace/details/google/directions-backend.googleapis.com
        .. _Travel mode: https://developers.google.com/maps/documentation/javascript/directions#TravelModes

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)

            gmap.directions(
                (37.799001, -122.442692),
                (37.832183, -122.477914),
                waypoints=[
                    (37.801036, -122.434586),
                    (37.805461, -122.437262)
                ]
            )

            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.directions.png
        '''
        self._drawables.append(_Route(origin, destination, **kwargs))

    def scatter(self, lats, lngs, **kwargs):
        '''
        Plot a collection of points.

        Args:
            lats ([float]): Latitudes.
            lngs ([float]): Longitudes.

        Optional:

        Args:
            color/c/edge_color/ec (str or [str]):
                Color of each point. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            size/s (int or [int]): Size of each point, in meters (symbols only). Defaults to 40.
            marker (bool or [bool]): True to plot points as markers, False to plot them as symbols. Defaults to True.
            symbol (str or [str]): Shape of each point, as 'o', 'x', or '+' (symbols only). Defaults to 'o'.
            title (str or [str]): Hover-over title of each point (markers only).
            label (str or [str]): Label displayed on each point (markers only).
            precision (int or [int]): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.
            alpha/face_alpha/fa (float or [float]):
                Opacity of each point's face, ranging from 0 to 1 (symbols only). Defaults to 0.3.
            alpha/edge_alpha/ea (float or [float]):
                Opacity of each point's edge, ranging from 0 to 1 (symbols only). Defaults to 1.0.
            edge_width/ew (int or [int]): Width of each point's edge, in pixels (symbols only). Defaults to 1.

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.479481, 15, apikey=apikey)

            attractions = zip(*[
                (37.769901, -122.498331),
                (37.768645, -122.475328),
                (37.771478, -122.468677),
                (37.769867, -122.466102),
                (37.767187, -122.467496),
                (37.770104, -122.470436)
            ])

            gmap.scatter(
                *attractions,
                color=['red', 'orange', 'yellow', 'green', 'blue', 'purple'],
                s=60,
                ew=2,
                marker=[True, True, False, True, False, False],
                symbol=[None, None, 'o', None, 'x', '+'],
                title=['First', 'Second', None, 'Third', None, None],
                label=['A', 'B', 'C', 'D', 'E', 'F']
            )

            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.scatter.png
        '''
        ARG_MAP = {
            'color': _ArgInfo(['color', 'c', 'edge_color', 'ec'], '#000000'),
            'size': _ArgInfo(['size', 's'], 40),
            'marker': _ArgInfo(['marker'], True),
            'symbol': _ArgInfo(['symbol'], 'o'),
            'title': _ArgInfo(['title'], None),
            'label': _ArgInfo(['label'], None),
            'precision': _ArgInfo(['precision'], 6),
            'face_alpha': _ArgInfo(['alpha', 'face_alpha', 'fa'], 0.3),
            'edge_alpha': _ArgInfo(['alpha', 'edge_alpha', 'ea'], 1.0),
            'edge_width': _ArgInfo(['edge_width', 'ew'], 1)
        }
        # This links the draw-related settings to the arguments passed into this function.
        # Note that some settings can be set through more than one argument.
        # If no arguments are passed in for a given setting, its defined default is used.

        if len(lats) != len(lngs):
            raise ValueError("Number of latitudes and longitudes don't match!")

        # For each setting...
        settings = dict()
        for setting_name, arg_info in ARG_MAP.items():

            # ...attempt to set it from kwargs (if the value isn't a list, expand it into one):
            argument_name, value = _get_value(kwargs, arg_info.arguments, arg_info.default, get_key=True)
            settings[setting_name] = value if isinstance(value, list) else [value] * len(lats)

            # ...ensure that its length matches the number of points:
            if len(settings[setting_name]) != len(lats):
                raise ValueError("`%s`'s length doesn't match the number of points!" % argument_name)

        # For each point, plot a marker or symbol with its corresponding settings:
        for i, location in enumerate(zip(lats, lngs)):
            point_settings = {setting_name: value[i] for (setting_name, value) in settings.items()}
            
            if point_settings.pop('marker'):
                self.marker(*location, **point_settings)
            else:
                shape = point_settings.pop('symbol')
                if not _Symbol.is_valid(shape):
                    raise InvalidSymbolError("Symbol '%s' is not implemented." % shape)
                self._drawables.append(_Symbol(shape, *location, size=point_settings.pop('size'), **point_settings))

    def circle(self, lat, lng, radius, **kwargs):
        '''
        Plot a circle.

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

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)

            gmap.circle(37.776956, -122.448481, 200)
            gmap.circle(37.792915, -122.427716, 400, face_alpha=0, ew=3, color='red')
            gmap.circle(37.761601, -122.415438, 600, edge_color='#ffffff', fc='b')
            gmap.circle(37.757069, -122.457245, 800, edge_alpha=0, color='#cccccc')

            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.circle.png
        '''
        self._drawables.append(_Circle(lat, lng, radius, **kwargs))

    def plot(self, lats, lngs, **kwargs):
        '''
        Plot a polyline.

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

        Usage::
            
            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)

            path = zip(*[
                (37.773097, -122.471789),
                (37.785920, -122.472693),
                (37.787815, -122.472178),
                (37.791430, -122.469763),
                (37.792547, -122.469624),
                (37.800724, -122.469460)
            ])

            gmap.plot(*path, edge_width=7, color='red')
            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.plot.png
        '''
        if len(lats) != len(lngs):
            raise ValueError("Number of latitudes and longitudes don't match!")

        self._drawables.append(_Polyline(lats, lngs, **kwargs))

    def heatmap(self, lats, lngs, **kwargs):
        '''
        Plot a heatmap.

        Args:
            lats ([float]): Latitudes.
            lngs ([float]): Longitudes.

        Optional:

        Args:
            radius (int): Radius of influence for each data point, in pixels. Defaults to 10.
            gradient ([(int, int, int, float)]): Color gradient of the heatmap, as a list of `RGBA`_ colors.
                The color order defines the gradient moving towards the center of a point.
            opacity (float): Opacity of the heatmap, ranging from 0 to 1. Defaults to 0.6.
            max_intensity (int): Maximum intensity of the heatmap. Defaults to 1.
            dissipating (bool): True to dissipate the heatmap on zooming, False to disable dissipation. Defaults to True.
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.
            weights ([float]): List of weights corresponding to each data point. Each point has a weight
                of 1 by default. Specifying a weight of N is equivalent to plotting the same point N times.
        
        .. _RGBA: https://www.w3.org/TR/css-color-3/#rgba-color

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.448481, 14, apikey=apikey)

            attractions = zip(*[
                (37.769901, -122.498331),
                (37.768645, -122.475328),
                (37.771478, -122.468677),
                (37.769867, -122.466102),
                (37.767187, -122.467496),
                (37.770104, -122.470436)
            ])

            gmap.heatmap(
                *attractions,
                radius=40,
                weights=[5, 1, 1, 1, 3, 1],
                gradient=[(0, 0, 255, 0), (0, 255, 0, 0.9), (255, 0, 0, 1)]
            )

            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.heatmap.png
        '''
        if len(lats) != len(lngs):
            raise ValueError("Number of latitudes and longitudes don't match!")

        weights = _get_value(kwargs, ['weights'])
        if weights is not None and len(weights) != len(lats):
            raise ValueError("`weights`' length doesn't match the number of points!")

        self._drawables.append(_Heatmap(lats, lngs, **kwargs))

    def ground_overlay(self, url, bounds, **kwargs):
        '''
        Overlay an image from a given URL onto the map.

        Args:
            url (str): URL of image to overlay.
            bounds (dict): Image bounds, as a dict of the form
                ``{'north': float, 'south': float, 'east': float, 'west': float}``.

        Optional:

        Args:
            opacity (float): Opacity of the overlay, ranging from 0 to 1. Defaults to 1.0.

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 12, apikey=apikey)

            url = 'http://explore.museumca.org/creeks/images/TopoSFCreeks.jpg'
            bounds = {'north': 37.832285, 'south': 37.637336, 'east': -122.346922, 'west': -122.520364}
            gmap.ground_overlay(url, bounds, opacity=0.5)

            gmap.draw("map.html")

        .. image:: GoogleMapPlotter.ground_overlay.png
        '''
        self._drawables.append(_GroundOverlay(url, bounds, **kwargs))

    def polygon(self, lats, lngs, **kwargs):
        '''
        Plot a polygon.

        Args:
            lats ([float]): Latitudes.
            lngs ([float]): Longitudes.

        Optional:

        Args:
            color/c/edge_color/ec (str): Color of the polygon's edge.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            alpha/edge_alpha/ea (float): Opacity of the polygon's edge, ranging from 0 to 1. Defaults to 1.0.
            edge_width/ew (int): Width of the polygon's edge, in pixels. Defaults to 1.
            alpha/face_alpha/fa (float): Opacity of the polygon's face, ranging from 0 to 1. Defaults to 0.3.
            color/c/face_color/fc (str): Color of the polygon's face.
                Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.448481, 14, apikey=apikey)

            golden_gate_park = zip(*[
                (37.771269, -122.511015),
                (37.773495, -122.464830),
                (37.774797, -122.454538),
                (37.771988, -122.454018),
                (37.773646, -122.440979),
                (37.772742, -122.440797),
                (37.771096, -122.453889),
                (37.768669, -122.453518),
                (37.766227, -122.460213),
                (37.764028, -122.510347)
            ])

            gmap.polygon(*golden_gate_park, face_color='pink', edge_color='cornflowerblue', edge_width=5)
            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.polygon.png
        '''
        if len(lats) != len(lngs):
            raise ValueError("Number of latitudes and longitudes don't match!")
        
        self._drawables.append(_Polygon(lats, lngs, **kwargs))

    def enable_marker_dropping(self, color, **kwargs):
        '''
        Allows markers to be dropped onto the map when clicked.

        Clicking on a dropped marker will delete it.
        
        Note: Calling this function multiple times will just overwrite the existing dropped marker settings.

        Args:
            color (str): Color of the markers to be dropped.

        Optional:

        Args:
            title (str): Hover-over title of the markers to be dropped.
            label (str): Label displayed on the markers to be dropped.
            draggable (bool): Whether or not the markers to be dropped are `draggable`_. Defaults to False.

        .. _draggable: https://developers.google.com/maps/documentation/javascript/markers#draggable

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)
            gmap.enable_marker_dropping('orange', draggable=True)
            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.enable_marker_dropping.gif
        '''
        self._marker_dropper = _MarkerDropper(color, **kwargs)

    def draw(self, file):
        '''
        Draw the HTML map to a file.

        Args:
            file (str): File to write to, as a file path.

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)
            gmap.draw('map.html')

        .. image:: GoogleMapPlotter.draw.png
        '''
        with open(file, 'w') as f:
            with _Writer(f) as w:
                self._write_html(w)

    def get(self):
        '''
        Return the HTML map as a string.

        Returns:
            str: HTML map.

        Usage::

            import gmplot
            apikey = '' # (your API key here)
            gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13, apikey=apikey)
            print(gmap.get())

        .. code-block:: html
            
            -> <html>
               <head>
               <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
               <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
               <title>Google Maps - gmplot</title>
               <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization"></script>
               <script type="text/javascript">
                   function initialize() {
                       var map = new google.maps.Map(document.getElementById("map_canvas"), {
                           zoom: 13,
                           center: new google.maps.LatLng(37.766956, -122.438481)
                       });

                   }
               </script>
               </head>
               <body style="margin:0px; padding:0px;" onload="initialize()">
                   <div id="map_canvas" style="width: 100%; height: 100%;" />
               </body>
               </html>
        '''
        with StringIO() as f:
            with _Writer(f) as w:
                self._write_html(w)
            return f.getvalue()

    def _write_html(self, w):
        '''
        Write the HTML map.

        Args:
            w (_Writer): Writer used to write the HTML map.
        '''
        context = _Context()

        w.write('''
            <html>
            <head>
            <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
            <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
            <title>{title}</title>
            <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization{key}"></script>
            <script type="text/javascript">
        '''.format(title=self._title, key=('&key=%s' % self._apikey if self._apikey else '')))
        w.indent()
        w.write('function initialize() {')
        w.indent()
        self._map.write(w)
        [drawable.write(w) for drawable in self._drawables]
        [marker.write(w, context) for marker in self._markers]
        if self._marker_dropper: self._marker_dropper.write(w, context)
        w.dedent()
        w.write('}')
        w.dedent()
        w.write('''
            </script>
            </head>
            <body style="margin:0px; padding:0px;" onload="initialize()">
                <div id="map_canvas" style="width: 100%; height: 100%;" />
            </body>
            </html>
        ''')

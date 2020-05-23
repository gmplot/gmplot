from __future__ import absolute_import

import json
import math
import os
import requests
import warnings
import base64

from collections import namedtuple, Iterable

from gmplot.color import get_hex_color_code
from gmplot.google_maps_templates import SYMBOLS, CIRCLE_MARKER
from gmplot.utility import StringIO
from gmplot.writer import _Writer

Symbol = namedtuple('Symbol', ['symbol', 'lat', 'long', 'size'])
# TODO: Rename `long` to `lng` to match the rest of the project (counts as an API change).

class InvalidSymbolError(Exception):
    pass

class GoogleAPIError(Exception):
    pass

def safe_iter(var):
    try:
        return iter(var)
    except TypeError:
        return [var]

def _format_LatLng(lat, lng, precision=6):
    return 'new google.maps.LatLng(%.*f, %.*f)' % (precision, lat, precision, lng)

class GoogleMapPlotter(object):
    _HEATMAP_DEFAULT_WEIGHT = 1

    def __init__(self, center_lat, center_lng, zoom, map_type='', apikey=''):
        # TODO: Prepend a single underscore to any attributes meant to be non-public (counts as an API change).
        self.center = (float(center_lat), float(center_lng))
        self.zoom = int(zoom)
        self.map_type = str(map_type)
        self.apikey = str(apikey)
        self.grids = None
        self.paths = []
        self.shapes = []
        self.points = []
        self.symbols = []
        self.heatmap_points = []
        self.ground_overlays = []
        self.radpoints = []
        self.gridsetting = None
        self.coloricon = os.path.join(os.path.dirname(__file__), 'markers/%s.png')
        self.title = 'Google Maps - gmplot'

    @classmethod
    def from_geocode(cls, location_string, zoom=13, apikey=''):
        lat, lng = cls.geocode(location_string, apikey)
        return cls(lat, lng, zoom, apikey)

    @classmethod
    def geocode(self, location_string, apikey=''):
        geocode = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?address="%s"&key=%s' % (location_string, apikey))
        geocode = json.loads(geocode.text)
        if geocode.get('error_message', ''):
            raise GoogleAPIError(geocode['error_message'])

        latlng_dict = geocode['results'][0]['geometry']['location']
        return latlng_dict['lat'], latlng_dict['lng']

    def grid(self, slat, elat, latin, slng, elng, lngin):
        self.gridsetting = [slat, elat, latin, slng, elng, lngin]

    def marker(self, lat, lng, color='#FF0000', c=None, title=None, precision=6):
        self.points.append((lat, lng, get_hex_color_code(c or color), title, precision))

    def scatter(self, lats, lngs, color=None, size=None, marker=True, c=None, s=None, symbol='o', **kwargs):
        """
        Plot a collection of points on the map.

        :param lats: List of latitudes.
        :param lngs: List of longitudes.
        :param color: Color of plotted points.
        :param size: Size of plotted points (doesn't affect markers). Can be a list of sizes corresponding to each point.
        :param marker: True to plot points as markers, False to plot them as symbols.
        :param c: (Same as `color`.)
        :param s: (Same as `size`.)
        :param symbol: Shape of the plotted points (doesn't affect markers).
        """
        color = color or c
        size = size or s or 40

        # If `size` is a single value, expand it into a list to match the list of points:
        if not isinstance(size, Iterable):
            size = [size] * len(lats)

        kwargs["color"] = color
        settings = self._process_kwargs(kwargs)
        
        for lat, lng, symbol_size in zip(lats, lngs, size):
            if marker:
                self.marker(lat, lng, settings['color'], precision=settings['precision'])
            else:
                self._add_symbol(Symbol(symbol, lat, lng, symbol_size), **settings)

    def _add_symbol(self, symbol, color=None, c=None, **kwargs):
        color = color or c
        kwargs.setdefault('face_alpha', 0.5)
        kwargs.setdefault('face_color', "#000000")
        kwargs.setdefault("color", color)
        settings = self._process_kwargs(kwargs)
        self.symbols.append((symbol, settings))

    def circle(self, lat, lng, radius, color=None, c=None, **kwargs):
        self._add_symbol(Symbol('o', lat, lng, radius), color, c, **kwargs)

    def _process_kwargs(self, kwargs):
        """
        Process the given kwargs into visualization settings.

        :param kwargs: Dict of keyworded arguments to be converted into visualization settings.
        :return: Processed dict of settings.
        """
        settings = dict()

        # Remove all kwargs values of None (since they'll slip through the fallback lines below):
        kwargs = {key:value for key, value in kwargs.items() if value is not None}

        settings["edge_color"] = kwargs.get("color",
                                 kwargs.get("edge_color",
                                 kwargs.get("ec", "#000000")))

        settings["edge_alpha"] = kwargs.get("alpha",
                                 kwargs.get("edge_alpha",
                                 kwargs.get("ea", 1.0)))

        settings["edge_width"] = kwargs.get("edge_width",
                                 kwargs.get("ew", 1.0))

        settings["face_alpha"] = kwargs.get("alpha",
                                 kwargs.get("face_alpha",
                                 kwargs.get("fa", 0.3)))

        settings["face_color"] = kwargs.get("color",
                                 kwargs.get("face_color",
                                 kwargs.get("fc", "#000000")))

        settings["color"] = kwargs.get("color",
                            kwargs.get("c", settings["edge_color"]))

        settings["precision"] = kwargs.get("precision", 6)

        for key, color in settings.items():
            if 'color' in key:
                settings[key] = get_hex_color_code(color)

        settings["closed"] = kwargs.get("closed", None)
        return settings

    def plot(self, lats, lngs, color=None, c=None, **kwargs):
        color = color or c
        kwargs.setdefault("color", color)
        settings = self._process_kwargs(kwargs)
        path = zip(lats, lngs)
        self.paths.append((path, settings))

    def heatmap(self, lats, lngs, threshold=None, radius=10, gradient=None, opacity=0.6, maxIntensity=1, dissipating=True, precision=6, weights=None):
        """
        Plot a heatmap.

        :param lats: List of latitudes.
        :param lngs: List of longitudes.
        :param threshold: (Deprecated; use `maxIntensity` instead.)
        :param radius: Radius of influence for each data point, in pixels.
        :param gradient: Color gradient of the heatmap, as an array of CSS color strings.
        :param opacity: Opacity of the heatmap, ranging from 0 to 1.
        :param maxIntensity: Maximum intensity of the heatmap.
        :param dissipating: True to dissipate the heatmap on zooming, False to disable dissipation.
        :param precision: Number of digits after the decimal to round to for lat/lng values.
        :param weights: List of weights corresponding to each data point.
        
        More info: https://developers.google.com/maps/documentation/javascript/reference/visualization#HeatmapLayerOptions
        """
        # Try to give anyone using threshold a heads up.
        if threshold is not None:
            warnings.warn("The 'threshold' kwarg is deprecated, replaced in favor of 'maxIntensity'.", FutureWarning)
        else:
            threshold = 10
            
        settings = {}
        settings['threshold'] = threshold
        settings['radius'] = radius
        settings['gradient'] = gradient
        settings['opacity'] = opacity
        settings['maxIntensity'] = maxIntensity
        settings['dissipating'] = dissipating

        if weights is None:
            weights = [self._HEATMAP_DEFAULT_WEIGHT] * len(lats)

        heatmap_points = []
        for lat, lng, weight in zip(lats, lngs, weights):
            heatmap_points.append((lat, lng, weight))
        self.heatmap_points.append((heatmap_points, settings, precision))

    def ground_overlay(self, url, bounds_dict, opacity=1.0):
        '''
        :param url: Url of image to overlay
        :param bounds_dict: dict of the form  {'north': , 'south': , 'west': , 'east': }
        setting the image container
        :param opacity: The opacity of the overlay, expressed as a number between 0 and 1. Optional. Defaults to 1.
        :return: None
        Example use:
        import gmplot
        gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)
        bounds_dict = {'north':37.832285, 'south': 37.637336, 'west': -122.520364, 'east': -122.346922}
        gmap.ground_overlay('http://explore.museumca.org/creeks/images/TopoSFCreeks.jpg', bounds_dict)
        gmap.draw("my_map.html")
        Google Maps API documentation
        https://developers.google.com/maps/documentation/javascript/groundoverlays#introduction
        '''

        self.ground_overlays.append((url, bounds_dict, opacity))

    def polygon(self, lats, lngs, color=None, c=None, **kwargs):
        color = color or c
        kwargs.setdefault("color", color)
        settings = self._process_kwargs(kwargs)
        shape = zip(lats, lngs)
        self.shapes.append((shape, settings))

    def draw(self, file):
        '''
        Create the HTML file (which includes one Google Map and all elements to be rendered).

        :param file: File to write to, as a file path.
        '''

        with open(file, 'w') as f:
            with _Writer(f) as w:
                self._write_html(w)

    def get(self):
        '''Return the HTML map as a string (which includes one Google Map and all elements to be rendered).'''

        with StringIO() as f:
            with _Writer(f) as w:
                self._write_html(w)
            return f.getvalue()

    #############################################
    # # # # # # Low level Map Drawing # # # # # #
    #############################################

    def _write_html(self, w):
        '''
        Write the HTML map.

        :param w: Writer used to write the HTML map.
        '''

        w.write('''
            <html>
            <head>
            <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
            <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
            <title>{title}</title>
            <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization{key}"></script>
            <script type="text/javascript">
        '''.format(title=self.title, key=('&key=%s' % self.apikey if self.apikey else '')))
        w.indent()
        w.write('function initialize() {')
        w.indent()
        self.write_map(w)
        self.write_grids(w)
        self.write_points(w)
        self.write_paths(w)
        self.write_symbols(w)
        self.write_shapes(w)
        self.write_heatmap(w)
        self.write_ground_overlay(w)
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

    # TODO: Prepend a single underscore to the following functions to make them non-public (counts as an API change).

    def write_grids(self, w):
        if self.gridsetting is None:
            return
        slat = self.gridsetting[0]
        elat = self.gridsetting[1]
        latin = self.gridsetting[2]
        slng = self.gridsetting[3]
        elng = self.gridsetting[4]
        lngin = self.gridsetting[5]
        self.grids = []

        r = [
            slat + float(x) * latin for x in range(0, int((elat - slat) / latin))]
        for lat in r:
            self.grids.append(
                [(lat + latin / 2.0, slng + lngin / 2.0), (lat + latin / 2.0, elng + lngin / 2.0)])

        r = [
            slng + float(x) * lngin for x in range(0, int((elng - slng) / lngin))]
        for lng in r:
            self.grids.append(
                [(slat + latin / 2.0, lng + lngin / 2.0), (elat + latin / 2.0, lng + lngin / 2.0)])

        for line in self.grids:
            settings = self._process_kwargs({"color": "#000000"})
            self.write_polyline(w, line, settings)

    def write_points(self, w):
        color_cache = set()
        for point in self.points:
            self.write_point(w, point[0], point[1], point[2], point[3], point[4], color_cache)

    def write_circles(self, w): # TODO: Remove since unused (counts as an API change since it's technically a public function).
        for symbol, settings in self.symbols:
            if symbol.symbol == 'o':
                self.write_symbol(w, symbol, settings)

    def write_symbols(self, w):
        for symbol, settings in self.symbols:
            self.write_symbol(w, symbol, settings)

    def write_paths(self, w):
        for path, settings in self.paths:
            self.write_polyline(w, path, settings)

    def write_shapes(self, w):
        for shape, settings in self.shapes:
            self.write_polygon(w, shape, settings)

    def write_map(self, w):
        w.write('var map = new google.maps.Map(document.getElementById("map_canvas"), {')
        w.indent()
        if self.map_type:
            w.write('mapTypeId: "%s",' % self.map_type.lower())
        w.write('zoom: %d,' % self.zoom)
        w.write('center: %s' % _format_LatLng(self.center[0], self.center[1]))
        w.dedent()
        w.write('});')
        w.write()

    def write_point(self, w, lat, lng, color, title, precision, color_cache):
        marker_name = 'marker_%s' % color[1:]

        get_marker_icon_path = lambda color: self.coloricon % color[1:]
        marker_icon_path = get_marker_icon_path(color)

        if not os.path.exists(marker_icon_path):
            warnings.warn(" Marker color '%s' isn't supported." % color)
            marker_icon_path = get_marker_icon_path('#000000')

        # If a color icon hasn't been loaded before, convert it to base64, then embed it in the script:
        if color not in color_cache:
            with open(marker_icon_path, 'rb') as f:
                base64_icon = base64.b64encode(f.read()).decode()

            w.write('var %s = new google.maps.MarkerImage("data:image/png;base64,%s");' % (marker_name, base64_icon))
            w.write()
            color_cache.add(color)

        w.write('new google.maps.Marker({')
        w.indent()
        if title is not None:
            w.write('title: "%s",' % title)
        w.write('icon: %s,' % marker_name)
        w.write('position: %s,' % _format_LatLng(lat, lng, precision))
        w.write('map: map')
        w.dedent()
        w.write('});')
        w.write()

    def write_symbol(self, w, symbol, settings):
        try:
            template = SYMBOLS[symbol.symbol]
        except KeyError:
            raise InvalidSymbolError("Symbol %s is not implemented" % symbol.symbol)

        w.write(template.format(
            lat=symbol.lat,
            long=symbol.long,
            size=symbol.size,
            strokeColor=settings.get('color', settings.get('edge_color')),
            strokeOpacity=settings.get('edge_alpha'),
            strokeWeight=settings.get('edge_width'),
            fillColor=settings.get('face_color'),
            fillOpacity=settings.get('face_alpha')
        ))
        w.write()

    def write_circle(self, w, lat, long, size, settings): # TODO: Remove since unused (counts as an API change since it's technically a public function).
        self.write_symbol(w, Symbol('o', lat, long, size), settings)

    def write_polyline(self, w, path, settings):
        w.write('new google.maps.Polyline({')
        w.indent()
        w.write('clickable: %s,' % str(False).lower())
        w.write('geodesic: %s,' % str(True).lower())
        w.write('strokeColor: "%s",' % settings.get('color', settings.get('edge_color')))
        w.write('strokeOpacity: %f,' % settings.get('edge_alpha'))
        w.write('strokeWeight: %d,' % settings.get('edge_width'))
        w.write('map: map,')
        w.write('path: [')
        w.indent()
        for coordinate in path:
            w.write('%s,' % _format_LatLng(coordinate[0], coordinate[1], settings.get("precision")))
        w.dedent()
        w.write(']')
        w.dedent()
        w.write('});')
        w.write()

    def write_polygon(self, w, path, settings):
        w.write('new google.maps.Polygon({')
        w.indent()
        w.write('clickable: %s,' % str(False).lower())
        w.write('geodesic: %s,' % str(True).lower())
        w.write('fillColor: "%s",' % settings.get('face_color', settings.get('color')))
        w.write('fillOpacity: %f,' % settings.get('face_alpha'))
        w.write('strokeColor: "%s",' % settings.get('edge_color', settings.get('color')))
        w.write('strokeOpacity: %f,' % settings.get('edge_alpha'))
        w.write('strokeWeight: %d,' % settings.get('edge_width'))
        w.write('map: map,')
        w.write('paths: [')
        w.indent()
        for coordinate in path:
            w.write('%s,' % _format_LatLng(coordinate[0], coordinate[1], settings.get("precision")))
        w.dedent()
        w.write(']')
        w.dedent()
        w.write('});')
        w.write()

    def write_heatmap(self, w):
        for heatmap_points, settings_dict, precision in self.heatmap_points:
            w.write('new google.maps.visualization.HeatmapLayer({')
            w.indent()
            w.write('threshold: %d,' % settings_dict['threshold'])
            w.write('radius: %d,' % settings_dict['radius'])
            w.write('maxIntensity: %d,' % settings_dict['maxIntensity'])
            w.write('opacity: %f,' % settings_dict['opacity'])
            w.write('dissipating: %s,' % ('true' if settings_dict['dissipating'] else 'false'))
            if settings_dict['gradient']:
                w.write('gradient: [')
                w.indent()
                for r, g, b, a in settings_dict['gradient']:
                    w.write('"rgba(%d, %d, %d, %d)",' % (r, g, b, a))
                w.dedent()
                w.write('],')
            w.write('map: map,')
            w.write('data: [')
            w.indent()
            for lat, lng, weight in heatmap_points:
                location = _format_LatLng(lat, lng, precision)
                if weight == self._HEATMAP_DEFAULT_WEIGHT:
                    w.write('%s,' % location)
                else:
                    w.write('{location: %s, weight: %f},' % (location, weight)) 
            w.dedent()
            w.write(']')
            w.dedent()
            w.write('});')
            w.write()

    def write_ground_overlay(self, w):
        for url, bounds_dict, opacity in self.ground_overlays:
            w.write('''
                new google.maps.GroundOverlay(
                    "{url}",
                    {{
            '''.format(url=url))
            w.indent().indent()
            for direction in ['north', 'south', 'east', 'west']:
                w.write('%s: %.4f,' % (direction, bounds_dict[direction]))
            w.dedent().dedent()
            w.write('''
                    }},
                    {{
                        opacity: {opacity},
                        map: map
                    }}
                );
            '''.format(opacity=opacity))
            w.write()

if __name__ == "__main__":
    apikey=''

    mymap = GoogleMapPlotter(37.428, -122.145, 16, apikey)
    # mymap = GoogleMapPlotter.from_geocode("Stanford University", apikey)

    mymap.grid(37.42, 37.43, 0.001, -122.15, -122.14, 0.001)
    mymap.marker(37.427, -122.145, "yellow")
    mymap.marker(37.428, -122.146, "cornflowerblue")
    mymap.marker(37.429, -122.144, "k")
    lat, lng = mymap.geocode("Stanford University", apikey)
    mymap.marker(lat, lng, "red")
    mymap.circle(37.429, -122.145, 100, "#FF0000", ew=2)
    path = [(37.429, 37.428, 37.427, 37.427, 37.427),
             (-122.145, -122.145, -122.145, -122.146, -122.146)]
    path2 = [[i+.01 for i in path[0]], [i+.02 for i in path[1]]]
    path3 = [(37.433302 , 37.431257 , 37.427644 , 37.430303), (-122.14488, -122.133121, -122.137799, -122.148743)]
    path4 = [(37.423074, 37.422700, 37.422410, 37.422188, 37.422274, 37.422495, 37.422962, 37.423552, 37.424387, 37.425920, 37.425937),
         (-122.150288, -122.149794, -122.148936, -122.148142, -122.146747, -122.14561, -122.144773, -122.143936, -122.142992, -122.147863, -122.145953)]
    mymap.plot(path[0], path[1], "plum", edge_width=10)
    mymap.plot(path2[0], path2[1], "red")
    mymap.polygon(path3[0], path3[1], edge_color="cyan", edge_width=5, face_color="blue", face_alpha=0.1)
    mymap.heatmap(path4[0], path4[1], threshold=10, radius=40)
    mymap.heatmap(path3[0], path3[1], threshold=10, radius=40, dissipating=False, gradient=[(30,30,30,0), (30,30,30,1), (50, 50, 50, 1)])
    mymap.scatter(path4[0], path4[1], c='r', marker=True)
    mymap.scatter(path4[0], path4[1], s=90, marker=False, alpha=0.9, symbol='x', c='red', edge_width=4)
    # Get more points with:
    # http://www.findlatitudeandlongitude.com/click-lat-lng-list/
    scatter_path = ([37.424435, 37.424417, 37.424417, 37.424554, 37.424775, 37.425099, 37.425235, 37.425082, 37.424656, 37.423957, 37.422952, 37.421759, 37.420447, 37.419135, 37.417822, 37.417209],
                    [-122.142048, -122.141275, -122.140503, -122.139688, -122.138872, -122.138078, -122.137241, -122.136405, -122.135568, -122.134731, -122.133894, -122.133057, -122.13222, -122.131383, -122.130557, -122.129999])
    mymap.scatter(scatter_path[0], scatter_path[1], c='r', marker=True)
    mymap.draw('./mymap.html')

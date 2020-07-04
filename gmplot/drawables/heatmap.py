from collections import namedtuple

from gmplot.utility import _get, _format_LatLng

class _Heatmap(object):
    _DEFAULT_WEIGHT = 1

    _Point = namedtuple('Point', ['location', 'weight'])

    def __init__(self, lats, lngs, precision, **kwargs):
        '''
        Args:
            lats ([float]): Latitudes.
            lngs ([float]): Longitudes.
            precision (int): Number of digits after the decimal to round to for lat/lng values.

        Optional:

        Args:
            radius (int): Radius of influence for each data point, in pixels.
            gradient ([(int, int, int, float)]): Color gradient of the heatmap, as a list of `RGBA`_ colors.
                The color order defines the gradient moving towards the center of a point.
            opacity (float): Opacity of the heatmap, ranging from 0 to 1.
            max_intensity (int): Maximum intensity of the heatmap.
            dissipating (bool): True to dissipate the heatmap on zooming, False to disable dissipation.
            weights ([float]): List of weights corresponding to each data point. Each point has a weight
                of 1 by default. Specifying a weight of N is equivalent to plotting the same point N times.
        
        .. _RGBA: https://www.w3.org/TR/css-color-3/#rgba-color
        '''
        weights = _get(kwargs, ['weights'], [self._DEFAULT_WEIGHT] * len(lats))
        self._points = [self._Point(_format_LatLng(lat, lng, precision), weight) for lat, lng, weight in zip(lats, lngs, weights)]
        self._radius = kwargs.get('radius')
        self._gradient = kwargs.get('gradient')
        self._opacity = kwargs.get('opacity')
        self._max_intensity = kwargs.get('max_intensity')
        self._dissipating = kwargs.get('dissipating')

    def write(self, w):
        '''
        Write the heatmap.

        Args:
            w (_Writer): Writer used to write the heatmap.
        '''
        w.write('new google.maps.visualization.HeatmapLayer({')
        w.indent()
        if self._radius is not None: w.write('radius: %d,' % self._radius)
        if self._max_intensity is not None: w.write('maxIntensity: %d,' % self._max_intensity)
        if self._opacity is not None: w.write('opacity: %f,' % self._opacity)
        if self._dissipating is False: w.write('dissipating: false,')
        if self._gradient:
            w.write('gradient: [')
            w.indent()
            for r, g, b, a in self._gradient:
                w.write('"rgba(%d, %d, %d, %f)",' % (r, g, b, a))
            w.dedent()
            w.write('],')
        w.write('map: map,')
        w.write('data: [')
        w.indent()
        for point in self._points:
            if point.weight == self._DEFAULT_WEIGHT:
                w.write('%s,' % point.location)
            else:
                w.write('{location: %s, weight: %f},' % (point.location, point.weight))
        w.dedent()
        w.write(']')
        w.dedent()
        w.write('});')
        w.write()

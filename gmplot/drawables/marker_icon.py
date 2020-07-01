import os
import warnings

from gmplot.color import _get_hex_color
from gmplot.utility import _COLOR_ICON_PATH, _get_embeddable_image

class _MarkerIcon(object):
    def __init__(self, color):
        '''
        Args:
            color (str): Color of the marker icon.
        '''
        self._color = _get_hex_color(color)
        self._name = 'marker_icon_%s' % self._color[1:]

        # Get this marker icon as an embeddable image:
        get_marker_icon_path = lambda color: _COLOR_ICON_PATH % color[1:]
        marker_icon_path = get_marker_icon_path(self._color)

        if not os.path.exists(marker_icon_path):
            warnings.warn(" Marker color '%s' isn't supported." % self._color)
            marker_icon_path = get_marker_icon_path('#000000')

        self._icon = _get_embeddable_image(marker_icon_path)

    def get_name(self):
        '''Get the name of the marker icon.'''
        return self._name
    
    def write(self, w, color_cache):
        '''
        Write the marker icon (if it isn't already written).

        Args:
            w (_Writer): Writer used to write the marker icon.
            color_cache (set): Cache of colors written so far.
        '''
        # If this marker icon hasn't been written before, then embed it in the script:
        if self._color not in color_cache:
            w.write('var %s = {' % self._name)
            w.indent()
            w.write('url: "%s",' % self._icon) 
            w.write('labelOrigin: new google.maps.Point(10, 11)') # TODO: Avoid hardcoded label origin.
            w.dedent()
            w.write('};')
            w.write()
            color_cache.add(self._color)

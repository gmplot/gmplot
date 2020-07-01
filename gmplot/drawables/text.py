from gmplot.color import _get_hex_color
from gmplot.utility import _COLOR_ICON_PATH, _get_value, _format_LatLng, _get_embeddable_image

class _Text(object):    
    def __init__(self, lat, lng, text, **kwargs):
        '''
        Args:
            lat (float): Latitude of the text label.
            lng (float): Longitude of the text label.
            text (str): Text to display.

        Optional:

        Args:
            color/c (str): Text color. Can be hex ('#00FFFF'), named ('cyan'), or matplotlib-like ('c'). Defaults to black.
        '''
        self._position = _format_LatLng(lat, lng)
        self._text = text
        self._color = _get_hex_color(_get_value(kwargs, ['color', 'c'], '#000000'))
        self._icon = _get_embeddable_image(_COLOR_ICON_PATH % 'clear')

    def write(self, w):
        '''
        Write the text.

        Args:
            w (_Writer): Writer used to write the text.
        '''
        w.write('new google.maps.Marker({')
        w.indent()
        w.write('label: {')
        w.indent()
        w.write('text: "%s",' % self._text)
        w.write('color: "%s",' % self._color)
        w.write('fontWeight: "bold"')
        w.dedent()
        w.write('},')
        w.write('icon: "%s",' % self._icon)
        w.write('position: %s,' % self._position)
        w.write('map: map')
        w.dedent()
        w.write('});')
        w.write()

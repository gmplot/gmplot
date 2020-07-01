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
            precision (int): Number of digits after the decimal to round to for lat/lng values. Defaults to 6.
        '''
        precision = _get_value(kwargs, ['precision'], 6)
        self._position = _format_LatLng(lat, lng, precision)
        self._text = text
        self._color = _get_hex_color(_get_value(kwargs, ['color', 'c'], '#000000'))
        self._icon = _get_embeddable_image(_COLOR_ICON_PATH % 'clear')

    def write(self, w):
        '''
        Write the text.

        Args:
            w (_Writer): Writer used to write the text.
        '''
        w.write('''
            new google.maps.Marker({{
                label: {{
                    text: "{text}",
                    color: "{color}",
                    fontWeight: "bold"
                }},
                icon: "{icon}",
                position: {position},
                map: map
            }});
        '''.format(
            text=self._text,
            color=self._color,
            icon=self._icon,
            position=self._position
        ))
        w.write()

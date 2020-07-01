import json

from gmplot.utility import _get_value

class _GroundOverlay(object):
    def __init__(self, url, bounds, **kwargs):
        '''
        Args:
            url (str): URL of image to overlay.
            bounds (dict): Image bounds, as a dict of the form ``{'north':, 'south':, 'east':, 'west':}``.

        Optional:

        Args:
            opacity (float): Opacity of the overlay, ranging from 0 to 1. Defaults to 1.0.
        '''
        self._url = url
        self._bounds = bounds
        self._opacity = _get_value(kwargs, ['opacity'], 1.0)

    def write(self, w):
        '''
        Write the ground overlay.

        Args:
            w (_Writer): Writer used to write the ground overlay.
        '''
        w.write('''
            new google.maps.GroundOverlay(
                "{url}",
                {bounds},
                {{
                    opacity: {opacity},
                    map: map,
                    clickable: false
                }}
            );
        '''.format(
            url=self._url,
            bounds=json.dumps(self._bounds),
            opacity=self._opacity
        ))
        w.write()

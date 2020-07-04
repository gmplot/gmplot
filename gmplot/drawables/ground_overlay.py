import json

class _GroundOverlay(object):
    def __init__(self, url, bounds, **kwargs):
        '''
        Args:
            url (str): URL of image to overlay.
            bounds (dict): Image bounds, as a dict of the form
                ``{'north': float, 'south': float, 'east': float, 'west': float}``.

        Optional:

        Args:
            opacity (float): Opacity of the overlay, ranging from 0 to 1.
        '''
        self._url = url
        self._bounds = bounds
        self._opacity = kwargs.get('opacity')

    def write(self, w):
        '''
        Write the ground overlay.

        Args:
            w (_Writer): Writer used to write the ground overlay.
        '''
        w.write('new google.maps.GroundOverlay(')
        w.indent()
        w.write('"%s",' % self._url)
        w.write('%s,' % json.dumps(self._bounds))
        w.write('{')
        w.indent()
        if self._opacity is not None: w.write('opacity: %s,' % self._opacity)
        w.write('map: map,')
        w.write('clickable: false')
        w.dedent()
        w.write('}')
        w.dedent()
        w.write(');')
        w.write()

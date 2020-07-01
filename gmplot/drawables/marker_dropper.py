from gmplot.drawables.marker_icon import _MarkerIcon
from gmplot.drawables.marker import _Marker

class _MarkerDropper(object):
    '''
    Handler that drops markers on map clicks.

    The markers can be deleted when clicked on.
    '''
    _MARKER_NAME = 'dropped_marker'
    _EVENT_OBJECT_NAME = 'event'

    def __init__(self, color, **kwargs):
        '''
        Args:
            color (str): Color of the markers to be dropped.

        Optional:

        Args:
            title (str): Hover-over title of the markers to be dropped.
            label (str): Label displayed on the markers to be dropped.
            draggable (bool): Whether or not the markers to be dropped are draggable.
        '''
        self._marker_icon = _MarkerIcon(color)
        self._marker = _Marker(
            '%s.latLng' % self._EVENT_OBJECT_NAME,
            name=self._MARKER_NAME,
            title=kwargs.get('title'),
            label=kwargs.get('label'),
            icon=self._marker_icon.name,
            draggable=kwargs.get('draggable')
        )

    def write(self, w, color_cache):
        '''
        Write the marker dropper.

        Args:
            w (_Writer): Writer used to write the marker dropper.
            color_cache (set): Cache of colors written so far.
        '''
        # Write the marker icon (if it isn't written already).
        self._marker_icon.write(w, color_cache)

        # Write the marker-dropping handler:
        w.write('map.addListener("click", function(%s) {' % self._EVENT_OBJECT_NAME)
        w.indent()
        self._marker.write(w)
        w.write('''
            {marker_name}.addListener('click', function() {{
                {marker_name}.setMap(null);
            }});
        '''.format(marker_name=self._MARKER_NAME))
        w.dedent()
        w.write('});')
        w.write()

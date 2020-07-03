from gmplot.utility import _get_value
from gmplot.drawables.marker_icon import _MarkerIcon
from gmplot.drawables.raw_marker import _RawMarker

class _MarkerDropper(object):
    '''
    Handler that drops markers on map clicks.

    The markers can be deleted when clicked on.
    '''
    _MARKER_NAME = 'dropped_marker'
    _EVENT_OBJECT_NAME = 'event'

    def __init__(self, **kwargs):
        '''
        Optional:

        Args:
            color/c (str): Color of the markers to be dropped. Can be hex ('#00FFFF'), named ('cyan'),
                or matplotlib-like ('c'). Defaults to red.
            title (str): Hover-over title of the markers to be dropped.
            label (str): Label displayed on the markers to be dropped.
            draggable (bool): Whether or not the markers to be dropped are draggable. Defaults to False.
        '''
        color = _get_hex_color(_get_value(kwargs, ['color', 'c'], 'red', pop=True))
        self._marker_icon = _MarkerIcon(color)
        self._marker = _RawMarker('%s.latLng' % self._EVENT_OBJECT_NAME, self._marker_icon.get_name(), **kwargs)

    def write(self, w, context):
        '''
        Write the marker dropper.

        Args:
            w (_Writer): Writer used to write the marker dropper.
            context (_Context): Context used to keep track of what was drawn to the map.
        '''
        # Write the marker icon (if it isn't written already):
        self._marker_icon.write(w, context)

        # Write the marker-dropping handler:
        w.write('map.addListener("click", function(%s) {' % self._EVENT_OBJECT_NAME)
        w.indent()
        self._marker.write(w, self._MARKER_NAME)
        w.write('''
            {marker_name}.addListener('click', function() {{
                {marker_name}.setMap(null);
            }});
        '''.format(marker_name=self._MARKER_NAME))
        w.dedent()
        w.write('});')
        w.write()

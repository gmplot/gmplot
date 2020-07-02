from gmplot.utility import _get_value

class _RawMarker(object):
    def __init__(self, position, icon, **kwargs):
        '''
        Args:
            position (str): JavaScript code that represents the position of the marker.
            icon (str): JavaScript code that represents the icon.

        Optional:

        Args:
            title (str): Hover-over title of the marker.
            label (str): Label displayed on the marker.
            draggable (bool): Whether or not the marker is draggable. Defaults to False.
        '''
        self._position = position
        self._icon = icon
        self._title = _get_value(kwargs, ['title'])
        self._label = _get_value(kwargs, ['label'])
        self._draggable = _get_value(kwargs, ['draggable'], False)

    def write(self, w, name=None):
        '''
        Write the raw marker.

        Args:
            w (_Writer): Writer used to write the raw marker.

        Optional:

        Args:
            name (str): JavaScript name of the marker.
        '''
        if name is not None: w.write('var %s = ' % name, end_in_newline=False)

        w.write('new google.maps.Marker({')
        w.indent()
        w.write('position: %s,' % self._position)
        w.write('icon: %s,' % self._icon)

        if self._title is not None: w.write('title: "%s",' % self._title)
        if self._label is not None: w.write('label: "%s",' % self._label)
        if self._draggable: w.write('draggable: %s,' % str(self._draggable).lower())

        w.write('map: map')
        w.dedent()
        w.write('});')
        w.write()

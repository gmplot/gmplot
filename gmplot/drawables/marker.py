class _Marker(object):
    def __init__(self, position, **kwargs):
        '''
        Args:
            position (str): JavaScript code that represents the position of the marker.

        Optional:

        Args:
            name (str): JavaScript name of the marker.
            title (str): Hover-over title of the marker.
            label (str): Label displayed on the marker.
            icon (str): JavaScript code that represents the icon.
            draggable (bool): Whether or not the marker is draggable.
        '''
        self._position = position
        self._name = kwargs.get('name')
        self._title = kwargs.get('title')
        self._label = kwargs.get('label')
        self._icon = kwargs.get('icon')
        self._draggable = kwargs.get('draggable')

    def write(self, w):
        '''
        Write the marker.

        Args:
            w (_Writer): Writer used to write the marker.
        '''
        if self._name is not None: w.write('var %s = ' % self._name, end_in_newline=False)

        w.write('new google.maps.Marker({')
        w.indent()
        w.write('position: %s,' % self._position)

        if self._title is not None: w.write('title: "%s",' % self._title)
        if self._label is not None: w.write('label: "%s",' % self._label)
        if self._icon is not None: w.write('icon: %s,' % self._icon)
        if self._draggable is not None: w.write('draggable: %s,' % str(self._draggable).lower())

        w.write('map: map')
        w.dedent()
        w.write('});')
        w.write()

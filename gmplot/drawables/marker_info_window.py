class _MarkerInfoWindow(object):
    def __init__(self, marker_name, content):
        '''
        Args:
            marker_name (str): JavaScript name of the marker that should display this info window.
            content (str): HTML content to be displayed in this info window.
        '''
        self._marker_name = marker_name
        self._content = content

    def write(self, w, info_marker_index):
        '''
        Write the info window that attaches to the given marker on click.

        Args:
            w (_Writer): Writer used to write the info window.
            info_marker_index (int): Index of this info window.
        '''
        w.write('''
            var {info_window_name} = new google.maps.InfoWindow({{
                content: '{content}'
            }});

            {marker_name}.addListener('click', function() {{
                {info_window_name}.open(map, {marker_name});
            }});
        '''.format(
            info_window_name='info_window_%d' % info_marker_index,
            marker_name=self._marker_name,
            content=self._content.replace("'", "\\'").replace("\n", "\\n") # (escape single quotes and newlines)
        ))
        w.write()

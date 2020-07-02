class _MarkerInfoWindow(object):
    def __init__(self, content):
        '''
        Args:
            content (str): HTML content to be displayed in this info window.
        '''
        self._content = content.replace("'", "\\'").replace("\n", "\\n") # (escape single quotes and newlines)

    def write(self, w, context, marker_name):
        '''
        Write the info window that attaches to the given marker on click.

        Args:
            w (_Writer): Writer used to write the info window.
            context (_Context): Context used to keep track of what was drawn to the map.
            marker_name (str): JavaScript name of the marker that should display this info window.
        '''
        w.write('''
            var {info_window_name} = new google.maps.InfoWindow({{
                content: '{content}'
            }});

            {marker_name}.addListener('click', function() {{
                {info_window_name}.open(map, {marker_name});
            }});
        '''.format(
            info_window_name='info_window_%d' % context.num_info_markers,
            marker_name=marker_name,
            content=self._content
        ))
        w.write()

class _Context(object):
    '''Context used to keep track of what was drawn to the map.'''

    def __init__(self):
        self.color_cache = set()
        '''Cache of colors written so far.'''

        self.num_info_markers = 0
        '''Number of markers with info windows written so far.'''

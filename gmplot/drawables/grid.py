import math

from gmplot.drawables.polyline import _Polyline

class _Grid(object):
    def __init__(self, bounds, lat_increment, lng_increment):
        '''
        Args:
            bounds (dict): Grid bounds, as a dict of the form
                ``{'north': float, 'south': float, 'east': float, 'west': float}``.
            lat_increment (float): Distance between latitudinal divisions.
            lng_increment (float): Distance between longitudinal divisions.
        '''
        SETTINGS = { # TODO: Allow those to be modified.
            'edge_width': 1.0,
            'color': "#000000",
            'precision': 6
        }

        # Set up the bounding box:
        self._bounding_box = _Polyline(*zip(*[
            (bounds['south'], bounds['west']),
            (bounds['north'], bounds['west']),
            (bounds['north'], bounds['east']),
            (bounds['south'], bounds['east']),
            (bounds['south'], bounds['west'])
        ]), **SETTINGS)

        get_num_divisions = lambda start, end, increment: int(math.ceil((end - start) / increment))

        # Set up the latitudinal divisions:
        self._lat_divisions = []
        for lat_index in range(1, get_num_divisions(bounds['south'], bounds['north'], lat_increment)):
            lat = bounds['south'] + float(lat_index) * lat_increment
            self._lat_divisions.append(_Polyline(*zip(*[(lat, bounds['west']), (lat, bounds['east'])]), **SETTINGS))

        # Set up the longitudinal divisions:
        self._lng_divisions = []
        for lng_index in range(1, get_num_divisions(bounds['west'], bounds['east'], lng_increment)):
            lng = bounds['west'] + float(lng_index) * lng_increment
            self._lng_divisions.append(_Polyline(*zip(*[(bounds['south'], lng), (bounds['north'], lng)]), **SETTINGS))

    def write(self, w):
        '''
        Write the grid.

        Args:
            w (_Writer): Writer used to write the grid.
        '''
        self._bounding_box.write(w)
        [lat_division.write(w) for lat_division in self._lat_divisions]
        [lng_division.write(w) for lng_division in self._lng_divisions]
        w.write()

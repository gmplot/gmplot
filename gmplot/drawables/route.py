from gmplot.utility import _get, _format_LatLng

class _Route(object):
    '''For more info, see Google Maps' `Directions Service https://developers.google.com/maps/documentation/javascript/directions`_.'''
    
    def __init__(self, origin, destination, precision, **kwargs):
        '''
        Args:
            origin ((float, float)): Origin, as a latitude/longitude tuple.
            destination ((float, float)): Destination, as a latitude/longitude tuple.
            precision (int): Number of digits after the decimal to round to for lat/lng values.

        Optional:

        Args:
            travel_mode (str): Travel mode.
            waypoints ([(float, float)]): Waypoints.
        '''
        self._origin = _format_LatLng(*origin, precision=precision)
        self._destination = _format_LatLng(*destination, precision=precision)
        self._travel_mode = kwargs.get('travel_mode')
        self._waypoints = [_format_LatLng(*waypoint, precision=precision) for waypoint in _get(kwargs, ['waypoints'], [])]

    def write(self, w):
        '''
        Write the route.

        Args:
            w (_Writer): Writer used to write the route.
        '''
        w.write('new google.maps.DirectionsService().route({')
        w.indent()
        if self._travel_mode is not None: w.write('travelMode: "%s",' % self._travel_mode.upper())
        w.write('origin: %s,' % self._origin)
        w.write('destination: %s,' % self._destination)
        if self._waypoints:
            w.write('waypoints: [')
            w.indent()
            [w.write('{location: %s, stopover: false},' % waypoint) for waypoint in self._waypoints]
            w.dedent()
            w.write(']')
        w.dedent()
        w.write('''  
            }, function(response, status) {
                if (status == google.maps.DirectionsStatus.OK) {
                    new google.maps.DirectionsRenderer({map: map}).setDirections(response);
                }
            });
        ''')
        w.write()

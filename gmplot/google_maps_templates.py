EARTH_RADIUS = 6378.8  # in KM

CIRCLE_MARKER = """\
\t\tnew google.maps.Circle({{
\t\t\tstrokeColor: '{strokeColor}',
\t\t\tstrokeOpacity: {strokeOpacity},
\t\t\tstrokeWeight: {strokeWeight},
\t\t\tfillColor: '{fillColor}',
\t\t\tfillOpacity: {fillOpacity},
\t\t\tmap: map,
\t\t\tcenter: new google.maps.LatLng({lat}, {long}),
\t\t\tradius: {size}
\t\t}});

"""

# FIXME: This generates an X marker in Cartesian frame rather than in lat/long.
X_MARKER = """\
\t\tvar lat = {lat};
\t\tvar long = {long};
\t\tvar delta = {size}/1000.0/%s/Math.sqrt(2);
\t\tvar dLat = delta * 180.0/Math.PI; 
\t\tvar dLon = delta * 180.0/Math.PI / Math.cos(Math.PI*lat/180);

\t\tnew google.maps.Polyline({{
\t\t\tpath: [
\t\t\t\tnew google.maps.LatLng(lat - dLat, long - dLon),
\t\t\t\tnew google.maps.LatLng(lat + dLat, long + dLon)
\t\t\t],
\t\t\tgeodesic: true,
\t\t\tstrokeColor: '{strokeColor}',
\t\t\tstrokeOpacity: {strokeOpacity},
\t\t\tstrokeWeight: {strokeWeight},
\t\t\tmap: map
\t\t}});

\t\tnew google.maps.Polyline({{
\t\t\tpath: [
\t\t\t\tnew google.maps.LatLng(lat - dLat, long + dLon),
\t\t\t\tnew google.maps.LatLng(lat + dLat, long - dLon)
\t\t\t],
\t\t\tgeodesic: true,
\t\t\tstrokeColor: '{strokeColor}',
\t\t\tstrokeOpacity: {strokeOpacity},
\t\t\tstrokeWeight: {strokeWeight},
\t\t\tmap: map
\t\t}});

""" % EARTH_RADIUS

# FIXME: This generates a plus marker in Cartesian frame rather than in lat/long.
PLUS_MARKER = """\
\t\tvar lat = {lat};
\t\tvar long = {long};
\t\tvar delta = {size}/1000.0/%s;
\t\tvar dLat = delta * 180.0/Math.PI; 
\t\tvar dLon = delta * 180.0/Math.PI / Math.cos(Math.PI*lat/180);

\t\tnew google.maps.Polyline({{
\t\t\tpath: [
\t\t\t\tnew google.maps.LatLng(lat, long - dLon),
\t\t\t\tnew google.maps.LatLng(lat, long + dLon)
\t\t\t],
\t\t\tgeodesic: true,
\t\t\tstrokeColor: '{strokeColor}',
\t\t\tstrokeOpacity: {strokeOpacity},
\t\t\tstrokeWeight: {strokeWeight},
\t\t\tmap: map
\t\t}});

\t\tnew google.maps.Polyline({{
\t\t\tpath: [
\t\t\t\tnew google.maps.LatLng(lat - dLat, long),
\t\t\t\tnew google.maps.LatLng(lat + dLat, long)
\t\t\t],
\t\t\tgeodesic: true,
\t\t\tstrokeColor: '{strokeColor}',
\t\t\tstrokeOpacity: {strokeOpacity},
\t\t\tstrokeWeight: {strokeWeight},
\t\t\tmap: map
\t\t}});

""" % EARTH_RADIUS

SYMBOLS = {
    'o': CIRCLE_MARKER,
    'x': X_MARKER,
    '+': PLUS_MARKER,
}

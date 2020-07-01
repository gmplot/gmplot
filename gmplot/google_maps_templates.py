# TODO: Prefix everything below with an underscore (counts as an API change).

EARTH_RADIUS = 6378.8  # in KM

CIRCLE_MARKER = """
new google.maps.Circle({{
    strokeColor: '{strokeColor}',
    strokeOpacity: {strokeOpacity},
    strokeWeight: {strokeWeight},
    fillColor: '{fillColor}',
    fillOpacity: {fillOpacity},
    map: map,
    center: new google.maps.LatLng({lat}, {lng}),
    radius: {size}
}});
""" # TODO: Set clickable=false and geodesic=true? (maybe counts as an API change?).

# TODO: Use `write_polyline()` or equivalent function below, instead of drawing polylines from scratch.

# FIXME: This generates an X marker in Cartesian frame rather than in lat/lng.
X_MARKER = """
var lat = {lat};
var lng = {lng};
var delta = {size}/1000.0/%s/Math.sqrt(2);
var dLat = delta * 180.0/Math.PI; 
var dLon = delta * 180.0/Math.PI / Math.cos(Math.PI*lat/180);

new google.maps.Polyline({{
    path: [
        new google.maps.LatLng(lat - dLat, lng - dLon),
        new google.maps.LatLng(lat + dLat, lng + dLon)
    ],
    geodesic: true,
    strokeColor: '{strokeColor}',
    strokeOpacity: {strokeOpacity},
    strokeWeight: {strokeWeight},
    map: map
}});

new google.maps.Polyline({{
    path: [
        new google.maps.LatLng(lat - dLat, lng + dLon),
        new google.maps.LatLng(lat + dLat, lng - dLon)
    ],
    geodesic: true,
    strokeColor: '{strokeColor}',
    strokeOpacity: {strokeOpacity},
    strokeWeight: {strokeWeight},
    map: map
}});
""" % EARTH_RADIUS

# FIXME: This generates a plus marker in Cartesian frame rather than in lat/lng.
PLUS_MARKER = """
var lat = {lat};
var lng = {lng};
var delta = {size}/1000.0/%s;
var dLat = delta * 180.0/Math.PI; 
var dLon = delta * 180.0/Math.PI / Math.cos(Math.PI*lat/180);

new google.maps.Polyline({{
    path: [
        new google.maps.LatLng(lat, lng - dLon),
        new google.maps.LatLng(lat, lng + dLon)
    ],
    geodesic: true,
    strokeColor: '{strokeColor}',
    strokeOpacity: {strokeOpacity},
    strokeWeight: {strokeWeight},
    map: map
}});

new google.maps.Polyline({{
    path: [
        new google.maps.LatLng(lat - dLat, lng),
        new google.maps.LatLng(lat + dLat, lng)
    ],
    geodesic: true,
    strokeColor: '{strokeColor}',
    strokeOpacity: {strokeOpacity},
    strokeWeight: {strokeWeight},
    map: map
}});
""" % EARTH_RADIUS

SYMBOLS = {
    'o': CIRCLE_MARKER,
    'x': X_MARKER,
    '+': PLUS_MARKER,
}

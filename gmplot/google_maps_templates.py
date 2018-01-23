EARTH_RADIUS = 6378.8  # in KM


CIRCLE = """
var center = new google.maps.LatLng({lat}, {long});
var radius = {size};
var circle = new google.maps.Circle({{
    strokeColor: '{strokeColor}',
    strokeOpacity: {strokeOpacity},
    strokeWeight: {strokeWeight},
    fillColor: '{fillColor}',
    fillOpacity: {fillOpacity},
    map: map,
    center: center,
    radius: radius
  }});

circle.setMap(map);

"""

# FIXME: This generate a Xmark in cartesian frame rather than in lat/long.
XMARK = """

var lat = {lat};
var long = {long};
var delta = {size}/1000.0/%s/Math.sqrt(2);
var dLat = delta * 180.0/Math.PI; 
var dLon = delta * 180.0/Math.PI / Math.cos(Math.PI*lat/180);

var coords = [
    new google.maps.LatLng(lat - dLat, long - dLon),
    new google.maps.LatLng(lat + dLat, long + dLon)
];
var linePath = new google.maps.Polyline({{
    path: coords,
    geodesic: true,
    strokeColor: '{strokeColor}',
    strokeOpacity: {strokeOpacity},
    strokeWeight: {strokeWeight},
}});
linePath.setMap(map);

var coords = [
    new google.maps.LatLng(lat - dLat, long + dLon),
    new google.maps.LatLng(lat + dLat, long - dLon)
];
var linePath = new google.maps.Polyline({{
    path: coords,
    geodesic: true,
    strokeColor: '{strokeColor}',
    strokeOpacity: {strokeOpacity},
    strokeWeight: {strokeWeight},
}});
linePath.setMap(map);

""" % EARTH_RADIUS


# FIXME: This generate a Xmark in cartesian frame rather than in lat/long.
CROSS = """

var lat = {lat};
var long = {long};
var delta = {size}/1000.0/%s;
var dLat = delta * 180.0/Math.PI; 
var dLon = delta * 180.0/Math.PI / Math.cos(Math.PI*lat/180);

var coords = [
    new google.maps.LatLng(lat, long - dLon),
    new google.maps.LatLng(lat, long + dLon)
];
var linePath = new google.maps.Polyline({{
    path: coords,
    geodesic: true,
    strokeColor: '{strokeColor}',
    strokeOpacity: {strokeOpacity},
    strokeWeight: {strokeWeight},
}});
linePath.setMap(map);

var coords = [
    new google.maps.LatLng(lat - dLat, long),
    new google.maps.LatLng(lat + dLat, long)
];
var linePath = new google.maps.Polyline({{
    path: coords,
    geodesic: true,
    strokeColor: '{strokeColor}',
    strokeOpacity: {strokeOpacity},
    strokeWeight: {strokeWeight},
}});
linePath.setMap(map);

""" % EARTH_RADIUS



SYMBOLS = {'o': CIRCLE,
           'x': XMARK,
           '+': CROSS,
}

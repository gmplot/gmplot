CIRCLE = """
var center = new google.maps.LatLng({lat}, {lon});
var radius = {radius};
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
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


MARKER = """
var position = new google.maps.LatLng({lat}, {lon});
var marker = new google.maps.Marker({{
  position: position,
  map: map,
  icon: {icon},
  title: '{title}'
}});
        
marker.setMap(map);

"""


DIAMOND_SYMBOL = """
var symbolDiamond = {{
          path: 'M -2,0 0,-3 2,0 0,3 z',
          strokeColor: '{strokeColor}',
          fillColor: '{fillColor}',
          fillOpacity: {fillOpacity}
        }};
        
"""

SYMBOLS = {'^': DIAMOND_SYMBOL,
           }



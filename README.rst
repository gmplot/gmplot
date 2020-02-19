gmplot
======

Plotting data on Google Maps, the easy way. A matplotlib-like
interface to generate the HTML and javascript to render all the
data you'd like on top of Google Maps. Several plotting methods
make creating exploratory map views effortless. Here's a crash course:

::

    from gmplot import gmplot

    # Place map
    gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)

    # Polygon
    golden_gate_park_lats, golden_gate_park_lons = zip(*[
        (37.771269, -122.511015),
        (37.773495, -122.464830),
        (37.774797, -122.454538),
        (37.771988, -122.454018),
        (37.773646, -122.440979),
        (37.772742, -122.440797),
        (37.771096, -122.453889),
        (37.768669, -122.453518),
        (37.766227, -122.460213),
        (37.764028, -122.510347),
        (37.771269, -122.511015)
        ])
    gmap.plot(golden_gate_park_lats, golden_gate_park_lons, 'cornflowerblue', edge_width=10)

    # Scatter points
    top_attraction_lats, top_attraction_lons = zip(*[
        (37.769901, -122.498331),
        (37.768645, -122.475328),
        (37.771478, -122.468677),
        (37.769867, -122.466102),
        (37.767187, -122.467496),
        (37.770104, -122.470436)
        ])
    gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=40, marker=False)

    # Marker
    hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
    gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

    mymap.marker_icon(37.430, -122.145, mymap.get_pin_icon(), "my pin")
    mymap.marker_icon(37.431, -122.146, mymap.get_icon(), "my icon")
    mymap.marker_icon(37.432, -122.147, mymap.get_icon_stack(), "my icon-stack")

    mymap.marker_icon_path(37.425, -122.140, "google.maps.SymbolPath.FORWARD_CLOSED_ARROW",
                            "FORWARD_CLOSED_ARROW", 5, 30, fill_opacity=1)
    mymap.marker_icon_path(37.426, -122.141,
       "'M 125,5 155,90 245,90 175,145 200,230 125,180 50,230 75,145 5,90 95,90 z'", "custom svg",
        1, fill_color="yellow", fill_opacity=0.8, stroke_color="gold", stroke_weight=14)

    # Draw
    gmap.draw("my_map.html")

.. image:: https://imgur.com/C6dnec8.png

Geocoding
---------

``gmplot`` contains a simple wrapper around Google's geocoding service enabling
map initilization to the location of your choice. Rather than providing latitude,
longitude, and zoom level during initialization, grab your gmplot instance with
a location:

::

    gmap = gmplot.GoogleMapPlotter.from_geocode("San Francisco")

Plot types
----------

* Polygons with fills - ``plot``
* Drop pins. - ``marker``
* Scatter points. - ``scatter``
* Grid lines. - ``grid``
* Heatmaps. - ``heatmap``

.. image:: http://i.imgur.com/dTNkbZ7.png

font-awesome
------------
For font-awesome icon support: https://mapmarker.io/documentation

Pin and Icon are using ``version 5``.

Icon Stack is using ``version 4``.

Misc.
-----

Code hosted on `GitHub <https://github.com/vgm64/gmplot>`_

Install easily with ``pip install gmplot`` from PyPI.

Inspired by Yifei Jiang's (jiangyifei@gmail.com) pygmaps_ module.

.. _pygmaps: http://code.google.com/p/pygmaps/


gmplot
======

Plotting data on Google Maps, the easy way. A matplotlib-like
interface to generate the HTML and javascript to render all the
data you'd like on top of Google Maps. Several plotting methods
make creating exploratory map views effortless. Here's a crash course:

::

    import gmplot

    gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)

    gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)
    gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
    gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
    gmap.heatmap(heat_lats, heat_lngs)

    gmap.draw("mymap.html")


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

* Polygons with fills.
* Drop pins.
* Scatter points.
* Grid lines.
* Heatmaps.

.. image:: http://i.imgur.com/dTNkbZ7.png

Misc.
-----

Code hosted on `GitHub <https://github.com/vgm64/gmplot>`_

Install easily with ``pip install gmplot`` from PyPI.

Inspired by Yifei Jiang's (jiangyifei@gmail.com) pygmaps_ module.

.. _pygmaps: http://code.google.com/p/pygmaps/


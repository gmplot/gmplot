import unittest
import gmplot
from gmplot.gmplot import _format_LatLng

class GMPlotTest(unittest.TestCase):
    def test_format_LatLng(self):
        self.assertEqual(_format_LatLng(45.123456, -80.987654), 'new google.maps.LatLng(45.123456, -80.987654)')
        self.assertEqual(_format_LatLng(45.123456, -80.987654, 4), 'new google.maps.LatLng(45.1235, -80.9877)')
        self.assertEqual(_format_LatLng(45.1, -80.9, 3), 'new google.maps.LatLng(45.100, -80.900)')

class TestMarkers(unittest.TestCase):
    def setUp(self):
        self.gmap = gmplot.GoogleMapPlotter(0, 0, 0)

    def test_marker_stores_lat_lon(self):
        self.gmap.marker(1, 11)
        self.gmap.marker(2, 22)
        self.assertEqual(1, self.gmap.points[0][0])
        self.assertEqual(11, self.gmap.points[0][1])
        self.assertEqual(2, self.gmap.points[1][0])
        self.assertEqual(22, self.gmap.points[1][1])

    def test_marker_writes(self):
        self.gmap.marker(1, 11)
        self.gmap.marker(2, 22)
        map_html = self.gmap.get()

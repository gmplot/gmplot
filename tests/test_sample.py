import unittest

import gmplot

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
        self.gmap.draw('/tmp/DEL.html')


if __name__ == '__main__':
    unittest.main()

import unittest
from gmplot.color import _get_hex_color

class ColorTest(unittest.TestCase):
    def setUp(self):
        self.longMessage = True

    def test_get_hex_color(self):
        # Test valid hex colors:
        VALID_HEX_COLORS = [
            '#000000',
            '#FFCC00',
            '#ae44BB'
        ]

        for color in VALID_HEX_COLORS:
            self.assertEqual(_get_hex_color(color), color.upper(), "'%s' should be formatted as uppercase" % color)

        # Test valid aliases of red:
        for color in ['r', 'red', '#FF0000']:
            self.assertEqual(_get_hex_color(color), '#FF0000', "'%s' should be a valid alias for 'red'" % color)

        # Test invalid colors:
        INVALID_COLORS = [
            '#FC0',
            '#GFCC00',
            '#0000000',
            '11ee22',
            'colorthatdoesntexist',
            '#abc'
        ]

        for color in INVALID_COLORS:
            with self.assertRaises(ValueError):
                _get_hex_color(color)
                self.fail("'%s' should be an invalid color" % color)

        # Test invalid types:
        INVALID_TYPES = [
            [],
            {},
            123
        ]

        for color in INVALID_TYPES:
            with self.assertRaises(TypeError):
                _get_hex_color(color)
                self.fail("'%s' should be an invalid type" % color)

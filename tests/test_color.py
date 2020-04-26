import unittest
import warnings
from gmplot.color import is_valid_hex_color, get_hex_color_code

class TestColors(unittest.TestCase):
    def test_is_valid_hex_color(self):
        self.assertTrue(is_valid_hex_color('#000000'))
        self.assertTrue(is_valid_hex_color('#FFCC00'))
        self.assertTrue(is_valid_hex_color('#ae44BB'))

        self.assertFalse(is_valid_hex_color('#FC0'))
        self.assertFalse(is_valid_hex_color('#GFCC00'))
        self.assertFalse(is_valid_hex_color('#0000000'))
        self.assertFalse(is_valid_hex_color('11ee22'))
        self.assertFalse(is_valid_hex_color('red'))
        self.assertFalse(is_valid_hex_color([]))

    def test_get_hex_color_code(self):
        self.assertEqual(get_hex_color_code('r'), '#FF0000')
        self.assertEqual(get_hex_color_code('red'), '#FF0000')
        self.assertEqual(get_hex_color_code('#FF0000'), '#FF0000')

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            self.assertEqual(get_hex_color_code('colorthatdoesntexist'), '#000000')

            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))

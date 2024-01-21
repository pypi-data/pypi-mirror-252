import unittest

from context import geo


class TestCoord(unittest.TestCase):
    def test_isclose(self):
        coord1 = geo.Coord(50, 40)
        coord2 = geo.Coord(50.4, 40.3)
        coord3 = geo.Coord(50, 43)

        self.assertTrue(coord1.isclose(coord2))
        self.assertFalse(coord1.isclose(coord3))

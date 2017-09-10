import unittest
from geodesics import great_circle, geodesic_point_buffer
from geodesics import geo_point_buffer
from geodesics import great_circle_distance, get_bounding_box, get_square_point_buffer
from geodesics import get_tissot_indicatrix, get_size_of_degree_at, get_square_point_buffer_geodesic
from geodesics import get_great_circle_from_two_points, get_great_circle_from_two_points2
from geodesics import convert_projection_extent
from cartesian import get_bounding_box_cartesian, get_line_cartesian, get_graticules
from shapely.geometry import Polygon, MultiPoint, LineString, MultiLineString, MultiPolygon
from utils import float_range_by, float_range, parse_qgis_extent


class TestGeodesics(unittest.TestCase):

    def test_parse_qgis_extents(self):
        extents = "-18683478,-15461152 : 19141536,4348463"
        tuple = parse_qgis_extent(extents)
        self.assertEqual(len(tuple), 4)
        x1, y1, x2, y2 = tuple
        self.assertEqual(x1, -18683478)
        self.assertEqual(y1, -15461152)
        self.assertEqual(x2, 19141536)
        self.assertEqual(y2, 4348463)
        extents = "30.92,29.88 : 31.41,30.13"
        tuple = parse_qgis_extent(extents)
        x1, y1, x2, y2 = tuple
        self.assertEqual(len(tuple), 4)
        self.assertEqual(x1, 30.92)
        self.assertEqual(y1, 29.88)
        self.assertEqual(x2, 31.41)
        self.assertEqual(y2, 30.13)

    def test_get_projection_extent(self):
        # mollweide, area over indian ocean and aus
        example = "+proj=moll +lon_0=0 + x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
        geom = convert_projection_extent(5456328, -2786634, 14254990, 2320744, example)
        self.assertIsInstance(geom, LineString)

    def test_get_great_cicle_two_points2(self):
        # Rapa Nui to Kheops Pyramid Great Circle
        geom = get_great_circle_from_two_points(-109.28894, -27.12201, 31.13074, 29.97594, ellipsoid='sphere')
        self.assertIsInstance(geom, MultiPoint)

    def test_get_great_cicle_two_points(self):
        geom = get_great_circle_from_two_points(-3.0, 55.97,  151.209444, -33.865)
        self.assertIsInstance(geom, MultiPoint)

    def test_get_square_buffer(self):
        geom = get_square_point_buffer(-0.088852182554, 51.5133703623, 1000.0)
        self.assertIsInstance(geom, Polygon)
        self.assertAlmostEqual(geom.area, 0.00012947400072198028)  # square degrees

    def test_get_square_buffer_geodesic(self):
        geom = get_square_point_buffer_geodesic(-0.088852182554, 51.5133703623, 1000000.0)
        self.assertIsInstance(geom, Polygon)
        self.assertAlmostEqual(geom.area, 129.52600421911623)  # square degrees

    def test_float_range_ascending(self):
        vals = list([x for x in float_range(0.0, 1.0, 100)])
        self.assertEqual(len(vals), 101)
        self.assertEqual(vals[0], 0.0)
        self.assertEqual(vals[-1], 1.0)

    def test_float_range_descending(self):
        vals = list([x for x in float_range(1.0, 0.0, 100)])
        self.assertEqual(len(vals), 101)
        self.assertEqual(vals[0], 1.0)
        self.assertEqual(vals[-1], 0.0)

    def test_float_range_unchanging(self):
        vals = list([x for x in float_range(0.0, 0.0, 100)])
        self.assertEqual(len(vals), 101)
        self.assertEqual(vals[0], 0.0)
        self.assertEqual(vals[-1], 0.0)

    def test_float_range_by_ascending(self):
        vals = list([x for x in float_range_by(0.0, 1.0, .1)])
        self.assertEqual(len(vals), 12)
        self.assertEqual(vals[0], 0.0)
        self.assertAlmostEqual(vals[1], 0.1)
        self.assertEqual(vals[-1], 1.0)

    def test_float_range_by_descending(self):
        vals = list([x for x in float_range_by(1.0, 0.0, .1)])
        self.assertEqual(len(vals), 12)
        self.assertEqual(vals[0], 1.0)
        self.assertAlmostEqual(vals[1], 0.9)
        self.assertEqual(vals[-1], 0.0)

    def test_float_range_by_unchanging(self):
        with self.assertRaises(AssertionError):
            vals = list([x for x in float_range_by(0.0, 0.0, .1)])

    def test_get_graticules(self):
        geom = get_graticules(longitude_resolution=5, latitude_resolution=5)
        self.assertIsInstance(geom, MultiLineString)

    def test_tissot_indicatrix(self):
        geom = get_tissot_indicatrix()
        self.assertIsInstance(geom, MultiPolygon)

    def test_get_bounding_box_cartesian(self):
        geom = get_bounding_box_cartesian(-180.0, -90.0, 180.0, 90.0, 10)
        self.assertIsInstance(geom, MultiLineString)
        self.assertEqual(len(geom.geoms), 4)
        self.assertEqual(len(geom.geoms[0].coords), 11)

    def test_get_line_cartesian(self):
        geom = get_line_cartesian(-52.8339407951, 48.1076136528, 77.5681609748, 8.07926741383)
        self.assertIsInstance(geom, LineString)
        self.assertEqual(len(geom.coords), 1001)

    def test_bounding_box(self):
        geom = get_bounding_box(10.0, 20.0, 45.0, 32.0)

    def test_greatcircle_distance(self):
        dist = great_circle_distance(-3.18904598892, 55.9532968753,
                                     31.130786522, 29.9759689257)
        self.assertEqual(dist, 3945700.7804510733)

    def test_great_circle_degree_lon_at_equator(self):
        dist = great_circle_distance(0.0, 0.0,
                                     1.0, 0.0)
        # see http://www.csgnetwork.com/degreelenllavcalc.html
        self.assertEqual(int(dist), 111319)

    def test_great_circle_degree_lat_at_equator(self):
        dist = great_circle_distance(0.0, 0.0,
                                     0.0, 1.0)
        # see http://www.csgnetwork.com/degreelenllavcalc.html
        self.assertEqual(int(dist), 110574)

    def test_great_circle_number_segments(self):
        geom = great_circle(-3.18904598892, 55.9532968753,
                            31.130786522, 29.9759689257,
                            1000)
        # if N segments, expect N+1 vertices
        self.assertEqual(len(geom.coords), 1001)

    def test_great_circle_geometry_types(self):
        geom = great_circle(-3.18904598892, 55.9532968753,
                            31.130786522, 29.9759689257,
                            1000,
                            Polygon)
        # if N segments, expect N+1 vertices
        self.assertIsInstance(geom, Polygon)
        geom = great_circle(-3.18904598892, 55.9532968753,
                            31.130786522, 29.9759689257,
                            1000,
                            LineString)
        # if N segments, expect N+1 vertices
        self.assertIsInstance(geom, LineString)
        geom = great_circle(-3.18904598892, 55.9532968753,
                            31.130786522, 29.9759689257,
                            1000,
                            MultiPoint)
        # if N segments, expect N+1 vertices
        self.assertIsInstance(geom, MultiPoint)

    def test_great_circle_start_end_points(self):
        geom = great_circle(-3.18904598892, 55.9532968753,
                            31.130786522, 29.9759689257,
                            1000)
        x1, y1 = geom.coords[0]
        self.assertAlmostEqual(x1, -3.18904598892)
        self.assertAlmostEqual(y1, 55.9532968753)
        xn, yn = geom.coords[-1]
        self.assertAlmostEqual(xn, 31.130786522)
        self.assertAlmostEqual(yn, 29.9759689257)

    def test_geodesic_pointbuffer_number_segments(self):
        geom = geodesic_point_buffer(-3.18907797315, 55.953326627,
                                     2000, 50000,
                                     Polygon)
        # again, expect N+1 points for N segments
        self.assertEqual(len(geom.exterior.coords), 2001)

    def test_geodesic_pointbuffer_number_segments(self):
        geom = geodesic_point_buffer(-3.18907797315, 55.953326627,
                                     2000, 500000,
                                     Polygon)
        # again, expect N+1 points for N segments
        self.assertEqual(len(geom.exterior.coords), 2001)

    def test_geo_point_buffer_number_segments(self):
        geom = geo_point_buffer(-3.18907797315, 55.953326627,
                                2000, 500000,
                                Polygon)
        # again, expect N+1 points for N segments
        self.assertIsInstance(geom, Polygon)
        self.assertEqual(len(geom.exterior.coords), 2001)

    def test_size_of_degrees(self):
        xsize, ysize = get_size_of_degree_at(0.0)
        self.assertAlmostEqual(xsize, 111319.49079327357)
        self.assertAlmostEqual(ysize, 110574.38855779878)
        xsize, ysize = get_size_of_degree_at(80.0)
        self.assertAlmostEqual(xsize, 19393.246801386882)
        self.assertAlmostEqual(ysize, 111663.20092602777)


if __name__ == '__main__':
    unittest.main()

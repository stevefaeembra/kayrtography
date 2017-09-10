from shapely.geometry import Polygon, MultiPoint, LineString, MultiLineString
from shapely.geometry import LineString, MultiPoint, MultiPolygon
from utils import float_range, float_range_by


def get_graticules(min_longitude=-180.0, max_longitude=180.0,
                   min_latitude=-90.0, max_latitude=90.0,
                   longitude_resolution=10.0,
                   latitude_resolution=10.0):
    """
    Creates graticule lines (in cartesian space)
    :param min_longitude: degrees [-180,180]
    :param max_longitude: degrees [-180,180]
    :param min_latitude: degrees [-90,90]
    :param max_latitude: degrees [-90,90]
    :param longitude_resolution: spacing of longitude lines, degrees
    :param latitude_resolution: spacing of latitude lines, degrees
    :return: 
    """
    xx = [x for x in float_range_by(min_longitude, max_longitude, longitude_resolution)]
    yy = [y for y in float_range_by(min_latitude, max_latitude, latitude_resolution)]
    lines = []
    for x in xx:
        geom = get_line_cartesian(x, min_latitude, x, max_latitude)
        lines.append(geom)
    for y in yy:
        geom = get_line_cartesian(min_longitude, y, max_longitude, y)
        lines.append(geom)
    return MultiLineString(lines)


def get_line_cartesian(longitude_start, latitude_start,
                       longitude_end, latitude_end,
                       segments=1000):
    """
    Create a densified, cartesian line between two points
    :param longitude_start: degrees [-180,180] 
    :param latitude_start: degrees [-90,90]
    :param longitude_end: degrees [-180,180]
    :param latitude_end: degrees [-90,90]
    :param segments: number of segments
    :return: geometry (LineString)
    """
    xx = [x for x in float_range(longitude_start, longitude_end, segments)]
    yy = [y for y in float_range(latitude_start, latitude_end, segments)]
    points = list(zip(xx, yy))
    return LineString(points)


def get_bounding_box_cartesian(longitude_sw, latitude_sw,
                               longitude_ne, latitude_ne,
                               segments=1000):
    """
    Create a cartesian bounding box, densified (so it will curve nicely
    when projected).
    :param longitude_sw: degrees [-180,180]
    :param latitude_sw: degrees [-90,90]
    :param longitude_ne: degrees [-180,180]
    :param latitude_ne:  degrees [-90,90]
    :param segments: number of segments
    :return: geometry (MultiLineString)
    """
    line_w = get_line_cartesian(longitude_sw, latitude_sw, longitude_sw, latitude_ne, segments)
    line_e = get_line_cartesian(longitude_ne, latitude_sw, longitude_ne, latitude_ne, segments)
    line_n = get_line_cartesian(longitude_sw, latitude_ne, longitude_ne, latitude_ne, segments)
    line_s = get_line_cartesian(longitude_sw, latitude_sw, longitude_ne, latitude_sw, segments)
    return MultiLineString([line_w, line_n, line_e, line_s])

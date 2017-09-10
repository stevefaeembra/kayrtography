import pyproj
from shapely.geometry import Polygon, MultiPoint, LineString, MultiLineString
import math
from pyproj import Geod, Proj
from shapely.geometry import LineString, MultiPoint, MultiPolygon, Point
from utils import float_range


def convert_projection_extent(x1, y1, x2, y2, proj4_string):
    """
    Use this to generate a densified outline of a projection's extent,
    converted to a WGS84 linestring. 
    Note that you may have issues if the poles or antimeridian appear 
    inside the area of interest.
    This is useful for showing the canvas extent of a projected map
    on a WGS84 basemap.
    :param x1: bottom left, in projection coords
    :param y1: 
    :param x2: top right, in projection coords
    :param y2: 
    :param proj4_string: proj4 definition of coordinate system 
    :return: LINESTRING projected to WGS84
    """
    coords = []
    wgs84_coords = []
    projector = Proj(proj4_string)
    wgs84 = pyproj.Proj("+init=EPSG:4326")
    for y in float_range(y1, y2, 1000):  # west edge
        coords.append((x1, y))
    for x in float_range(x1, x2, 1000):  # north edge
        coords.append((x, y2))
    for y in float_range(y2, y1, 1000):  # east edge
        coords.append((x2, y))
    for x in float_range(x2, x1, 1000):  # south edge
        coords.append((x, y1))
    for x, y in coords:
        try:
            x1, y1 = pyproj.transform(projector, wgs84, x, y)
            wgs84_coords.append((x1, y1))
        except RuntimeError:
            # ignore tolerance condition errors
            pass
    return LineString(wgs84_coords)


def get_great_circle_from_two_points(long_1, lat_1, long_2, lat_2, ellipsoid='WGS84'):
    """
    Get the great circle going through two points as multipoint
    note that a great circle may show a small gap at the end and
    not join up, unless you choose the ellipsoid = 'sphere' (and even then, it may
    'over-run'.)
    :param long_1: start point long
    :param lat_1: start point lat
    :param long_2: other point lon
    :param lat_2: other point lat
    :param ellipsoid: use default or 'sphere' to make it join at the ends
    :return: MULTIPOINT
    """
    # first, find the angle
    geo = Geod(ellps=ellipsoid)
    fwd, back, dist = geo.inv(long_1, lat_1, long_2, lat_2, radians=False)
    coords = []
    for dist in float_range(0.0, 40075000.0, 10000.0):
        to_lon, to_lat, to_z = geo.fwd(long_1, lat_1, fwd, dist, radians=False)
        coords.append((to_lon, to_lat))
    return MultiPoint(coords)


def get_great_circle_from_two_points2(long_1, lat_1, long_2, lat_2, ellipsoid='WGS84'):
    """
    Get the great circle going through two points as multipoint
    note that a great circle may show a small gap at the end and
    not join up, unless you choose the ellipsoid = 'sphere' (and even then, it may
    'over-run'.)
    :param long_1: start point long
    :param lat_1: start point lat
    :param long_2: other point lon
    :param lat_2: other point lat
    :param ellipsoid: use default or 'sphere' to make it join at the ends
    :return: MULTIPOINT
    """
    geo = Geod(ellps=ellipsoid)
    fwd, back, dist = geo.inv(long_1, lat_1, long_2, lat_2, radians=False)
    fwd2, back2, dist2 = geo.inv(long_2, lat_2, long_1, lat_1, radians=False)
    coords = []
    for dist in float_range(0.0, 40075000.0, 10000.0):
        to_lon, to_lat, to_z = geo.fwd(long_1, lat_1, fwd, dist, radians=False)
        coords.append((to_lon, to_lat))
        to_lon, to_lat, to_z = geo.fwd(long_2, lat_2, fwd2, dist, radians=False)
        coords.append((to_lon, to_lat))
    return MultiPoint(coords)


def get_tissot_indicatrix(min_longitude=-160, max_longitude=161,
                          min_latitude=-70, max_latitude=70,
                          segments=8,
                          radius_m=500000):
    """
    Generates tissot indicatrix
    :param min_longitude: degrees [-180,180]
    :param max_longitude: degrees [-180,180]
    :param min_latitude: degrees [-90,90]
    :param max_latitude: degrees [-90,90]
    :param segments: number of divisions (on both axes)
    :param radius_m: radius in meters
    :return: 
    """
    xx = [x for x in float_range(min_longitude, max_longitude, segments)]
    yy = [y for y in float_range(min_latitude, max_latitude, segments)]
    polys = []
    for x in xx:
        for y in yy:
            geom = geodesic_point_buffer(x, y, 100, radius_m, Polygon)
            polys.append(geom)
    return MultiPolygon(polys)


def get_bounding_box(longitude_sw, latitude_sw,
                     longitude_ne, latitude_ne,
                     segments=1000):
    """
    Create a great circle bounding box, densified (so it will curve nicely
    when projected).
    :param longitude_sw: degrees [-180,180]
    :param latitude_sw: degrees [-90,90]
    :param longitude_ne: degrees [-180,180]
    :param latitude_ne:  degrees [-90,90]
    :param segments: number of segments
    :return: geometry (MultiLineString)
    """
    line_w = great_circle(longitude_sw, latitude_sw, longitude_sw, latitude_ne, segments)
    line_e = great_circle(longitude_ne, latitude_sw, longitude_ne, latitude_ne, segments)
    line_n = great_circle(longitude_sw, latitude_ne, longitude_ne, latitude_ne, segments)
    line_s = great_circle(longitude_sw, latitude_sw, longitude_ne, latitude_sw, segments)
    return MultiLineString([line_w, line_n, line_e, line_s])


def great_circle_distance(longitude_start, latitude_start,
                          longitude_end, latitude_end):
    """
    Return great circle distance between two lat/lon 
    :param longitude_start: degrees [-180,180] 
    :param latitude_start: degrees [-90,90]
    :param longitude_end: degrees [-180,180]
    :param latitude_end: degrees [-90,90]
    :return: distance in meters
    """
    geo = Geod(ellps='WGS84')
    _, _, dist = geo.inv(longitude_start, latitude_start,
                         longitude_end, latitude_end)
    return dist


def great_circle(longitude_start, latitude_start,
                 longitude_end, latitude_end,
                 segments=100,
                 geom_type=LineString):
    """
    Generate great circle between two points with given number of
    segments. Good for plotting flight paths of planes :-)
    :param longitude_start: 
    :param latitude_start: 
    :param longitude_end: 
    :param latitude_end: 
    :param segments: number of segments
    :param geom_type: use Multipoint or LineString
    :return: WKT of great circle
    """
    geo = Geod(ellps='WGS84')
    points = []
    points.append((longitude_start, latitude_start))
    # geo.npts only includes intermediate steps
    points2 = geo.npts(lon1=longitude_start, lat1=latitude_start,
                       lon2=longitude_end, lat2=latitude_end,
                       npts=segments-1, radians=False)
    points.extend(points2)
    points.append((longitude_end, latitude_end))
    arc = geom_type(points)
    return arc


def geo_point_buffer(longitude, latitude,
                     segments, distance_m,
                     geom_type=MultiPoint,
                     wgs_84=True):
    """
    Creates a buffer in meters around a point given as long, lat in WGS84
    Works by creating an Azimuthal Equidistant projection centered 
    around the given (lon, lat) 

    :param longitude: center point longitude
    :param latitude: center point latitude
    :param segments: segments to approximate (more = smoother)
    :param distance_m: distance in meters
    :param geom_type: shapely type (e.g. Multipoint, Linestring, Polygon)
    :param wgs_84: return as WGS84, else keep azimuthal projection
    :return: geometry of requested type
    """

    spec = "+proj=aeqd +lat_0={} +lon_0={} +x_0=0 +y_0=0 +a=6371000 +b=6371000 +units=m +no_defs"
    spec = spec.format(latitude, longitude)
    custom = pyproj.Proj(spec)
    wgs84 = pyproj.Proj("+init=EPSG:4326")
    geodesic = pyproj.Geod(ellps='WGS84')
    coords = []
    xx, yy = pyproj.transform(wgs84, custom, longitude, latitude)
    for i in range(0, segments):
        angle = (2.0 * math.pi / segments) * float(i)
        x1 = xx + distance_m * math.sin(angle)
        y1 = yy + distance_m * math.cos(angle)
        x84, y84 = pyproj.transform(custom, wgs84, x1, y1)
        coords.append((x84, y84))

    ring = geom_type(coords)

    return ring


def geodesic_point_buffer(longitude, latitude,
                          segments, distance_m,
                          geom_type=MultiPoint):
    """
    Creates a buffer in meters around a point given as long, lat in WGS84
    Uses the geodesic, so should be much more accurate over larger distances

    :param longitude: center point longitude
    :param latitude: center point latitude
    :param segments: segments to approximate (more = smoother)
    :param distance_m: distance in meters
    :param geom_type: shapely type (e.g. Multipoint, Linestring, Polygon)
    :return: geometry, of requested type
    """
    geodesic = pyproj.Geod(ellps='WGS84')
    coords = []
    for i in range(0, segments):
        angle = (360.0 / segments) * float(i)
        x1, y1, z1 = geodesic.fwd(lons=longitude,
                                  lats=latitude,
                                  az=angle,
                                  dist=distance_m,
                                  radians=False)
        coords.append((x1, y1))

    ring = geom_type(coords)

    return ring


def get_square_point_buffer(longitude_centre, latitude_centre, size_m):
    """
    Create a square buffer. Done as cartesian bound box of geodesic buffer
    :param longitude_centre: 
    :param latitude_centre: 
    :param size_m: length of edge
    :return: polygon
    """
    circle = geodesic_point_buffer(longitude_centre, latitude_centre, 1000,
                                   size_m/2.0, LineString)
    min_x = min([x for x, y in circle.coords])
    min_y = min([y for x, y in circle.coords])
    max_x = max([x for x, y in circle.coords])
    max_y = max([y for x, y in circle.coords])
    return Polygon(
        [
            [min_x, min_y],
            [min_x, max_y],
            [max_x, max_y],
            [max_x, min_y],
            [min_x, min_y]
        ]
    )


def get_square_point_buffer_geodesic(longitude_centre, latitude_centre, size_m):
    """
    Create a square buffer. Edges are great circles.
    :param longitude_centre: 
    :param latitude_centre: 
    :param size_m: length of edge
    :return: polygon
    """
    circle = geodesic_point_buffer(longitude_centre, latitude_centre, 1000,
                                   size_m/2.0, LineString)
    min_x = min([x for x, y in circle.coords])
    min_y = min([y for x, y in circle.coords])
    max_x = max([x for x, y in circle.coords])
    max_y = max([y for x, y in circle.coords])
    geom_w = great_circle(min_x, min_y, min_x, max_y)
    geom_n = great_circle(min_x, max_y, max_x, max_y)
    geom_e = great_circle(max_x, max_y, max_x, min_y)
    geom_s = great_circle(max_x, min_y, min_x, min_y)
    points = []
    for x, y in geom_w.coords:
        points.append([x, y])
    for x, y in geom_n.coords:
        points.append([x, y])
    for x, y in geom_e.coords:
        points.append([x, y])
    for x, y in geom_s.coords:
        points.append([x, y])
    return Polygon(points)


def get_size_of_degree_at(latitude=0.0):
    """
    Returns the size of a degree at a given latitude (these values don't vary by longitude)
    :param latitude: 
    :return: (size degree longitude in m, size degree latitude in m)
    """
    if abs(latitude) >= 90.0:
        return (None, None)
    return (
        great_circle_distance(0.0, latitude, 1.0, latitude),
        great_circle_distance(0.0, latitude, 0.0, latitude+1)
    )

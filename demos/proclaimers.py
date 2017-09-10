"""
The Proclaimers song, "I'm gonna be (500 miles)".
Starting in Leith, Edinburgh, draw two point buffers, one at 500 miles, one at
1000 miles. Using the UK definition of Miles.
"""

from units import MI
from geodesics import geodesic_point_buffer
from shapely.geometry import MultiLineString, LineString

if __name__ == "__main__":
    x, y = -3.17011665725, 55.9764025681
    five_hundred = geodesic_point_buffer(x, y, 1000, 500.0*MI, LineString)
    five_hundred_more = geodesic_point_buffer(x, y, 1000, 1000.0*MI, LineString)
    just_to_be = MultiLineString([five_hundred, five_hundred_more])
    print(just_to_be.wkt)

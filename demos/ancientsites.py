"""
Generate a great circle passing through Easter Island and the middle
of the Pyramids of Giza. This line passes quite close to a number of
important archeological sites like Petra, Perseopolis and the Nazca lines.
"""

from geodesics import get_great_circle_from_two_points

if __name__ == "__main__":
    geom = get_great_circle_from_two_points(-109.28894, -27.12201, 31.13074, 29.97594, ellipsoid='WGS84')
    print(geom.wkt)

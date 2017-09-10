"""
Some examples of map canvas extents using various custom projections
These are converted to densified WGS84 linestrings
"""

from geodesics import convert_projection_extent
from utils import parse_qgis_extent

if __name__ == "__main__":

    # mollweide, area over indian ocean and aus
    example = "+proj=moll +lon_0=0 + x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
    geom = convert_projection_extent(5456328, -2786634, 14254990, 2320744, example)
    print(geom.wkt)

    # aeqd centered on edinburgh
    example = "+proj=aeqd +lat_0=55.9533507888 +lon_0=-3.18890398422 +units=m"
    geom = convert_projection_extent(-6262958, -6367407, 9598379, 2839657, example)
    print(geom.wkt)

    # OSGB, zoomed out to Europe
    example = "+init=EPSG:27700"
    geom = convert_projection_extent(-1828313, -1196252, 2280177, 2121200, example)
    print(geom.wkt)

    # as above, but using data pasted in from QGIS extent widget
    example = "+init=EPSG:27700"
    x1, y1, x2, y2 = parse_qgis_extent("-1828313, -1196252 : 2280177, 2121200")
    geom = convert_projection_extent(x1, y1, x2, y2, example)
    print(geom.wkt)

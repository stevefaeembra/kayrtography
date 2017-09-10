Cartographic Functions
======================

This library is a simple wrapper around the Shapely and pyProj libraries that I've developed for common cartographic use cases.

Dependencies
------------
- pyproj
- shapely

pyproj is used for geodesic calculations and projections, shapely is used to convert wgs84 coordinates into usable geometries.

Installation
------------

Installation in a virtual environment

```
pyvenv venv
. ./bin/activate
pip install -r requirements.txt
```

Features
--------
Note that in most cases, the WGS84 ellipsoid is assumed.

In **geodesics.py**

- great circle (densified) between two points
- great circle distance between two points
- great circle passing through two points and going around world
- geodesic point buffer 
  - using pyproj (tracing great circle around point)
  - using Azimuthal Equidistant projection
- square point buffer from centre (lon, lat) with given edge length
- bounding box from two WGS84 corners, using great circles
- size of degree (in meters) at given latitude
- tissot indicatrix
- convert canvas extent for arbitrary CRS to densified linestring in WGS84

In **cartesian.py**

- create graticules (densified)
- create cartesian line (densified) between two wgs84 points

In **utils.py**

- dump geometry to geojson file

In **units.py**

- some useful constants for conversion to meters

Examples
--------

See **/test/tests.py** for examples of usage.

How far can a missile reach if launched from Edinburgh if its range is 4000km?

```
geom = geodesic_point_buffer(-3.18907797315, 55.953326627, 2000, 4000000, Polygon)
print(geom.wkt)
```


What's the great circle between London Heathrow and Dubai airports?

```
geom = great_circle(-0.455, 51.471, 55.368, 25.250, 1000, LineString)
print(geom.wkt)
```

The **units.py** has various unit conversions into meters, e.g.

```
import units
# 500 nautical mile radius
geom = geodesic_point_buffer(-3.189, 55.953, 2000, 500.0 * NM, Polygon)
print(geom.wkt)
```


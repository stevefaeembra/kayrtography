"""
Utility methods
"""

import json
import re
from shapely.geometry import mapping


def float_range(start_val, end_val, steps):
    """
    Generator to produce values interpolated along a range
    :param start_val: start value
    :param end_val: end value
    :param steps: number of divisions
    :return: 
    """
    ascending = (end_val > start_val)
    if (start_val == end_val):
        for i in range(0, steps):
            yield start_val
    else:
        curr_val = start_val
        step_size = float((end_val - start_val)/steps)
        while (ascending and curr_val <= end_val) or \
              (not ascending and curr_val >= end_val):
            yield curr_val
            curr_val += step_size
    yield end_val


def float_range_by(start_val, end_val, step_size):
    """
    Generator to produce values interpolated along a range
    :param start_val: start value
    :param end_val: end value
    :param by: amount to increase/decrease by each call 
    :return: 
    """
    assert(start_val != end_val)
    ascending = (end_val > start_val)
    if not ascending and step_size > 0:
        step_size *= -1.0
    curr_val = start_val
    while (ascending and curr_val <= end_val) or \
          (not ascending and curr_val >= end_val):
        yield curr_val
        curr_val += step_size
    yield end_val


def dump_geometry_to_geojson(geometry, file_name="/tmp/foo.geojson"):
    """
    Dump geometry to a geojson file for debugging in QGIS etc.
    :param geometry:
    :param file_name: 
    :return: n/a, creates file
    """
    with open(file_name, "w") as fo:
        data = mapping(geometry)
        record = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': data
                }
            ]
        }
        fo.write(json.dumps(record, indent=4))


def parse_qgis_extent(extent_string):
    """
    takes an extent as copied from Extent Widget and parses into
    x1, y1, x2, y2 coordinates
    e.g. "-18683478,-15461152 : 19141536,4348463"
    QGIS assumes x1,y1 is bottom-left, x2,y2 is top-right
    :param extent_string: 
    :return: (x1,y1,x2,y2)
    """
    coords = []
    for val in re.finditer("([+-]?\d+([.]?\d+))", extent_string):
        v, _ = (val.groups(0))
        coords.append(float(v))
    return tuple(coords)

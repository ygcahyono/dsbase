import geohash
import math
import os
import shapely.ops as ops
import pyproj
from shapely.geometry import Polygon, MultiPolygon
from functools import partial
from datetime import datetime

class GeohashPoly(object):
    def __init__(self, hashcode):
        self.hashcode = hashcode
        self._polygon = self._create_polygon_from_hashcode(hashcode)

    def _create_polygon_from_hashcode(self, hashcode):
        box_hash = geohash.bbox(hashcode)
        s, e, w, n = box_hash['s'], box_hash['e'], box_hash['w'], box_hash['n']
        poly = Polygon([(w, s), (e, s), (e, n), (w, n)]).buffer(0)
        return poly

    def intersects(self, polygon):
        return self._polygon.intersects(polygon)

    def intersection(self, polygon):
        return self._polygon.intersection(polygon)

    @property
    def area(self):
        return get_polygon_area(self._polygon)

    @property
    def polygon(self):
        return self._polygon


def _get_neighbor(point, delta, steps=1):
    return point + (steps * delta * 2)


def _get_geohash_from_tuple(coord_tuple, precision):
    return geohash.encode(coord_tuple[0], coord_tuple[1], precision)


def _get_delta_from_geohash(hashcode):
    decoded = geohash.decode_exactly(hashcode)
    return (decoded[2] * 2, decoded[3] * 2)


def _convert_tuplelist_to_string(list_of_tuples):
    flattened = []
    for tup in list_of_tuples:
        flattened.extend(list(tup))
    flattened = ", ".join(map(str, flattened))
    return flattened


def get_neighbor_by_direction(hashcode, direction):
    if not isinstance(direction, tuple):
        raise TypeError("direction should be a tuple of form (y_step, x_step).")
    (lat, lon, lat_delta, lon_delta) = geohash.decode_exactly(hashcode)
    (lat_step, lon_step) = direction
    nlat, nlon = _get_neighbor(lat, lat_delta, lat_step), _get_neighbor(lon, lon_delta, lon_step)
    return geohash.encode(nlat, nlon, len(hashcode))


def get_neighborhood_by_corners(corner_sw, corner_ne, precision=6):
    hashcode_sw = _get_geohash_from_tuple(corner_sw, precision)
    hashcode_ne = _get_geohash_from_tuple(corner_ne, precision)
    (delta_lat, delta_lon) = _get_delta_from_geohash(hashcode_sw)
    box_sw, box_ne = geohash.bbox(hashcode_sw), geohash.bbox(hashcode_ne)
    step_lat = int(math.ceil((box_ne['s'] - box_sw['s']) / delta_lat))
    step_lon = int(math.ceil((box_ne['e'] - box_sw['e']) / delta_lon))
    dir_set = [(i, j) for i in range(step_lat + 1) for j in range(step_lon + 1)]
    hashes = [get_neighbor_by_direction(hashcode_sw, dir_element) for dir_element in dir_set]
    return hashes


def get_geohashes_by_total_bounds(total_bounds_tuple, precision=6):
    (w, s, e, n) = total_bounds_tuple
    return get_neighborhood_by_corners((s, w), (n, e), precision)


def create_geohash_polygon(hashcode):
    box_hash = geohash.bbox(hashcode)
    s, e, w, n = box_hash['s'], box_hash['e'], box_hash['w'], box_hash['n']
    return Polygon([(w, s), (e, s), (e, n), (w, n)])


def create_neighborhood_polygon(hashcode_list):
    if not isinstance(hashcode_list, list):
        raise TypeError("should pass in a list of geohashes.")
    return ops.cascaded_union([create_geohash_polygon(home) for home in hashcode_list])


def get_polygon_area(polygon, sqkm=True):
    if polygon.is_empty:
        return 0.0
    geom_area = ops.transform(partial(
        pyproj.transform,
        pyproj.Proj(init='EPSG:4326'),
        pyproj.Proj(
            proj='aea',
            lat1=polygon.bounds[1],
            lat2=polygon.bounds[3]
        )
    ), polygon)
    area = geom_area.area
    if sqkm:
        area /= 1000000
    return area


def get_intersecting_geohashes_from_polygon(polygon_coords, precision = 6):
    polygon_bounds = polygon_coords.total_bounds
    polygon_values = polygon_coords.values[0]
    if polygon_coords.geom_type.values[0] == 'Polygon':
        polygon = Polygon(polygon_values)
    elif polygon_coords.geom_type.values[0] == 'MultiPolygon':
        polygon = MultiPolygon(polygon_values)
    base_geohashes = get_geohashes_by_total_bounds(polygon_bounds, precision)
    geohashpolys = [GeohashPoly(hashcode) for hashcode in base_geohashes]
    intersecting_geohashes = [gp.hashcode for gp in geohashpolys if gp.intersects(polygon)]
    return intersecting_geohashes


def collapse_and_reverse_assignment(ddict):
    if not isinstance(ddict, dict):
        raise TypeError("Doh! Should be dict, you dicthead.")
    rev_dict = {}
    for hashcode, areas in ddict.items():
        area = areas[0]
        if area not in rev_dict:
            rev_dict[area] = []
        rev_dict[area].append(hashcode)
    return rev_dict

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def innerList(In):
    
    if len(In)%2 != 0:
        raise ValueError('Please input even list')
        
    else:
        outerList = []
        for x in chunks(In,2):
            outerList.append(x)
            
    return outerList

def createGeoJson(outerList, geohashName = 'DEFAULT', cityCode = 'JKT', cityID = 10, code = 'PULAUSERIBU', \
                  countryCode = 'ID', updatedAt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%m:%S')):

    geojson = """
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        """+str(outerList)+"""
                    ]
                },
                "properties": {
                    "name": \""""+str(geohashName)+"""\",
                    "areaType": "Default",
                    "cityCode": 'Default',
                    "cityID": 'Default',
                    "code": 'Default',
                    "countryCode": "ID",
                    "countryID": "6",
                    "description": "",
                    "message": "",
                    "messageDisplay": "false",
                    "updatedAt": \""""+str(updatedAt)+"""\",
                    "version": "1"
                }
            }
        ]
    }
    """
    
    return geojson

# if __name__ == '__main__':
#     pass

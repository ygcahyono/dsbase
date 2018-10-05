import geopandas as gpd
import pandas as pd
import os
import subprocess

from queryGrab import geoHelper
from shapely.geometry import Polygon, MultiPolygon

# def convert_geojson_to_geohash(filepath, precision = 6, columns_to_keep=None, city_id=None, country_id=None, city_name=None):
# def directory_n_name(filepath):
#     filepath_noext = os.path.splitext(os.path.abspath(filepath))[0]
#     loc = filepath_noext.rfind('/')
#     name = filepath_noext[loc+1:]
#     return name

def to_geohash(name, is_neighbour = False, precision = 6, columns_to_keep=None, city_id=None, country_id=None, city_name=None):
    '''
        this function is basically creating geohash file by inputing geojson file.
        you can put is_neighbour = True if you want to create geohash file contain broader areas around the 
        defined geofences.

        ps: some os this codes is reused function from convert_geojson_to_geohash credits to: jerome.montino@grabtaxi.com
        the addtition is aimed to can convert the lists of polygon directly to geohash csv file.
    '''
    
    gdf = gpd.read_file(os.getcwd() +'/'+ name + '.geojson')
    if not columns_to_keep is None:
        gdf = gdf[columns_to_keep]
        gdf.columns = ['name', 'geometry']
    if 'name' not in gdf.columns:
        gdf['name'] = city_name 
    areas = gdf['name'].unique().tolist() 

    hashtuples = []
    for area in areas:
        geom = gdf.loc[gdf['name'] == area, :]['geometry']
        hashcodes = geoHelper.get_intersecting_geohashes_from_polygon(geom, precision = precision)
        if geom.geom_type.values[0] == 'Polygon':
            areapoly = Polygon(geom.values[0])
        elif geom.geom_type.values[0] == 'MultiPolygon':
            areapoly = MultiPolygon(geom.values[0])
        areapoly = areapoly.buffer(0)
        for hashcode in hashcodes:
            geohashpoly = geoHelper.GeohashPoly(hashcode)
            overlap = geohashpoly.intersection(areapoly)
            oarea = geoHelper.get_polygon_area(overlap)
            hashtuples.append((area, hashcode, oarea))

    df = pd.DataFrame(hashtuples, columns=['area', 'geohash', 'size'])
    primary_max = df.sort_values(by='size', ascending=False).drop_duplicates('geohash')
    secondary_max = df.sort_values(by='size', ascending=False).drop_duplicates('area')
    removed = secondary_max.loc[~secondary_max['area'].isin(primary_max['area'].unique().tolist()), :]
    primary_max = primary_max.loc[~primary_max['geohash'].isin(removed['geohash'].unique().tolist()), :]
    xdf = pd.concat([primary_max, removed])
    xdf['city_id'] = city_id
    xdf['country_id'] = country_id
    xdf['city_name'] = city_name
    xdf = xdf[['geohash', 'city_id', 'country_id', 'city_name']]

    export_path = os.path.abspath(os.getcwd() +'/'+ name + '_geohash.csv')
    xdf.to_csv(export_path, index=False)

    if is_neighbour:

        neighborhood_poly = []
        for area in xdf['area'].unique().tolist():
            hashcodes = xdf.loc[xdf['area'] == area]['geohash'].tolist()
            area_poly = geoHelper.create_neighborhood_polygon(hashcodes)
            neighborhood_poly.append((area, area_poly))

        new_gdf = gpd.GeoDataFrame(neighborhood_poly, columns=['name', 'geometry'])

        export_path = os.path.abspath(os.getcwd() +'/'+ name + '_neighborhood-geohash.geojson')
        with open(export_path, 'w') as f:
            f.write(new_gdf.to_json())


def convert_polygon_to_geohash(lists, name = 'geohashFile', precision = 6, columns_to_keep=None, city_id=None, country_id=None, city_name=None):
    ''' this function sum up all the process by converting list of pair geofences to geojson and creating geohash csv file '''

    innerList = geoHelper.innerList(lists)
    f = open(name +".geojson","w+")
    f.write(geoHelper.createGeoJson(innerList, geohashName= city_name))
    f.close()
    to_geohash(name = name, precision = precision, columns_to_keep=columns_to_keep, city_id=city_id, country_id=country_id, city_name=city_name)
    os.remove(os.getcwd() +'/'+ name + '.geojson')










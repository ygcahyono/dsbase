from .Presto import queryPr, pushPr
from .geoConverter import convert_polygon_to_geohash
from .GoogleSheets import readGs, writeGs, shareGs, createGs, deleteGs

__version__ = '1.4.0'

def sample(N,e):
	from math import ceil
	return int(ceil(N*1.0/(1+N*e*e)))
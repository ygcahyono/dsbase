from .Presto import queryPr, pushPr
from .geoConverter import convert_polygon_to_geohash, to_geohash
from .GoogleSheets import readGs, writeGs, shareGs, createGs, deleteGs, createFolder, moveFile

__version__ = '2.1.4'

def sample(N,e):
	from math import ceil
	return int(ceil(N*1.0/(1+N*e*e)))


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
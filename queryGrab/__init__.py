"""{{ cookiecutter.package_name }} - {{ cookiecutter.package_description }}"""

from .Presto import queryPr, pushPr
from .geoConverter import convert_polygon_to_geohash
from .GoogleSheets import readGs

__version__ = '1.2.0'

def sample(N,e):
	from math import ceil
	return int(ceil(N*1.0/(1+N*e*e)))
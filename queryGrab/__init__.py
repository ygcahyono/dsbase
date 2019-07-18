from multiprocessing import cpu_count
from .Presto import queryPr, pushPr
from .geoConverter import convert_polygon_to_geohash, to_geohash
from .GoogleSheets import readGs, writeGs, shareGs, createGs, deleteGs, createFolder, moveFile
import pandas as pd

__version__ = '2.2.1'

def sample(N,e):
	from math import ceil
	return int(ceil(N*1.0/(1+N*e*e)))


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def parallelize(data, func, num_of_processes=cpu_count()):
    import numpy as np
    from multiprocessing import Pool

    data_split = np.array_split(data, num_of_processes)
    pool = Pool(num_of_processes)
    data = pd.concat(pool.map(func, data_split))
    pool.close()
    pool.join()

    return data

def run_on_subset(func, data_subset):
    return data_subset.apply(func, axis=1)

def parallelize_on_rows(data, func, num_of_processes=cpu_count()):
    '''
    how to parallelize on rows?
    
    '''
    from functools import partial
    return parallelize(data, partial(run_on_subset, func), num_of_processes)
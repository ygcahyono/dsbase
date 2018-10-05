import pandas as pd
import time

from pydatagateway import datagateway
from datetime import datetime
from .credentials import configPr


def conPr(verbose=1, depth = 0):

	if depth>9:
		raise ValueError('already reach maximum connection trying')

	if verbose:
		print('trying to connect')

	try:
		config = configPr['adhoc']

		if verbose:
			print('connected')

		konPr = datagateway.connect(**config).cursor()

		return konPr

	except:

		if verbose:
			print('not connected')
			print('sleeping for 3 seconds')
			print('------------------')

		time.sleep(3)
		return conPr(verbose=verbose, depth=depth+1)


def queryPr(query, verbose = 1):

	konPr = conPr(verbose= verbose)

	if verbose:
	    print('executing query!')
	    start = datetime.now()

	konPr.execute(query)

	df = pd.DataFrame(konPr.fetchall(),columns = [c[0] for c in konPr.description])

	if verbose:
	    print('dataframe is done in '+str(datetime.now()-start))

	return df
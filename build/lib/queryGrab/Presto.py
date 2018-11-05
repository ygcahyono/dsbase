import pandas as pd
import time
from pyhive import presto
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

		konPr = presto.connect(**config).cursor()

		return konPr

	except:

		if verbose:
			print('not connected')
			print('sleeping for 3 seconds')
			print('------------------')

		time.sleep(3)
		return conPr(verbose=verbose, depth=depth+1)


def queryPr(query, verbose = 1):
	''' 
	this function is used to gather data from presto database and return it into pandas variable.
	'''


	konPr = conPr(verbose= verbose)

	if verbose:
	    print('executing query!')
	    start = datetime.now()

	konPr.execute(query)

	df = pd.DataFrame(konPr.fetchall(),columns = [c[0] for c in konPr.description])

	if verbose:
	    print('dataframe is done in '+str(datetime.now()-start))

	return df

def pushPr(query, verbose = 1):
	'''
	this function is used to execute sql queries strings through pydatagateway function.
	it can contain insert into and create table formats:

	for instance:
		- insert table: 
		q = 'insert into econs_id.df_testing(select id, name, email from public.drivers limit 10)'
		
		- create table:
		q = """
		create table if not exists econs_id.testing (
		id int,
		name varchar,
		email varchar
		) WITH (
		    partitioned_by = ARRAY['id'])"""

		- drop table:
		q = 'drop table econs_id.df_testing'

		- delete table
		q = 'delete from econs_id.df_testing where name = 'Hadaiq'

	ps: be aware of the usage of insert table, the columns must be same as the actual 
	stored columns in the database.
	'''

	konPr = conPr(verbose= verbose)

	if verbose:
	    print('executing query!')
	    start = datetime.now()

	konPr.execute(query)

	if verbose:
	    print('query\'s been pushed in '+str(datetime.now()-start))

	return None
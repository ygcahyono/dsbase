**DSBASE** a package will keep be developed to help day to day work as a data servant to gather insight as fast and effective as possive. This package projected will be having some Statistical method for problem solving, connector to the database, create and process report on Google Drive, and many FUN project related Data Analytics / Science day to day aspects hopefully will be developed in this package.

## Installation.

1. Clone the depedencies.
	a. Anaconda (preferably using Anaconda 3.5+)
	'''
	$ conda install -c anaconda mysql-connector-python
	'''

	b. Install pydatagateway, geopandas, shapely
	'''
	$ sudo pip install -r requirements.txt
	'''

2. Clone this repository and install this repository
	'''
	$ sudo python setup.py install
	'''

## Creds requirements.

	Please create your own credentials and put it into queryGrab folder (credentials.py).


## Functions.

### Day to day work.

- [Presto](#1-presto)
	- [x] Query to Pandas DF (PyHive connector).
	- [x] Develop functions that could execute several sql queries. Eg: insert, drop, and delete.
- [Geohash](#2-geohash)
	- [x] Create Geohash file from geofences list.
- [Google Sheet](#3-google-sheet)
	- [x] Read google docs from known docs name.
	- [x] Write, Insert, Delete, Share Google Sheets.
	- [x] Create folder and move files
	- [ ] Gather all google docs file from cloud repo.

### Data Analytics related work.

- [x] Slovin's Formula
- [x] Parallelization (By Rows)
- [ ] Cohort Graphs


## How to do.

### Presto.
Gather data from Presto Hive Grab Database and return `Pandas format DataFrame`.

- `def queryPr(query, verbose = 1):`: 

	example:
	```
	Q = ('''
	select * from yourScheme.yourTable limit 10
	''')
	df = queryPr(Q)
	```

### Geohash
Turn the list of pair coordinate into Geohash file that can be used to determine specific location so we can pull the exact 
booking rides (f0r example) from database.

	example:
	```
	# set the geofence.
	lists = [106.75665329101594, -5.9485476420121, 106.87214100000006, -5.91722502774615, 106.93003999999996, -5.752303, 106.72691199999997, -5.775628, 106.72918747070298, -5.94171811791231, 106.75665329101594, -5.9485476420121]

	# convert it to csv file with the determine properties.
	convert_polygon_to_geohash(list, name = 'default', precision= 6, city_id = 10, country_id = 6, city_name = 'Jakarta')
	```


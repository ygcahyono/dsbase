
**DSBASE** is an package that hopefully keep on developed to help the day to day work of Data Scientist 
in Grab Indonesia. This base usage of this package is to pull the data from our Presto database using 
pydatagateway to become Pandas DataFrame.

a
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

## Creds requirement.
	Please create your own credentials and put it into DSBASE folder (credentials.py).

## Functions.

### Day to day work.

- [Presto](#1-presto)
	- [x] Query to Pandas DF.
	- [x] Develop functions that could execute several sql queries. Eg: insert, drop, and delete.
- [Geohash](#2-geohash)
	- [x] Create Geohash file from geofences list.
- [Google Sheet](#3-google-sheet)
	- [x] Read google docs from known docs name.
	- [ ] Gather all google docs file from cloud repo.

### Data Science related work.

- [x] Slovin's Formula



## How to do.

### Presto.
Gather data from Presto Hive Grab Database and return `Pandas format DataFrame`.

- `def queryPr(query, verbose = 1):`: 

	example:
	```
	Q = ('''
	select * from public.prejoin_bookings limit 10
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


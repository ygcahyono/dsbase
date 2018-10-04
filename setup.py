import setuptools

setuptools.setup(
    name="queryGrab",
    version="0.1.0",
    url="",
    author="Yogi Cahyono",
    author_email="yogi.cahyono@grabtaxi.com",
    description="A package to help COUNTRY DATA SCIENTISTS to finish their straightforward works.",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)

try:
    from pydatagateway import datagateway
except:
    sys.exit('Please install pydatagateway')
try:
    import geopandas
except:
    sys.exit('Please install geopandas')
try:
    from shapely.geometry import Polygon, MultiPolygon
except:
    sys.exit('please install shapely')
try:
    import geohash
except:
    sys.exit('please install geohash')
try:
    import pyproj
except:
    sys.excit('please install pyproj')


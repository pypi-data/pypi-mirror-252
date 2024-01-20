
*mapdata.py* is a viewer for geographic coordinate data read from a CSV file, spreadsheet,
or database.  Both a map and a data
table are displayed.  When a location is selected on the map, the same location is highlighted in the
table, and *vice-versa*.  Single or multiple selections may be enabled.  Locations may also
be selected and highlighted by writing a query expression to select rows of the data table.

![example map](https://mapdata.readthedocs.io/en/latest/_images/UI_CSOs_1.png)
Coordinates should be in decimal degrees, in WGS84 (coordinate reference system [CRS] 4326), however,
coordinates in other CRSs can be converted to 4326.

The map display can be customized in several ways:

  * Different raster tile servers may be used for the basemap.  The default is
    OpenStreetMap.  Several alternatives are provided, and other tile servers
    can be specified in a configuration file.

  * Locations identified by coordinates in the data file may be designated by
    different types of markers and by different colors.  The default marker for
    locations, and the default marker used to flag selected locations can both be
    customized.  Symbols and colors to use for location markers can be specified
	in a configuration file and in the data file.  Different symbols and markers
	can be used for different selected locations.

  * Locations may be unlabeled or labeled with data values from the data file
    The label font, size, color, and location can all be customized.

The map can be exported to a Postscript, PNG, or JPEG file.  Using command-line options,
*mapdata* can be directed to load a data file and display location markers and then to
export the map to an image file, and quit.

Selected rows in the data table can be exported to a CSV or spreadsheet file.

Data can also be displayed in several different types of plots: box plots, scatter
plots, line charts, ECDF plots, Q-Q plots, Fisher-Jenks group plots, strip charts, 
and counts of categorical and quantitative variables.  Plots
can use either all data or only data values that are selected in the map and
table.  Plots have a live connection to the data table, so when selections are
changed the plots are automatically updated.

![example plot](https://mapdata.readthedocs.io/en/latest/_images/UI_cat_stripchart.png)

SQL commands can be used when pulling a data set from a database, to create
a temporary table, for example, instead of using a base table.  The SQL
commands can be augmented with [execsql](https://pypi.org/project/execsql/)
metacommands and substitution variables.

Complete documentation is at [https://mapdata.readthedocs.io/en/latest](https://mapdata.readthedocs.io/en/latest).

A configuration file template, application icons for Linux and Windows, a .desktop
file for Linux, and additional bitmap symbols, are available for download from
[OSDN](https://osdn.net/projects/mapdata/releases/).


## Dependencies

*Mapdata.py* uses the following third-party Python libraries:

  * [jenkspy](https://pypi.org/project/jenkspy/)

  * [loess](https://pypi.org/project/loess/)

  * [numpy](https://pypi.org/project/numpy/)

  * [matplotlib](https://pypi.org/project/matplotlib/)

  * [odfpy](https://pypi.org/project/odfpy/)
  
  * [openpyxl](https://pypi.org/project/openpyxl/)

  * [pillow](https://pypi.org/project/pillow/)

  * [pyproj](https://pypi.org/project/pyproj/)

  * [scipy.stats](https://pypi.org/project/SciPy/)

  * [seaborn](https://pypi.org/project/seaborn/)

  * [statsmodels](https://pypi.org/project/statsmodels/)

  * [tkintermapview](https://pypi.org/project/tkintermapview/)

  * [xlrd](https://pypi.org/project/xlrd/)

If *mapdata.py* is used to query a database to obtain a data set to view and
explore, then one or more of the following Python libraries will have to be
installed manually, depending on the type of DBMS used:

   * PostgreSQL: [psycopg2](https://pypi.org/project/psycopg2/)

   * MariaDB and MySQL: [pymysql](https://pypi.org/project/pymysql/)

   * DuckDB: [duckdb](https://pypi.org/project/duckdb/)

   * SQL Server: [pydobc](https://pypi.org/project/pyodbc/)

   * Oracle: [cx-Oracle](https://pypi.org/project/cx-Oracle/)

   * Firebird: [fdb](https://pypi.org/project/fdb/)


[![Downloads](https://pepy.tech/badge/mapdata)](https://pypi.org/project/mapdata/)  

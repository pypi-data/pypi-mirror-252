import setuptools
import io

with io.open('README.md', encoding='utf-8') as f:
	long_description = f.read()

setuptools.setup(name='mapdata',
	version='2.21.0',
	description="An interactive map and table explorer for geographic coordinates in a spreadsheet, CSV file, or database",
	author='Dreas Nielsen',
	author_email='cortice@tutanota.com.com',
    url='https://osdn.net/project/mapdata/',
    packages=['mapdata'],
	scripts=['mapdata/mapdata.py'],
    license='GPL',
	install_requires=['tkintermapview', 'pyproj', 'jenkspy', 'odfpy', 'openpyxl', 'xlrd', 'matplotlib', 'seaborn', 'loess', 'statsmodels', 'scipy'],
	python_requires = '>=3.8',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Environment :: X11 Applications',
		'Environment :: Win32 (MS Windows)',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Information Technology',
		'License :: OSI Approved :: GNU General Public License (GPL)',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Operating System :: POSIX',
		'Operating System :: Microsoft :: Windows',
		'Programming Language :: Python :: 3',
		'Topic :: Office/Business',
		'Topic :: Scientific/Engineering'
		],
	keywords=['Map', 'Locations', 'CRS', 'CSV', 'Spreadsheet', 'Database', 'PNG', 'JPG', 'Postscript'],
	long_description_content_type="text/markdown",
	long_description=long_description
	)

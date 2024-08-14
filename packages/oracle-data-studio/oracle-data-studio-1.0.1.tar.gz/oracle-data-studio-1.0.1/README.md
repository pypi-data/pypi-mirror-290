# Python Data Studio API

Python client for Data Studio on ADB offers a number of operations on accessing and management of Oracle Databases via Oracle REST Database Services. In particular, functions are provided which support upload to the database files from Cloud Store, tables from database links, manipulation with analytic views and insights.

Data Studio API is working in Python 3.6 or later version.

### Build Python Data Studio API (Source Distribution and Built Distribution)

To build all distributions of Python Data Studio API, use the following command in core folder:

	python -m build

This command generates two files in dist directory: adp_ords-<version>.tar.gz (source distribution) and adp_ords-<version>-py3-none-any.whl (built distribution) files.

### Install Data Studio API from Python Wheel file

There are two options to install Python ORDS: without dependencies and with dependencies. Python Data Studio API has only one dependencies: requests package.

All related package that are used in Data Studio API, are listed in file requirements.txt. You may install these packages independently from Data Studio API, and the install Data Studio API using the following command:

	pip install ords_python-1.0.0-py3-none-any.whl

To install Data Studio API and its dependencies, use the following command:

	pip install ords_python-1.0.0-py3-none-any.whl -r requirements.txt

### Using Data Studio API

Python file should contain two lines:

	import adp
	ords = adp.login(url,username,password)

where `url` is an url for ORDS with protocol, host and port,
`username` is a name of the schema,
`password`  is a password of the schema.


This code returns an instance to the class that contains all Data Studio functions.

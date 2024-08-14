# Python Data Studio API

Python client for Data Studio on ADB offers a number of operations on accessing and management of Oracle Databases via Oracle REST Database Services. In particular, functions are provided which support upload to the database files from Cloud Store, tables from database links, manipulation with analytic views and insights.

Data Studio API is working in Python 3.6 or later version.

### Install Data Studio API

	pip install oracle-data-studio


### Using Data Studio API

Python file should contain two lines:

	import adp
	ords = adp.login(url,username,password)

where `url` is an url for ORDS with protocol, host and port,
`username` is a name of the schema,
`password`  is a password of the schema.


This code returns an instance to the class that contains all Data Studio functions.

For more detailed documentation, visit [Oracle documentation](https://docs.oracle.com/en/database/oracle/sql-developer-web/sdwad/working-python-ords-api-oml.html)

MySQL database functions for data collected

# Create Database

## Create Empty MySql Database

Create a an empty MySql database to hold the sample data.

## Execute Sql Scripts

To create the database execute the SQL scripts in the following order:

1. create-material_samples.SQL
2. create-mm_samples.SQL
3. create-cmmi_pixel_data.SQL
4. create-scattering_geometry_pixel_map.SQL

## Execute Pixel Map Data Loader

Execute the pixel map data loader against the target database.

This will load the scattering_geometry_pixel_map table.  

Modify the JSON configuration file with the target database values.
Modify the JSON configuration file with the path to the samples.

pixel-map-data-loader/config.json
```
{
    "dataDirectory" : "%DataDirectory%",
    "hostName" : "%DatabaseHostName%",
    "userName" : "%DatabaseUserName%", 
    "userPassword": "%DatabaseUserPassword%",
    "dbName": "%DatabaseName"
}
```

Execute the pixel-map-data-loader (must be in pixel-map-data-loader directory)
```
python3 main.py
```

## Execute Data Loader

Execute the data loader to load all of the samples into the database.  This will take a very long time.

Modify the JSON configuration file with the target database values.
Modify the JSON configuration file with the path to the samples.

data-loader/config.json
```
{
    "dataDirectory" : "%DataDirectory%",
    "hostName" : "%DatabaseHostName%",
    "userName" : "%DatabaseUserName%", 
    "userPassword": "%DatabaseUserPassword%",
    "dbName": "%DatabaseName"
}
```

This will load the following tables:
mm_samples
material_samples
cmmi_pixel_data

Execute the data-loader (must be in data-loader directory)
```
python3 main.py
```

## Execute Sample Queries

To test the database connect to the database with MySql Workbench and execute queries to test the database.

Modify the JSON launch file with the approiate query parameters.
Modify the JSON configuration file with the target database values.

Execute the desired query python file (must be in the queries directory) via the command line
```
python3 query1.py
```
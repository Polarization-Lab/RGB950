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

TODO: finish XXXXXX
This will load the XXXXXX table.  

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

Execute the pixel-map-data-loader
```
TODO: figure out 
```

## Execute Data Loader

Execute the data loader to load all of the samples into the database.  This will take a very long time.

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

This will load the following tables:

TODO: list the tables.


```
TODO: figure out 
```

## Execute Sample Queries

To test the database connect to the database with MySql Workbench and execute queies to test the database.

```
TODO: add sample query
```
import os
import sys
import json
import math
from mysql.connector import Error
from dataloader import loadSample
from dataloader import Config
from dataloader import createDBConnection

def read_query(connection, query,data):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query,data)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def main():
    # load the configuration
    scriptDir = os.path.dirname(__file__)
    configPath = os.path.join(scriptDir, 'config.json')

    with open(configPath, "r") as json_data_file:
        jsonData = json.load(json_data_file)

    # get the directory where the CMMI files are stored
    config = Config()
    config.rootSampleDirectory = jsonData["rootSampleDirectory"]
    config.hostName = jsonData["hostName"]
    config.userName = jsonData["userName"] 
    config.userPassword = jsonData["userPassword"]
    config.dbName = jsonData["dbName"]

    # create database connection
    dbConnection = createDBConnection(config.hostName, config.userName, config.userPassword, config.dbName)

    # looping over degree increment table
    theta_h = 1
    for phi_d in range(1,362):
        for theta_d in range(1,92):
            while(theta_h < 92):
                # convert to radians
                phi_d = math.radians(phi_d)
                theta_d = math.radians(theta_d)
                theta_h = math.radians(theta_h)
                
                queryStatement = """SELECT pixel_x, pixel_y, AOI, AOC FROM scattering_geometry_pixel_map AS sgpm WHERE sgpm.phi_d = %s AND sgpm.theta_d = %s AND sgpm.theta_h = %s"""
                data = (phi_d,theta_d,theta_h)
                result = read_query(dbConnection,queryStatement,data)
                
                # TODO: add to new table OR create "closest" algorithm here
                if len(result) == 0:
                    # perform closest algorithm
                    # minimize the distance
                    closest = 0
                else:
                    # insert into table
                    insertStatement = """INSERT pixel_x, pixel_y, AOI, AOC INTO mitsuba_map VALUE(%s,%s,%s,%s)"""
                    values = (pixel_x,pixel_y,AOI,AOC)
                    read_query(dbConnection, insertStatement,values)

                # convert back to degrees for proper iterating
                phi_d = math.degrees(phi_d)
                theta_d = math.degrees(theta_d)
                theta_h = math.degrees(theta_h)
                theta_h = 90*(theta_h/91)^2
            

          
if __name__ == "__main__":
    main()

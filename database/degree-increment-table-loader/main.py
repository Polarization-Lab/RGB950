# load the table that holds degree increments for all values/combinations of theta_h...
import os
import sys
import json
import math
from mysql.connector import Error
from dataloader import loadSample
from dataloader import Config
from dataloader import createDBConnection

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

    # TODO: add loops here to loop through old table
    for phi_d in range(1,362):
        for theta_d in range(1,92):
            for theta_h in range(1,92):
                phi_d = math.radians(phi_d)
                theta_d = math.radians(theta_d)
                theta_h = math.radians(theta_h)
                insertStmt = """INSERT INTO degree_increments_map (phi_d,theta_d,theta_h) VALUES (%s,%s,%s)"""
                data = (phi_d,theta_d,theta_h)
                cursor = dbConnection.cursor()
                try:
                    cursor.execute(insertStmt, data)
                    dbConnection.commit()
                    print("Query successful")
                except Error as err:
                    print(f"Error: '{err}'")
                phi_d = math.degrees(phi_d)
                theta_d = math.degrees(theta_d)
                theta_h = math.degrees(theta_h)


if __name__ == "__main__":
    main()

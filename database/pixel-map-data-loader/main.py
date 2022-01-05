import os
import json
import mysql.connector
import pandas as pd
from mysql.connector import Error
from decimal import *
        
def createDBConnection(hostName, userName, userPassword, dbName):
    
    """Establish a connection to a mySQL server
        Parameters
        ----------
        host_name : str
        user_name : str
        user_password : str
        db_name : str
            
        Returns
        -------
        connection : connection object 
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostName,
            user=userName,
            passwd=userPassword,
            database=dbName,
            auth_plugin = 'mysql_native_password'
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def readDataFile(dataFilePath):
    # create an array to hold the file data
    fileData = []

    # read the file into an array
    with open(dataFilePath) as fp:
        line = fp.readline()
        while line:
            # split the line to an array
            lineData = line.split('","')

            # add the line data to the file data arrary
            fileData.append(lineData)

            # convert the line data into decimal
            line = fp.readline()

    # return the file data
    return fileData

def loadData(dbConnection, AOI, AOC, fileData):
    # define the insert statement that will be used 
    # to insert the data into the database
    insertStmt = """INSERT INTO scattering_geometry_pixel_map (pixel_x,pixel_y,theta_h,phi_h,theta_d,phi_d,AOI,AOC) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

    # load the data into the database
    pixel_x = 0
    for row in fileData:
        pixel_y = 0

        for column in row:
            # remove the linefeed
            column = column.strip()

            # remove open curly brace
            columnData = column.replace('"{', '')
            if columnData.__contains__("{"):
                columnData = column.replace('{', '')

            # remove end curly brace
            columnData = columnData.replace('}', '')
            if (columnData.__contains__('"')):
                columnData = columnData.replace('"', '')

            # split the data
            pixelData = columnData.split(",")

            # convert the data to the correct variables
            try:
                
                theta_h = Decimal(pixelData[0])
                phi_h = Decimal(pixelData[1])
                theta_d = Decimal(pixelData[2])
                if (pixelData[3].__contains__("*")): 
                    pixelData[3] = pixelData[3].replace("*^", "e")
                phi_d = Decimal(pixelData[3])

                # create data for insert
                data = (pixel_x,pixel_y,theta_h,phi_h,theta_d,phi_d,AOI,AOC)
                
                # execute the insert statement
                cursor = dbConnection.cursor()
                try:
                    cursor.execute(insertStmt,data)
                    dbConnection.commit()
                    print("Query successful")
                except Error as sqlError:
                    print(f"Error: '{sqlError}'")
            except:
                print(pixel_x)      
                print(pixel_y)        

            # increment the y pixel location
            pixel_y+=1
        # increment the x pixel location
        pixel_x+=1

def main():
    # load the configuration
    scriptDir = os.path.dirname(__file__)
    configPath = os.path.join(scriptDir, 'config.json')

    with open(configPath, "r") as json_data_file:
        jsonData = json.load(json_data_file)

    # get the directory where the map data files are stored
    dataDirectory = jsonData["dataDirectory"]
    hostName = jsonData["hostName"]
    userName = jsonData["userName"] 
    userPassword = jsonData["userPassword"]
    dbName = jsonData["dbName"]

    # look for the data files in the data directory
    object = os.scandir(dataDirectory)

    # loop over all of the data files in the data directory
    for n in object :
        if n.is_file():
            # get the file name
            dataFileName = n.name
            print (dataFileName)

            if (dataFileName.__contains__(".csv")):

                # parse the data file name
                AOI = dataFileName.rsplit("_", 3)[1]
                AOC = dataFileName.rsplit("_", 3)[2]
                AOC = AOC.rsplit(".",2)[0]

                print (AOI)
                print (AOC)

                # build the path to the data file 
                dataFilePath = os.path.join(dataDirectory, dataFileName)

                # read the data file into an array
                fileData = readDataFile(dataFilePath)

                # connect to the database
                dbConnection = createDBConnection(hostName, userName, userPassword, dbName)

                # load the data file into the database
                loadData(dbConnection, AOI, AOC, fileData)
    object.close()

          
if __name__ == "__main__":
    main()

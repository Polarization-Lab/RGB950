import math
import os
import glob
import json
from dataloader import createDBConnection
from dataloader import Config
from cmmidataloader import readCMMI

class MMData:
    m00 = []
    m01 = []
    m02 = []
    m03 = []
    m10 = []
    m11 = []
    m12 = []
    m13 = []
    m20 = []
    m21 = []
    m22 = []
    m23 = []
    m30 = []
    m31 = []
    m32 = []
    m33 = []

# TODO: clean up and create a function to control the process and add input parameters for function (sampleNo,wavelength)

def read_query(connection, query,data):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query,data)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def average(lst):
    return sum(lst) / len(lst)

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
config.sampleNo = jsonData["sampleNo"]
config.wavelength = jsonData["wavelength"]

# create new map table that holds the specific pixels that correspond to degree increments of phi_d, theta_h, and theta_d

# process: take the table that will hold the degeree increments of all the combinations of phi_h... 
# take each combo and put it through sgpm table and find the closest value -> 
# take that pixel location and AOI and AOC and store it in new map table

# using this to add to dictionary/add to pBRDF

dbConnection = createDBConnection(config.hostName, config.userName, config.userPassword, config.dbName)

for phi_d in range(1,362):
    for theta_d in range(1,92):
        theta_h = 0
        previous_theta_h = 0
        next_theta_h = 90*math.pow(theta_h/91,2)
        while(theta_h < 92):
            # convert to radians
            phi_d_radians = math.radians(phi_d)
            theta_d_radians = math.radians(theta_d)
            theta_h_radians = math.radians(theta_h)
            previous_theta_h_radians = math.radians(previous_theta_h)
            next_theta_h_radians = math.radians(next_theta_h)

            # define bins
            lower_phi_d = phi_d_radians - math.radians(0.5)
            upper_phi_d = phi_d_radians + math.radians(0.5)
            lower_theta_d = theta_d_radians - math.radians(0.5)
            upper_theta_d = theta_d_radians + math.radians(0.5)
            lower_theta_h = (theta_h_radians - previous_theta_h_radians)/2
            upper_theta_h = (next_theta_h_radians - theta_h_radians)/2

            # find pixels for each bin
            queryStatement = """SELECT pixel_x, pixel_y, AOI, AOC FROM scattering_geometry_pixel_map AS sgpm WHERE phi_d BETWEEN %s AND %s
                AND theta_h BETWEEN %s AND %s
                AND theta_d BETWEEN %s AND %s"""
            data = (lower_phi_d,upper_phi_d,lower_theta_h,upper_theta_h,lower_theta_d,upper_theta_d)
            result = read_query(dbConnection,queryStatement,data)

            mmData = MMData()

            # loop over results
            for row in result:
                pixel_x = row[0]
                pixel_y = row[1]
                # build filename based on sample_no and AOI and AOC
                #20210712_001_451_615ms_f8_10_20.cmmi
                for subdirs, dirs, files in os.walk("/Users/carolinehumphreys/Projects/Polarization-Lab/RGB950/database/data-loader/test-data/2021"):
                    # loop over all of the files
                    for fileName in files:
                        # only process cmmi files
                        filePattern = AOI + "_" + AOC + ".cmmi"
                        if (fileName.__contains__(filePattern)):
                            mm = readCMMI(fileName)
                            image0 = mm[0]
                            image1 = mm[1]
                            image2 = mm[2]
                            image3 = mm[3]
                            image4 = mm[4]
                            image5 = mm[5]
                            image6 = mm[6]
                            image7 = mm[7]
                            image8 = mm[8]
                            image9 = mm[9]
                            image10 = mm[10]
                            image11 = mm[11]
                            image12 = mm[12]
                            image13 = mm[13]
                            image14 = mm[14]
                            image15 = mm[15]

                            mmData.m00.append(image0[pixel_x][pixel_y])
                            mmData.m01.append(image1[pixel_x][pixel_y])
                            mmData.m02.append(image2[pixel_x][pixel_y])
                            mmData.m03.append(image3[pixel_x][pixel_y])
                            mmData.m10.append(image4[pixel_x][pixel_y])
                            mmData.m11.append(image5[pixel_x][pixel_y])
                            mmData.m12.append(image6[pixel_x][pixel_y])
                            mmData.m13.append(image7[pixel_x][pixel_y])
                            mmData.m20.append(image8[pixel_x][pixel_y])
                            mmData.m21.append(image9[pixel_x][pixel_y])
                            mmData.m22.append(image10[pixel_x][pixel_y])
                            mmData.m23.append(image11[pixel_x][pixel_y])
                            mmData.m30.append(image12[pixel_x][pixel_y])
                            mmData.m31.append(image13[pixel_x][pixel_y])
                            mmData.m32.append(image14[pixel_x][pixel_y])
                            mmData.m33.append(image15[pixel_x][pixel_y])

                # for name in glob.glob('/Users/carolinehumphreys/Projects/Polarization-Lab/RGB950/database/data-loader/test-data/2021/*[0-9].*'):
                #     print(name)
                # build filepath based on Config and filename
                # read CMMI file
                # collect the pixel data into array

            # average MM data for all collected pixel data
            # TODO: make sure 0s arent getting averaged
            m00 = average(mmData.m00)
            m01 = average(mmData.m01)
            m02 = average(mmData.m02)
            m03 = average(mmData.m03)
            m10 = average(mmData.m10)
            m20 = average(mmData.m20)
            m30 = average(mmData.m30)
            m11 = average(mmData.m11)
            m12 = average(mmData.m12)
            m21 = average(mmData.m21)
            m22 = average(mmData.m22)
            m23 = average(mmData.m23)
            m31 = average(mmData.m31)
            m32 = average(mmData.m32)
            m33 = average(mmData.m33)
            m13 = average(mmData.m13)

            # TODO: put into dictionary with corresponding theta_d, theta_h, phi_d


            # take pixels and AOI and AOC and phi_d,theta_d, and theta_h
            # put into pixel table
            # take AOI and AOC -> a file
            # in that file -> pixels
            # average each MM value for the given pixels
            # goes into the dictionary (pBRDF for rendering)
            
            # iterate theta_h
            previous_theta_h = theta_h
            theta_h = 90*(theta_h/91)^2
            next_theta_h = 90*(theta_h/91)^2


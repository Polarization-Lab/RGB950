import math
import os
import glob
import json
#import h5py
import numpy as np
from dataloader import createDBConnection
from dataloader import Config
from cmmidataloader import readCMMI
from tensor import write_tensor
from tensor import read_tensor

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

# made connection to the database
dbConnection = createDBConnection(config.hostName, config.userName, config.userPassword, config.dbName)

# sample pbsdf to be changed
result1 = read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')

# looping over degree increments for each angle
# at each degree increment the bins are created and the MM values averaged for each bin
for phi_d in range(0,361):
    for theta_d in range(0,91):
        # theta_h = 0
        previous_theta_h = 0
        # next_theta_h = 90*math.pow(theta_h/91,2)
        for theta_h in range(0,91):
        # while(theta_h < 92):

            # debugging
            if(phi_d == 72):
                print('breakpoint')
            # determine the previous theta_h
            if (theta_h > 1): 
                previous_theta_h = theta_h - 1
            else:
                previous_theta_h = 0

            # determine the next theta_h to find the correct bin
            next_theta_h = 90*math.pow(theta_h/91,2)

            # convert to radians
            phi_d_radians = math.radians(phi_d)
            theta_d_radians = math.radians(theta_d)
            theta_h_radians = math.radians(theta_h)
            previous_theta_h_radians = math.radians(previous_theta_h)
            next_theta_h_radians = math.radians(next_theta_h)

            # define bins
            # bin around phi_d is +- 0.5 degrees
            lower_phi_d = phi_d_radians - math.radians(0.5)
            upper_phi_d = phi_d_radians + math.radians(0.5)
            # bin around theta_d is +- 0.5 degrees
            lower_theta_d = theta_d_radians - math.radians(0.5)
            upper_theta_d = theta_d_radians + math.radians(0.5)
            # bin around theta_h is defined as midpoint between previous and next values and current value
            lower_theta_h = theta_h_radians - math.radians(0.5)
            upper_theta_h = theta_h_radians + math.radians(0.5)
            #lower_theta_h = (theta_h_radians - previous_theta_h_radians)/2
            #upper_theta_h = (next_theta_h_radians - theta_h_radians)/2

            # find pixels for each bin
            print('phi_d')
            print(phi_d)
            print('theta_d')
            print(theta_d)
            print('theta_h')
            print(theta_h)
            queryStatement = """SELECT pixel_x, pixel_y, AOI, AOC FROM scattering_geometry_pixel_map AS sgpm WHERE phi_d BETWEEN %s AND %s
                AND theta_h BETWEEN %s AND %s
                AND theta_d BETWEEN %s AND %s"""
            data = (lower_phi_d,upper_phi_d,lower_theta_h,upper_theta_h,lower_theta_d,upper_theta_d)
            result = read_query(dbConnection,queryStatement,data)
            # if we dont have data that matches the bin
            if len(result)==0:
                # put 0 in M in dictionary
                print('No data found')
                result1['M'][phi_d,theta_d,theta_h,:,:,:] = np.nan

            else: 
                mmData = MMData()
                print('Found Data')

                # TODO: make a lookup table that holds which pixels and files correspond to which bins
                # another table/file somewhere

                # loop over results of query
                for row in result:
                    pixel_x = row[0]
                    pixel_y = row[1]
                    AOI = str(row[2])
                    AOC = str(row[3])

                    # define the path of sample for which the pbsdf is to be created
                    samplePath = "/Users/carolinehumphreys/Projects/Polarization-Lab/RGB950/database/data-loader/test-data/2021/001"

                    # loop over over the wavelength folders
                    for i in range(1,4):
                        dir_list = os.listdir(samplePath)
                            # loop over the wavelength directories
                        wavelengthDirectory = os.path.join(samplePath,dir_list[i])
                        cmmiDirectory = os.path.join(wavelengthDirectory,'cmmi')

                        wavelength = wavelengthDirectory.rsplit("_", 6)[2]
                        print(wavelength)

                        # loop over all of the files
                        for fileName in os.listdir(cmmiDirectory):
                            # only process cmmi files
                            filePattern = AOI + "_" + AOC + ".cmmi"
                            if (fileName.__contains__(filePattern)):
                                filePath = os.path.join(cmmiDirectory,fileName)
                                mm = readCMMI(filePath)
                                print('done')
                                
                                # obtaining Mueller matrix data
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

                                # adding Mueller Matrix data to class
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
                                break

                # average MM data for all collected pixel data
                m00 = np.nanmean(mmData.m00)
                m01 = np.nanmean(mmData.m01)
                m02 = np.nanmean(mmData.m02)
                m03 = np.nanmean(mmData.m03)
                m10 = np.nanmean(mmData.m10)
                m20 = np.nanmean(mmData.m20)
                m30 = np.nanmean(mmData.m30)
                m11 = np.nanmean(mmData.m11)
                m12 = np.nanmean(mmData.m12)
                m21 = np.nanmean(mmData.m21)
                m22 = np.nanmean(mmData.m22)
                m23 = np.nanmean(mmData.m23)
                m31 = np.nanmean(mmData.m31)
                m32 = np.nanmean(mmData.m32)
                m33 = np.nanmean(mmData.m33)
                m13 = np.nanmean(mmData.m13)
                
                # assign MM values to the dictionary
                wavelength = int(wavelength)
                if wavelength == 451:
                    wavelengthIndex = 1
                elif wavelength == 524:
                    wavelengthIndex = 2
                else:
                    waveleghtIndex = 3
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,0,0] = m00
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,0,1] = m01
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,0,2] = m02
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,0,3] = m03
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,1,0] = m10
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,2,0] = m20
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,3,0] = m30
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,1,1] = m11
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,1,2] = m12
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,1,3] = m13
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,2,1] = m21
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,2,2] = m22
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,2,3] = m23
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,3,1] = m31
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,3,2] = m32
                result1['M'][phi_d,theta_d,theta_h,wavelengthIndex,3,3] = m33
                
                # take pixels and AOI and AOC and phi_d,theta_d, and theta_h
                # put into pixel table
                # take AOI and AOC -> a file
                # in that file -> pixels
                # average each MM value for the given pixels
                # goes into the dictionary (pBRDF for rendering)
            
        # iterate theta_h
        # previous_theta_h = theta_h
        # theta_h = 90*math.pow(theta_h/91,2)
        # next_theta_h = 90*math.pow(theta_h/91,2)

# write to pbsdf file at the very end
# result1 is the dictionary that holds the data
write_tensor("temp1.pbsdf", **result1)
print('wrote to pbsdf file')
# write_tensor(filename="test.pbsdf", M=data['M'], phi_d=data['phi_d'], theta_d=data['theta_d'], theta_h=data['theta_h'],wvls=data['wvls'])



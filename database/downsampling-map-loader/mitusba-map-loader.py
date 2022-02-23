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

# looping over degree increments for each angle
# at each degree increment the bins are created and the MM values averaged for each bin
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
            # if we dont have data that matches the bin
            if len(result)==0:
                # put 0 in M in dictionary
                result1 = read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')
                result1['M']=0

            else: 
                AOI = result[2]
                AOC = result[3]

                mmData = MMData()

                # TODO: make a lookup table that holds which pixels and files correspond to which bins
                # another table/file somewhere

                # loop over results of query
                for row in result:
                    pixel_x = row[0]
                    pixel_y = row[1]
                    # build filename based on sample_no and AOI and AOC
                    # file name example:
                    # 20210712_001_451_615ms_f8_10_20.cmmi
                    for subdirs, dirs, files in os.walk("/Users/carolinehumphreys/Projects/Polarization-Lab/RGB950/database/data-loader/test-data/2021"):
                        # loop over all of the files
                        for fileName in files:
                            # TODO: keep each wavelength separate here
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
                # TODO: material and location of samples will change
                # material_name = '001'
                # TODO: probably need to add some more loops here
                # pbrdf_fn = os.path.join('/Users/carolinehumphreys/Desktop/Polarization Lab/pBSDF files', config.sampleNo, 'table_backward\pbrdf.mat')
                # pbrdf_out_fn = os.path.join('/Users/carolinehumphreys/Desktop/Polarization Lab/pBSDF files', config.sampleNo, 'table_backward', config.sampleNo + '.pbrdf')

                # pbrdf_dat = h5py.File(pbrdf_fn)
                result1 = read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')
                # write for loops to loop over wavelengths, MM values
                i = 0
                wavelength = {451,524,662}
                for i in range(2):
                    # assign MM values
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],0,0] = m00
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],0,1] = m01
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],0,2] = m02
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],0,3] = m03
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],1,0] = m10
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],2,0] = m20
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],3,0] = m30
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],1,1] = m11
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],1,2] = m12
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],1,3] = m13
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],2,1] = m21
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],2,2] = m22
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],2,3] = m23
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],3,1] = m31
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],3,2] = m32
                    result1['M'][phi_d,theta_d,theta_h,wavelength[i],3,3] = m33

                # phi_d = np.array(pbrdf_dat['phi_d'])
                # theta_d = np.array(pbrdf_dat['theta_d'])
                # theta_h = np.array(pbrdf_dat['theta_h'])
                

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

            # write to file at the very end
            write_tensor("Temp.pbsdf", **result1)


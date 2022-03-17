import struct
import numpy as np
import os
from cmmidataloader import readCMMI
import tensor
from tensor import write_tensor
from tensor import read_tensor

class CMMIWavelengthData:
    wavelength = 0
    filePath = []
 
# function to open the binary file
def openBinaryFile(filePath):
    with open(filePath, mode='rb') as file: 
        fileContent = file.read()
        a = struct.unpack("H" * ((len(fileContent)) // 2), fileContent)
        a = np.reshape(a, (600,600,3))
        return a

def getBinaryFiles(binaryFilePath):
    binaryFilePathList = []
    # walk through folder and get all binary files
    for subdirs, dirs, files in os.walk(binaryFilePath):
        for fileName in files:
            # ignore the .DS_Store files
            if fileName.__contains__(".DS_Store"):
                continue
            filePath = os.path.join(binaryFilePath,fileName)
            binaryFilePathList.append(filePath)
    return binaryFilePathList

# get list of all the CMMI files and their corresponding wavelengths
def getCMMIFiles(cmmiFilePath):
    # create a dictionary to hold the cmmi files based on wavelength
    cmmiFileWavelengths = {}

    # walk through folder and get all binary files
    for subdirs, dirs, files in os.walk(cmmiFilePath):
        for fileName in files:
            # ignore the .DS_Store files
            if fileName.__contains__(".DS_Store"):
                continue
            
            if (fileName.__contains__(".cmmi")):
                # get the file path
                filePath = os.path.join(cmmiFilePath, subdirs)
                filePath = os.path.join(filePath,fileName)

                # parse the wavelength out of the file name
                wavelength = fileName.rsplit("_", 7)[2]

                # check to see if wavelengthData contains the wavelength
                if wavelength in cmmiFileWavelengths:
                    # wavelengthData contains the wavelength
                    # add the file to array

                    # get a reference to the wavelength file array
                    wavelengthFiles = cmmiFileWavelengths[wavelength]

                    # add the cmmi file path to the wavelength file array
                    wavelengthFiles.append(filePath)

                else:
                    # wavelengthData does not contains the wavelength
                    # create new array
                    wavelengthFiles = []
                    wavelengthFiles.append(filePath)

                    # add the new array to the wavelengths array
                    cmmiFileWavelengths[wavelength] = wavelengthFiles

    return cmmiFileWavelengths
    

# set file paths for cmmi and binary files
binaryFilePath = "/Users/carolinehumphreys/Desktop/Polarization Lab/binaryFiles"
cmmiFilePath = "/Users/carolinehumphreys/Desktop/Polarization Lab/2021/001"

# get list of binary file paths
binaryList = getBinaryFiles(binaryFilePath)
# get the list of cmmi file paths
cmmiList = getCMMIFiles(cmmiFilePath)

# initialize the MM_total and index_tracker dictionaries
MM_total = read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')
MM_total['M'][:,:,:,:,:,:] = np.nan
index_tracker = read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')
index_tracker['M'][:,:,:,:,:,:] = 0
# MM_total = np.zeros(361,91,91,3,4,4);        
# MM_total = np.nan;
# indx_tracker = np.zeros(361,91,91,3);

# loop through each wavelength
for wavelength in cmmiList:
    # get the cmmi files for each wavelengths
    wavelengthFiles = cmmiList[wavelength]

    # set index tracker to be 0
    k=0

    # loop over the 30 cmmi files and 30 binary files
    for filePath in wavelengthFiles:
        # get the Mueller Matrix data from the file
        mm = readCMMI(filePath)
        # open the binary file here
        table = openBinaryFile(binaryList[k])
        print(k)
        # iterate k
        k = k + 1
        # loop over the 600x600 pixels
        for i in range(600):
            for j in range(600):
                #access the angle coord. per pixel
                theta_d_idx = table[i,j][0]
                theta_h_idx = table[i,j][1]
                phi_d_idx = table[i,j][2]

                #Get the Mueller matrix at pixel (i,j)
                MM = mm[:,i,j]
                # reshape to 4x4
                MM = MM.reshape(4,4)

                # get wavelength index
                if wavelength == '451':
                    wavelengthIndex = 1
                elif wavelength == '524':
                    wavelengthIndex = 2
                else:
                    wavelengthIndex = 3
                
                # add data to dictionary and increment the index tracker
                index_tracker['M'][phi_d_idx,theta_d_idx,theta_h_idx,wavelengthIndex] +=1;
                MM_total['M'][phi_d_idx,theta_d_idx,theta_h_idx,wavelengthIndex,:,:] += MM;

# calculate the mean using MM_total and index_tracker
#Computing the average MM per bin
# loop over all the bins
for i in range(361):
    for j in range(91):
        for k in range(91):
            # loop over all the wavelengths
            for m in range(3):
                MM_total['M'][i,j,k,m,:,:] = MM_total['M'][i,j,k,m,:,:]/index_tracker['M'][i,j,k,m];        

#load the pbsdf file
# file is sample pBSDF file
A = tensor.read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')
A['M'] = MM_total['M'];
tensor.write_tensor("/Users/carolinehumphreys/Desktop/Polarization Lab/2021/001/pBSDFtest.pbsdf",**A);
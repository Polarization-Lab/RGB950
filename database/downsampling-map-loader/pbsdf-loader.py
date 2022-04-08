import struct
import numpy as np
import os
#from cmmidataloader import readCMMI
import tensor
from tensor import write_tensor
from tensor import read_tensor
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

class CMMIWavelengthData:
    wavelength = 0
    filePath = []

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)    
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

# function stuff for read CMMI files
def readCMMI(inputfilename):
    raw = np.fromfile(inputfilename,np.float32).newbyteorder('>');
    M = np.zeros([16,600,600])
    for i in range(16):
        M[i,:,:] = np.flipud(raw[5+i::16][0:(600*600)].reshape([600,600]).T)
    return M
def PlotCMMI(MM,minval,maxval):
    f, axarr = plt.subplots(nrows = 4,ncols = 4,figsize=(50, 50))
    MM = MM.reshape([4,4,600,600])
    MM = MM/MM[0,0,:,:]
    for i in range(4):
        for j in range(4):
            axarr[i,j].imshow(MM[i,j,:,:],cmap=colmap,vmin = minval,vmax=maxval)
 
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

def getBinaryFile(binaryFilePathList, aoc, aoi):
    for binaryFilePath in binaryFilePathList:
        # parse the AOC and AOI from the file name
        pattern = str(aoi)+ '_' + str(aoc)
        if binaryFilePath.__contains__(pattern):
            return binaryFilePath
    return ""

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
cmmiFilePath = "/Users/carolinehumphreys/Desktop/Polarization Lab/2021/094"

# get list of binary file paths
binaryList = getBinaryFiles(binaryFilePath)

# get the list of cmmi file paths
cmmiList = getCMMIFiles(cmmiFilePath)

# initialize the MM_total and index_tracker dictionaries
MM_total = read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')
MM_total['M'][:,:,:,:,:,:] = 0
MM_total['wvls']=np.array([451,525,662,700,750]).astype(np.uint16)
#index_tracker = read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')
index_tracker = np.zeros([361,91,91,3])
#index_tracker['M'][:,:,:,:,:,:] = 0
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

        # parse out the AOC and AOI out of the CMMI file name
        aoi = filePath.rsplit("_", 7)[6]
        aoc = filePath.rsplit("_", 7)[7]
        aoc = aoc.rsplit(".",2)[0]

        # lookup binary file based on the aoc and aoi
        binaryFilePath = getBinaryFile(binaryList,aoc, aoi)

        # open the binary file here
        table = openBinaryFile(binaryFilePath)
        print(k)
        # iterate k
        k = k + 1
        # loop over the 600x600 pixels
        for i in range(600):
            for j in range(600):
                #access the angle coord. per pixel
                # original
                theta_d_idx = table[i,j][1]-1
                theta_h_idx = table[i,j][0]-1
                phi_d_idx = table[i,j][2]-1
                # version 1
                # theta_d_idx = table[i,j][0]-1
                # theta_h_idx = table[i,j][1]-1
                # phi_d_idx = table[i,j][2]-1
                # version 2 - doenst work
                # theta_d_idx = table[i,j][0]-1
                # theta_h_idx = table[i,j][2]-1
                # phi_d_idx = table[i,j][1]-1
                # # version 3 - doenst work
                # theta_d_idx = table[i,j][1]-1
                # theta_h_idx = table[i,j][2]-1
                # phi_d_idx = table[i,j][0]-1
                # # version 4 - doesnt work
                # theta_d_idx = table[i,j][2]-1
                # theta_h_idx = table[i,j][0]-1
                # phi_d_idx = table[i,j][1]-1
                # # version 5 - doesnt work
                # theta_d_idx = table[i,j][2]-1
                # theta_h_idx = table[i,j][1]-1
                # phi_d_idx = table[i,j][0]-1

                #Get the Mueller matrix at pixel (i,j)
                MM = mm[:,i,j]
                if (np.isnan(MM).any()==1):
                    print('issue')
                
                # normalize the mm data
                norm = np.linalg.norm(MM)
                normMM = MM/norm

                # reshape to 4x4
                MM = normMM.reshape(4,4)

                # get wavelength index
                if wavelength == '451':
                    wavelengthIndex = 0
                elif wavelength == '524':
                    wavelengthIndex = 1
                else:
                    wavelengthIndex = 2
                
                # add data to dictionary and increment the index tracker
                index_tracker[phi_d_idx,theta_d_idx,theta_h_idx,wavelengthIndex] +=1;
                MM_total['M'][phi_d_idx,theta_d_idx,theta_h_idx,wavelengthIndex,:,:] += MM;
                # print("MM_total")
                # print(MM_total['M'][phi_d_idx,theta_d_idx,theta_h_idx,wavelengthIndex,:,:])
                # print("MM")
                # print(MM)

# calculate the mean using MM_total and index_tracker
#Computing the average MM per bin
# loop over all the bins
for i in range(361):
    for j in range(91):
        for k in range(91):
            # loop over all the wavelengths
            for m in range(3):
                if (index_tracker[i,j,k,m] == 0):
                    MM_total['M'][i,j,k,m,:,:]=0
                    # putting the ideal depolarizer instead of 0
                    # MM_total['M'][i,j,k,m,0,0] = 1
                    # MM_total['M'][i,j,k,m,0,1] = 0
                    # MM_total['M'][i,j,k,m,0,2] = 0
                    # MM_total['M'][i,j,k,m,0,3] = 0
                    # MM_total['M'][i,j,k,m,1,0] = 0
                    # MM_total['M'][i,j,k,m,2,0] = 0
                    # MM_total['M'][i,j,k,m,3,0] = 0
                    # MM_total['M'][i,j,k,m,1,1] = 0
                    # MM_total['M'][i,j,k,m,1,2] = 0
                    # MM_total['M'][i,j,k,m,1,3] = 0
                    # MM_total['M'][i,j,k,m,2,1] = 0
                    # MM_total['M'][i,j,k,m,2,2] = 0
                    # MM_total['M'][i,j,k,m,2,3] = 0
                    # MM_total['M'][i,j,k,m,3,1] = 0
                    # MM_total['M'][i,j,k,m,3,2] = 0
                    # MM_total['M'][i,j,k,m,3,3] = 0
                else:
                    MM_total['M'][i,j,k,m,:,:] = MM_total['M'][i,j,k,m,:,:]/index_tracker[i,j,k,m];  

                if (np.isnan(MM_total['M'][i,j,k,m,:,:]).any()==1):
                    print('issue')      

#load the pbsdf file
# file is sample pBSDF file
A = tensor.read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')
A['M'] = MM_total['M'];
A['wvls'] = MM_total['wvls'];
tensor.write_tensor("/Users/carolinehumphreys/Desktop/Polarization Lab/2021/094/pBSDF094_newreadCMMI.pbsdf",**A);
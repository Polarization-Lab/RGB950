import os
from cmmidataloader import readCMMI

samplePath = "/Users/carolinehumphreys/Projects/Polarization-Lab/RGB950/database/data-loader/test-data/2021/001"

# loop over over the wavelength folders

AOI = '10'
AOC = '20'
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
            break
import numpy as np
import struct

import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

#Blue to Red Color scale for MM
colmap = np.zeros((255,3));
# Red
colmap[126:183,0]= np.linspace(0,1,57);
colmap[183:255,0]= 1; 
# Green
colmap[0:96,1] = np.linspace(1,0,96);
colmap[158:255,1]= np.linspace(0,1,97); 
# Blue
colmap[0:71,2] = 1;
colmap[71:128,2]= np.linspace(1,0,57); 
colmap = ListedColormap(colmap)

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
# file_path = "//767-mueller.optics.arizona.edu/Depolarization/Projects/Oculus/Data Sample Library/RGB950 Polarimeter/Measurements/2021/135/20210816_135_451_700ms_f16_All/cmmi/20210816_135_451_700ms_f16_10_20.cmmi"
file_path = "/Users/carolinehumphreys/Desktop/Polarization Lab/2021/135/20210816_135_451_700ms_f16_All/cmmi/20210816_135_451_700ms_f16_10_20.cmmi"
a = readCMMI(file_path)
PlotCMMI(a,-.05,.05)

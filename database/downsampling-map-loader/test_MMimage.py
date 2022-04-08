
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from cmmidataloader import readCMMI
from PIL import Image as im


# creating a dataset
filePath = '/Users/carolinehumphreys/Desktop/Polarization Lab/2021/135/20210816_135_451_700ms_f16_All/cmmi/20210816_135_451_700ms_f16_10_20.cmmi'
mm = readCMMI(filePath)
print(np.shape(mm))

nrows, ncols = 600, 600
for i in range(16):
        MM = mm[i,:,:]
        print(MM[300,300])
        MM = MM.reshape(nrows, ncols)
        print(np.shape(MM))
        print(MM.dtype)
        # convert to float32
        MM = MM.astype(np.float32)
        print(MM.dtype)
        print(MM)

        fig1 = plt.figure(figsize = (15,10))
        plt.imshow(MM,cmap ='hsv',vmin = -0.05,vmax = 0.05)
        # plt.colorbar()
        plt.axis('off')
        plt.title('AoLP')
        cb = plt.colorbar(ticks=[0,45,90,135,180])
        for t in cb.ax.get_yticklabels():
            t.set_fontsize(40)
        plt.show()

  

  

  

import struct
import numpy as np
import tensor
from tensor import write_tensor
from tensor import read_tensor

MM_total = read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')
MM_total['M'][:,:,:,:,:,:] = 0
MM_total['wvls']=np.array([451,525,662,700,750]).astype(np.uint16)
print(MM_total['M'])

# put depolarizing MMs into each place
MM_total['M'][:,:,:,:,0,0]=1
print(MM_total['M'])

A = tensor.read_tensor('/Users/carolinehumphreys/Downloads/6_gold_mitsuba/6_gold_raw.pbsdf')
A['M'] = MM_total['M'];
A['wvls'] = MM_total['wvls'];
tensor.write_tensor("/Users/carolinehumphreys/Desktop/Polarization Lab/2021/001/depolarizingtest.pbsdf",**A);

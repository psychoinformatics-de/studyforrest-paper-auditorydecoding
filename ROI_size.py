import sys
import os
import numpy as np
import nibabel as nib


subject_list=sys.argv[1].split(', ')
mask_name=sys.argv[2]
voxel_count=[]

for subject in subject_list:
    ### load dataset with mask for all runs into a list
    mask_datapath='/home/data/exppsy/spark/Study_Forrest/analysis/masks/'+subject+'/task002'  
    voxel_count.append(float(np.count_nonzero(nib.load(mask_datapath+'/'+mask_name+'.nii.gz').get_data())))
    
print 'mean %f' % np.mean(voxel_count)
print 'std %f' % np.std(voxel_count)

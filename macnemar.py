import sys
import os
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from mvpa2.base.hdf5 import h5load
from mvpa2.misc.stats import binomial_proportion_ci
import math
from scipy.stats import binom
from statsmodels.sandbox.stats.runs import mcnemar

#subject_list=['sub001', 'sub002', 'sub003', 'sub004', 'sub005', 'sub006', 'sub007', 'sub008', 'sub009', 'sub010', 'sub011', 'sub012', 'sub013', 'sub014', 'sub015', 'sub016', 'sub017', 'sub018', 'sub019']
#req_filter='bp'
#fwhm_list=['0', '6']
subject_list=sys.argv[1].split(', ')
req_filter=sys.argv[2]
fwhm_list=sys.argv[3].split(', ')
MVPA_result_folder=sys.argv[4]
mask_name=sys.argv[5]

hits_dict={}

for fwhm in fwhm_list:
    fwhm_hits=[]
    for subject in subject_list:
        data=h5load(MVPA_result_folder+'/'+subject+'_'+mask_name+'_'+req_filter+'_'+str(fwhm)+'.hdf5') 
        fwhm_hits+=list(data.samples[:,0] == data.sa.targets)

	hits_dict[fwhm]=fwhm_hits			

#~ paired_list_of_hits=zip(hits_dict[FWHM_list[0]],hits_dict[FWHM_list[1]])
#~ stat=mcnemar_midp(paired_list_of_hits.count((0, 1)), paired_list_of_hits.count((1, 0)))
stat_pval=mcnemar(hits_dict[fwhm_list[0]], hits_dict[fwhm_list[1]], exact=False, correction=True)
print stat_pval[0]
print stat_pval[1]*len(subject_list)

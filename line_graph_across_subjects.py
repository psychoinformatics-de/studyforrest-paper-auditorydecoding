import sys
import os
import numpy as np
import scipy.stats as stats
import mvpa2.misc.plot as mvpa_plot
import matplotlib.pyplot as plt
from mvpa2.base.hdf5 import h5load
import matplotlib.gridspec as gridspec
import nibabel as nib
from nilearn import image
import math


screen_dpi=400
fig = plt.figure(figsize=(4.0, 3.2), dpi=screen_dpi)


marker_dict = {'hp':'^', \
               'bp':'*', \
               'lp':'o', \
               'bs':'v' }

label_dict = {'hp':'High-Pass', \
              'bp':'Band-Pass', \
              'bs':'Band-Stop', \
              'lp':'Low-Pass'}

color_dict = {'hp':'red', \
              'bp':'black', \
              'bs':'cyan', \
              'lp':'blue'}

old_filter_dict = {'hp':'HPF', \
              'bp':'BPF', \
              'bs':'BSF', \
              'lp':'LPF'}


subject_list=sys.argv[1].split(', ')
filter_types=sys.argv[2].split(', ')
MVPA_result_folder=sys.argv[3]
mask_name=sys.argv[4]

#filter_types=['lp', 'hp', 'bp', 'bs']
#subject_list=['sub001', 'sub002', 'sub003', 'sub004', 'sub005', 'sub006', 'sub007', 'sub008', 'sub009', 'sub010', 'sub011', 'sub012', 'sub013', 'sub014', 'sub015', 'sub016', 'sub017', 'sub018', 'sub019']


for req_filter in filter_types:
    mean_list=[]
    ste_list=[]
    for fwhm in range(21):
        subject_accuracy=[]
        for subject in subject_list:
            data=h5load(MVPA_result_folder+'/'+subject+'_'+mask_name+'_'+req_filter+'_'+str(fwhm)+'.hdf5')
            subject_accuracy.append(float(data.a['confusion'].value.percent_correct))
            ### check data from old dataset
#            old_data=h5load('/home/data/exppsy/Field_Strength_Comparison/analysis/MVPA_auditory/Grey_Auditory_cortex_results/'+subject+'/results/task002/gauss/'+old_filter_dict[req_filter]+'/'+str(fwhm)+'/accuracy.hdf5')
#            if not (float(data.a['confusion'].value.percent_correct)==np.mean(old_data)):
#                print subject
#                print req_filter
#                print fwhm
            
        mean_list.append(np.mean(subject_accuracy))
        ste_list.append(stats.sem(subject_accuracy))
    plt.errorbar(np.arange(1,21), mean_list[1:], ste_list[1:], linestyle='-', marker='.', color=color_dict[req_filter], label=label_dict[req_filter])    
plt.errorbar([0], mean_list[0], ste_list[0], linestyle='None', marker='o', color='gray', label='unfiltered')

plt.legend(loc=3, prop={'size':6}, ncol=1)
plt.axis([-1,21, 18, 87])
#plt.fill_between(np.arange(4.95,8.05, 0.05), 15, 105, facecolor='gray', alpha=0.5)
plt.xticks(np.arange(0, 21, 5), np.arange(0, 21, 5), fontsize=8)
plt.yticks(np.arange(25,87,10), np.arange(25,87,10), fontsize=8)
plt.axhline(y=20, color='black', linestyle='dashed', linewidth=1)

plt.tight_layout()
graph_plots_folder=os.path.abspath(os.path.join(MVPA_result_folder, 'plot_folder'))
if not os.path.exists(graph_plots_folder):
    os.makedirs(graph_plots_folder)

print 'plotted graphs are saved in: '+graph_plots_folder
plt.savefig(os.path.join(graph_plots_folder, 'auditory_consolidated.svg'), dpi=screen_dpi)
#plt.show()

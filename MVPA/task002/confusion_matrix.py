from mvpa2.base.hdf5 import h5load
import matplotlib.pyplot as plt
import numpy as np
import os

###['"ambient"', '"country"', '"metal"', '"rocknroll"', '"symphonic"']
confusion_matrix=np.zeros([5,5])
for sub in range(1,20):
    subject='sub%03d' %sub 
    confusion_folder='/home/data/exppsy/Field_Strength_Comparison/analysis/MVPA_auditory/Grey_Auditory_cortex_confusion_results/'+subject+'/results/task002/gauss/LPF/0'
    confusion_matrix+=h5load(confusion_folder+'/confusion_matrix.hdf5')

confusion_matrix_norm=confusion_matrix/152
cax = plt.matshow(confusion_matrix_norm, interpolation='nearest', cmap='gray', vmin=0, vmax=0.6)
plt.colorbar(cax)
plt.show()
plt.savefig(os.path.join('/home/data/exppsy/Field_Strength_Comparison/analysis/MVPA_auditory', 'LPF_0.svg'))

USAGE:

Please clone the repository into a folder of our choice. After you have downloaded the dataset, 
and change to the subdirectory by issuing the following command from the command line. 

    cd studyforrest-paper-auditorydecoding

Then run the following command will produce the results of the MVPA in the outpur folder of your choice. 


python mvpa_eval_spatial_preproc.py \
            -o out \
            --result-label sub001 lp 5\
            --bold-images /home/data/psyinf/forrest_gump/openfmri.org/sub001/BOLD/task002_run0*/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz \
            --mask /home/data/exppsy/spark/Study_Forrest/analysis/masks/sub001/task002/Grey_Auditory_cortex.nii.gz \
            -m polynomial_order 2 \
            -m behav_file /home/data/psyinf/forrest_gump/openfmri.org/sub001/behav/task002_run0*/behavdata.txt \
            -m motion_file /home/data/psyinf/forrest_gump/openfmri.org/sub001/BOLD/task002_run0*/bold_dico_moco.txt \
            -m run_number 1 2 3 4 5 6 7 8 \
            --fwhm 5 \
            --filter-type lp \
            --mkds code-spatial_preproc/MVPA/task002/create_evds.py \
            --clf code-spatial_preproc/MVPA/task002/clf.py \
            --tune-hyperparam code-spatial_preproc/MVPA/task002/tune_test_values.py


### All the following commands need to be run from '/home/data/exppsy/spark/Study_Forrest/analysis' location


bash code-spatial_preproc/condor/run_MVPA.sh 'sub001, sub002, sub003, sub004, sub005, sub006, sub007, sub008, sub009, sub010, sub011, sub012, sub013, sub014, sub015, sub016, sub017, sub018, sub019' 'task002' 'Grey_Auditory_cortex'

python code-spatial_preproc/line_graph_across_subjects.py

python code-spatial_preproc/macnemar.py

python code-spatial_preproc/ROI_size.py 'sub001, sub002, sub003, sub004, sub005, sub006, sub007, sub008, sub009, sub010, sub011, sub012, sub013, sub014, sub015, sub016, sub017, sub018, sub019' Grey_Auditory_cortex

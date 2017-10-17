### All the following commands need to be run from '/home/data/exppsy/spark/Study_Forrest/analysis' location


bash code-spatial_preproc/condor/run_MVPA.sh 'sub001, sub002, sub003, sub004, sub005, sub006, sub007, sub008, sub009, sub010, sub011, sub012, sub013, sub014, sub015, sub016, sub017, sub018, sub019' 'task002' 'Grey_Auditory_cortex'

python code-spatial_preproc/line_graph_across_subjects.py

python code-spatial_preproc/macnemar.py

python code-spatial_preproc/ROI_size.py 'sub001, sub002, sub003, sub004, sub005, sub006, sub007, sub008, sub009, sub010, sub011, sub012, sub013, sub014, sub015, sub016, sub017, sub018, sub019' Grey_Auditory_cortex

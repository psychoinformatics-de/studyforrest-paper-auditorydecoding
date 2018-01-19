USAGE:

Please clone the repository into a folder of our choice. After you have downloaded the dataset, 
and change to the subdirectory by issuing the following command from the command line. 

    cd studyforrest-paper-auditorydecoding

Then run the following command will produce the results of the MVPA in the output folder of your choice. 


    python mvpa_eval_spatial_preproc.py \
            -o <output folder> \
            --result-label <subject-ID> <filter type> <FWHM>\
            --bold-images <dataset_folder>/<subject-ID>/BOLD/task002_run0*/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz \
            --mask <subject specific mask image> \
            -m polynomial_order 2 \
            -m behav_file <dataset_folder>/<subject-ID>/behav/task002_run0*/behavdata.txt \
            -m motion_file <dataset_folder>/<subject-ID>/BOLD/task002_run0*/bold_dico_moco.txt \
            -m run_number 1 2 3 4 5 6 7 8 \
            --fwhm <FWHM> \
            --filter-type <filter type> \
            --mkds MVPA/task002/create_evds.py \
            --clf MVPA/task002/clf.py \
            --tune-hyperparam MVPA/task002/tune_test_values.py



    <output folder>: where you want to save the output of the MVPA
    <subject-ID>: subject ID of the particular participant eg: sub001
    <filter type>: EIther of 'lp, hp, bp, bs' standing for low-pass, high-pass, band-pass, band-stop filters              
    <FWHM>: Full-width half maxima of the Gaussian filters
    <dataset_folder>: location where the Openfmri dataset is downloaded
    <subject specific mask image>: ROI mask image of the particular participant 


For generating the mean and std. deviation of the ROI mask sizes across the subjects please use the following command:

    python code-spatial_preproc/ROI_size.py <list-of-subjects> <path-to-ROI> <ROI-mask>

    Example Run: python code-spatial_preproc/ROI_size.py 'sub001, sub002' 'analysis/masks' 'Grey_Auditory_cortex'


For generating the plot of decoding accuracies across different levels of spatial smoothing across subjects, please use the following command:

    python code-spatial_preproc/line_graph_across_subjects.py <list-of-subjects> <list-of-filter-types> <MVPA-output-folder> <ROI-mask>

    Example Run: code-spatial_preproc/line_graph_across_subjects.py 'sub001, sub002' 'LP, BP' 'analysis/MVPA_auditory_results' 'Grey_Auditory_cortex'


For running macnemar test between 2 levels of spatial smoothing data points, please use the following command:

    python code-spatial_preproc/macnemar.py <list-of-subjects> <filter-type> <FWHM-levels> <MVPA-output-folder> <ROI-mask>

    Example Run: code-spatial_preproc/macnemar.py 'sub001, sub002' 'BP' '2, 7' 'analysis/MVPA_auditory_results' 'Grey_Auditory_cortex'



If 'condor' is installed on a linux system, the following bash script could also be used to generate the MVPA result dataset.
 
bash code-spatial_preproc/condor/run_MVPA.sh 'sub001, sub002, sub003, sub004, sub005, sub006, sub007, sub008, sub009, sub010, sub011, sub012, sub013, sub014, sub015, sub016, sub017, sub018, sub019' 'task002' 'Grey_Auditory_cortex'

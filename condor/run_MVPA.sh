#!/bin/bash

. /etc/fsl/5.0/fsl.sh

set -e
set -u


###input argument description
# 1. filename of the condor script to be edited
# 2. subject id
# 3. task id

subject_list="$1"
req_task_list="$2"
mask_image_list="$3"
#filename="$4"


condor_script="code-spatial_preproc/condor/auditory_MVPA_filtering.submit"
condor_output_folder="condor_output/auditory_MVPA"

###initialize environment in condor submit file
initialization_string="universe = vanilla
executable=/usr/bin/python2.7
initialdir = /home/data/exppsy/spark/Study_Forrest/analysis
request_cpus = 1
request_memory = 8000
getenv = True"


#MVPA_call='code-spatial_preproc/mvpa_eval_spatial_preproc.py \
#            -o /home/data/exppsy/spark/Study_Forrest/analysis/MVPA_results \
#            --result-label subject req_mask req_filter FWHM \
#            --bold-images ""/home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run0*/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz"" \
#            --mask /home/data/exppsy/spark/Study_Forrest/analysis/masks/subject/req_task/req_mask.nii.gz \
#            -m polynomial_order 2 \
#            -m behav_file ""/home/data/psyinf/forrest_gump/openfmri.org/subject/behav/req_task_run0*/behavdata.txt"" \
#            -m motion_file ""/home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run0*/bold_dico_moco.txt"" \
#            -m run_number 1 2 3 4 5 6 7 8 \
#            --fwhm FWHM \
#            --filter-type req_filter \
#            --mkds code-spatial_preproc/MVPA/req_task/create_evds.py \
#            --clf code-spatial_preproc/MVPA/req_task/clf.py \
#            --tune-hyperparam code-spatial_preproc/MVPA/req_task/tune_test_values.py'



MVPA_call='code-spatial_preproc/mvpa_eval_spatial_preproc.py -o /home/data/exppsy/spark/Study_Forrest/analysis/MVPA_results --result-label subject req_mask req_filter FWHM --bold-images /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run001/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run002/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run003/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run004/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run005/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run006/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run007/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run008/bold_dico_bold7Tp1_to_subjbold7Tp1.nii.gz --mask /home/data/exppsy/spark/Study_Forrest/analysis/masks/subject/req_task/req_mask.nii.gz -m polynomial_order 2 -m behav_file /home/data/psyinf/forrest_gump/openfmri.org/subject/behav/req_task_run001/behavdata.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/behav/req_task_run002/behavdata.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/behav/req_task_run003/behavdata.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/behav/req_task_run004/behavdata.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/behav/req_task_run005/behavdata.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/behav/req_task_run006/behavdata.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/behav/req_task_run007/behavdata.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/behav/req_task_run008/behavdata.txt -m motion_file /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run001/bold_dico_moco.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run002/bold_dico_moco.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run003/bold_dico_moco.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run004/bold_dico_moco.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run005/bold_dico_moco.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run006/bold_dico_moco.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run007/bold_dico_moco.txt /home/data/psyinf/forrest_gump/openfmri.org/subject/BOLD/req_task_run008/bold_dico_moco.txt -m run_number 1 2 3 4 5 6 7 8 --fwhm FWHM --filter-type req_filter --mkds code-spatial_preproc/MVPA/req_task/create_evds.py --clf code-spatial_preproc/MVPA/req_task/clf.py --tune-hyperparam code-spatial_preproc/MVPA/req_task/tune_test_values.py'


echo "$initialization_string" > $condor_script


IFS=', ' read -a subject_array <<< "$subject_list"
IFS=', ' read -a task_array <<< "$req_task_list"
IFS=', ' read -a mask_array <<< "$mask_image_list"
declare -a filter_type=('lp' 'hp' 'bp' 'bs')

for mask in "${mask_array[@]}"; do
    for subject in "${subject_array[@]}"; do
        echo 'Processing : ' $subject
        for task in "${task_array[@]}"; do
            for filter in "${filter_type[@]}"; do        
                for FWHM in {0..20}; do
                    echo $subject

                    echo "arguments = \"$MVPA_call\"" | sed -e s/'subject'/$subject/g -e s/'req_task'/$task/g -e s/'req_filter'/$filter/g -e s/'FWHM'/$FWHM/g -e s/'req_mask'/$mask/g >> $condor_script
                    echo "error  = $condor_output_folder/$subject.$filter.$FWHM.err" >> $condor_script
                    echo "output = $condor_output_folder/$subject.$filter.$FWHM.out" >> $condor_script
                    echo "log = $condor_output_folder/$subject.$filter.$FWHM.log" >> $condor_script
                    echo "Queue" >> $condor_script



                done
            done
        done
    done
done

condor_submit $condor_script
watch condor_q spark




















###subject_list=$1
###session_list="$2"
###pval="$3"
###zthresh="$4"
###filename="$5"
###fsf_folder="GLM/fsf_folder"
###fsf_file=$fsf_folder"/"$filename
###condor_script="code/condor/run_GLM.submit"
###condor_output_folder="condor_output/GLM"
###mkdir -p $condor_output_folder
###rm -f $condor_script

######initialize environment in condor submit file
###initialization_string="universe = vanilla
###executable = /usr/bin/fsl5.0-feat
###initialdir = /home/data/psyinf/multires7T/analysis
###request_cpus = 1
###request_memory = 8000
###getenv = True"


###echo "$initialization_string" > $condor_script


###IFS=', ' read -a subject_list <<< "$subject_list"
###IFS=', ' read -a session_list <<< "$session_list"


###for subject in "${subject_list[@]}"; do
###    echo 'Processing : ' $subject

###    for session in "${session_list[@]}"; do
###        ###if [ $filename != 'design_level_2.fsf' ]; then
###        if [ $filename != 'design_surface_level_2.fsf' ]; then     
###            for run_id in {1..10}; do
###                #run_folder=$fsf_folder"/"$subject"/"$session"/task-orientation_run-$(zeropad $run_id 2)"
###                mkdir -p $fsf_folder'/'$subject'/'$session
###                run_fsf_file=$fsf_folder"/"$subject"/"$session"/task-orientation_run-$(zeropad $run_id 2)_"$filename
###                cp $fsf_file $run_fsf_file
###                sed -i s/'sub'/$subject/g $run_fsf_file
###                sed -i s/'sess'/$session/g $run_fsf_file
###                sed -i s/'run'/"run-$(zeropad $run_id 2)"/g $run_fsf_file
###                sed -i s/'pval'/$pval/g $run_fsf_file
###                sed -i s/'zthresh'/$zthresh/g $run_fsf_file
###                #~ 
###                #~ 
###                echo "arguments = $run_fsf_file" >> $condor_script
###                echo "error  = $condor_output_folder/$subject.$session.$run_id.err" >> $condor_script
###                echo "output = $condor_output_folder/$subject.$session.$run_id.out" >> $condor_script
###                echo "log = $condor_output_folder/$subject.$session.$run_id.log" >> $condor_script
###                echo "Queue" >> $condor_script
###            done
###        else
###            #run_folder=$fsf_folder"/"$subject"/"$session"/task-orientation_run-$(zeropad $run_id 2)"
###            mkdir -p $fsf_folder'/'$subject'/'$session
###            level2_fsf_file=$fsf_folder"/"$subject"/"$session"/"$filename
###            cp $fsf_file $level2_fsf_file
###            sed -i s/'sub'/$subject/g $level2_fsf_file
###            sed -i s/'sess'/$session/g $level2_fsf_file
###            sed -i s/'pval'/$pval/g $level2_fsf_file
###            sed -i s/'zthresh'/$zthresh/g $level2_fsf_file
###            #~ 
###            #~ 
###            echo "arguments = $level2_fsf_file" >> $condor_script
###            echo "error  = $condor_output_folder/$subject.$session.err" >> $condor_script
###            echo "output = $condor_output_folder/$subject.$session.out" >> $condor_script
###            echo "log = $condor_output_folder/$subject.$session.log" >> $condor_script
###            echo "Queue" >> $condor_script        
###    
###        fi
###    done
###done

###condor_submit $condor_script
####watch condor_q spark



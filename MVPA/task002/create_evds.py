from mvpa2.suite import eventrelated_dataset, zscore
import numpy as np

def fx(dataset, behav_file, motion_file, polynomial_order,
       run_number):
    print("events      ->  %s" % behav_file)
    print("nuisance    ->  %s" % motion_file)

    tsds = dataset
    behav_txt = np.recfromcsv(behav_file, delimiter=',')
    events = [dict(
              onset=float(event['run_volume']) * 2.0,
              duration=6.0,
              targets=event['genre'],
              chunks=int(event['run']),
              stim=event['stim'])
              for event in behav_txt]

    motion = np.loadtxt(motion_file)

    add_reg_names = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
    hrf_estimates = eventrelated_dataset(
        tsds,
        events,
        model='hrf',
        time_attr='time_coords',
        condition_attr=(('targets', 'chunks')),
        design_kwargs=dict(
            drift_model='polynomial',
            drift_order=polynomial_order,
            hrf_model='canonical with derivative',
            add_regs=motion,
            add_reg_names=add_reg_names),
        glmfit_kwargs=dict(model='ar1'))

    #hrf_estimates.sa['subj'] = [subject] * len(hrf_estimates)
    hrf_estimates.sa['run'] = [run_number] * len(hrf_estimates)

    # zscore voxelwise
    # XXX `hrf_estimates` has no chunks! hence zscoring is not performed run-wise!
    zscore(hrf_estimates)
    return hrf_estimates

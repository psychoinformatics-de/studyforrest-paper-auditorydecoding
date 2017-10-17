#!/usr/bin/python
from __future__ import print_function

import sys
import os
from os.path import join as opj
from os.path import basename
import argparse

import numpy as np
from nilearn import image
import nibabel as nib

from mvpa2.suite import LinearCSVMC
from mvpa2.suite import SMLR
from mvpa2.suite import CrossValidation
from mvpa2.suite import NFoldPartitioner
from mvpa2.suite import mean_match_accuracy
from mvpa2.suite import LearnerError
from mvpa2.suite import FeatureSelectionClassifier
from mvpa2.suite import fmri_dataset
from mvpa2.suite import SensitivityBasedFeatureSelection
from mvpa2.suite import OneWayAnova
from mvpa2.suite import FractionTailSelector
from mvpa2.suite import Splitter
from mvpa2.suite import TransferMeasure
from mvpa2.suite import BinaryFxNode
from mvpa2.suite import h5save
from mvpa2.suite import vstack
from mvpa2.suite import ConfusionMatrix

from mvpa2.cmdline.helpers import script2obj


#
# Helper functions
#

def gaussian_spatial_filter(img, ftype, fwhm, bandwidth=1):
    """
    Parameters
    ----------
    img : image(-series)
    ftype : str
      Filter type label (LP, HP, BP, BS).
    fwhm : float
      Size of the base Gaussian kernel (in mm)
    bandwidth : float
      FWHM difference of the second Gaussian in the difference-of-Gaussians
      band pass/stop filter pair. The second filter size is determined by
      subtracting this value from the base kernel FWHM.
    """
    if not fwhm > 0:
        return img

    # TODO somewhere we should support pre _and_ post masking

    if ftype.lower() == 'lp':
        print("Creating Spatially low pass filtered image")
        img = image.smooth_img(img, fwhm=fwhm)

    elif ftype.lower() == 'hp':
        print("Creating Spatially high pass filtered image")
        LPF_bold = image.smooth_img(orig_bold, fwhm=fwhm)
        HPF_bold = img.get_data() - LPF_bold.get_data()
        img = nib.nifti1.Nifti1Image(HPF_bold, img.get_affine())

    elif ftype.lower() == 'bp':
        print("Creating Spatially Band pass filtered image")
        LPF_bold_1 = image.smooth_img(img, fwhm=fwhm)
        LPF_bold_2 = image.smooth_img(img, fwhm=fwhm - bandwidth)
        BPF_bold = LPF_bold_2.get_data() - LPF_bold_1.get_data()
        img = nib.nifti1.Nifti1Image(BPF_bold, img.get_affine())

    elif ftype.lower() == 'bs':
        print("Creating Spatially Band stop filtered image")
        LPF_bold_1 = image.smooth_img(img, fwhm=fwhm)
        LPF_bold_2 = image.smooth_img(img, fwhm=fwhm - bandwidth)
        BPF_bold = LPF_bold_2.get_data() - LPF_bold_1.get_data()
        BSF_bold = img.get_data() - BPF_bold
        img = nib.nifti1.Nifti1Image(BSF_bold, img.get_affine())
    else:
        raise ValueError('unknown filter type: {}'.format(ftype))

    return img


def optimize_clf_hyperparam(ds, clf, target_attr, chunk_attr, test_values):
    best_accuracy = None
    best_val = None
    for val in test_values:
        clf = clf(target_attr, val)
        cv = CrossValidation(
            clf,
            NFoldPartitioner(attr=chunk_attr),
            errorfx=mean_match_accuracy,
            enable_ca=['stats'])

        try:
            accuracy = np.mean(cv(ds))
        except LearnerError as e:
            # XXX we should not ignore that without a message
            continue

        if best_accuracy is None or accuracy > best_accuracy:
            best_val = val
            best_accuracy = accuracy

    return best_val


#
# cmdline arguments
#
parser = argparse.ArgumentParser(add_help=True)
parser.add_argument(
    '-i', '--bold-images', nargs='+', metavar='PATH', required=True)
parser.add_argument(
    '-o', '--output-directory', metavar='PATH', required=True, dest='output_dir')
parser.add_argument(
    '--mask', metavar='PATH', default=None)
parser.add_argument(
    '--clf', required=True, dest='clf', type=script2obj)
parser.add_argument(
    '--fwhm', default=0.0, type=float, metavar='SIZE (mm)')
parser.add_argument(
    '--dog-bandwidth', default=1.0, type=float, metavar='<size difference in FWHM (mm)>')
parser.add_argument(
    '-f', '--filter-type', default='none', choices=['lp', 'hp', 'bp', 'bs', 'none'])
parser.add_argument(
    '-l', '--result-labels', nargs='+', required=True, metavar='LABEL')
parser.add_argument(
    '-m', '--mkds-arg', action='append', nargs='+', metavar='ARG')
parser.add_argument(
    '-t', '--target-attr', default='targets', metavar='NAME')
parser.add_argument(
    '-c', '--chunk-attr', default='chunks', metavar='NAME')
parser.add_argument(
    '--mkds', required=True, metavar='PATH', type=script2obj)
parser.add_argument(
    '--tune-hyperparam', metavar='PATH', type=script2obj)

try:
    import argcomplete
    argcomplete.autocomplete(parser)
except ImportError:
    pass

args = parser.parse_args()

mkds_args = {}
if args.mkds_arg:
    nbold = len(args.bold_images)
    # we got some mkds arguments, this will always be a list
    for pa in args.mkds_arg:
        argname = pa[0]
        if len(pa) == 1:
            # enable a flag with the given name
            mkds_args[argname] = [True] * nbold
        elif len(pa) == 2:
            # enable a flag with the given name
            mkds_args[argname] = [pa[1]] * nbold
        else:
            if not len(pa) == nbold + 1:
                raise ValueError(
                    'number of arguments {} for "{}" does not match number of bold images: {}'.format(
                        len(pa) - 1, argname, nbold))
            mkds_args[argname] = pa[1:]

#
# output preparation
#

# create output folders of needed
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

#
# all run-wise processing in here
#

ds_list = []  # run-wise dataset list

for run_id, bold_filename in enumerate(args.bold_images):
    # TODO the inside of this loop could be perform in parallel
    # maybe Rf into a dedicated script, the resulting ds are
    # pretty small in file size

    print("bold_image  ->  %s" % bold_filename)
    print("mask_image  ->  %s" % args.mask)
    print("Filter_sel  ->  %s" % args.filter_type)
    print("FWHM        ->  %d" % args.fwhm)

    orig_bold = nib.load(bold_filename)

    if args.filter_type == 'none':
        fmri_img = orig_bold
    else:
        fmri_img = gaussian_spatial_filter(
        orig_bold,
        ftype=args.filter_type,
        fwhm=args.fwhm,
        bandwidth=args.dog_bandwidth)

    tsds = fmri_dataset(fmri_img, mask=args.mask)
    # load original data to get actual timing info, and avoid potential
    # problems from pre-processing above
    tsds.sa.time_coords = fmri_dataset(bold_filename).sa.time_coords

    # post-process time series dataset -- possibly modeling
    run_mkds_args = {k: v[run_id] for k, v in mkds_args.items()}
    ds = args.mkds(tsds, **run_mkds_args)
    for attr in ('target', 'chunk'):
        attr_val = getattr(args, '{}_attr'.format(attr))
        if attr_val not in ds.sa.keys():
            raise RuntimeError(
                '{} "{}" not found in dataset attributes: {}"'.format(
                    attr, attr_val, ds.sa.keys()))
    ds_list.append(ds)

#merge ds across runs
dataset = vstack(ds_list, a=0)

#
# analysis setup
# TODO: possible Rf into a plugin to allow for other types
#

# collect raw predictions, so we can compute a McNemar test easily
# without any reconstruction of binomial results
results = []
# use a confusion matrix to collect all results in multiple sets,
# one for each data fold
confusion = ConfusionMatrix(labels=list(dataset.sa[args.target_attr].unique))

partitioner = NFoldPartitioner(attr=args.chunk_attr)

# possibly nested cross validation
# TODO make fold generation more flexible
splitter = Splitter('partitions')
for isplit, partitions in enumerate(partitioner.generate(dataset)):
    dstrain, dstest = list(splitter.generate(partitions))

    if args.tune_hyperparam:
        tuned_par = optimize_clf_hyperparam(
            dstrain,
            args.clf,
            args.target_attr,
            args.chunk_attr,
            args.tune_hyperparam())
        clf = args.clf(args.target_attr, tuned_par)
    else:
        clf = args.clf(args.target_attr)

    tm = TransferMeasure(clf, splitter)
    res = tm(partitions)
    # make a record of the tuned hyper parameter for comprehensive
    # reporting
    if args.tune_hyperparam:
        res.a['tuned_hyperparam'] = tuned_par
    results.append(res)
    # feed predictions into the confusion tracker as a new set
    confusion.add(res.sa[args.target_attr].value, res.samples[:, 0])

# one result dataset
results = vstack(results, a='all')
# report analysis params for the afterlife
results.a['confusion'] = confusion
results.a['mask'] = args.mask
results.a['fwhm'] = args.fwhm
results.a['dog_bandwidth'] = args.dog_bandwidth
results.a['filter_type'] = args.filter_type
for k, v in mkds_args.items():
    results.a['mkds_{}'.format(k)] = v

# brag about it
print(results)
print(confusion)

# safe to disk
h5save(
    opj(
        args.output_dir,
        '_'.join(args.result_labels) + '.hdf5'),
    results)

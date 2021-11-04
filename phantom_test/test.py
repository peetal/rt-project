from subprocess import call
import sys, os


#test_struc = Struc('0414151_strongbad01014_*', '/Users/peetal/Desktop/example_dicom', '/Users/peetal/Documents/Github/rt-cloud/projects/phantom_test', 'sub_test')
#test_struc.run_sub_struc_preprocessing()



#dicom_pattern = '0414151_strongbad01005_{TR:04d}_001'
#dicom_dir = '/Users/peetal/Desktop/example_dicom'
#code_dir = '/Users/peetal/Documents/Github/rt-cloud/projects/phantom_test'
#subj_id = 'sub_test'


#test_func = func(dicom_pattern, 6, dicom_dir, code_dir, subj_id)
#test_func._dcm2nifti()
#test_func._creat_ref_bold()
#time3 = test_func._linear_registration(useFastSeg=False)
#print(time3)

import os
import sys
import struct
import logging
import argparse
import numpy as np
from preprocessing_func import Struc, RefBOLD, ProcessNewVol
from initialize import initialize_cfg
from utils import read_nifti, getOutputFilename, applymask

# obtain full path for current directory: '.../rt-cloud/projects/sample'
currPath = os.path.dirname(os.path.realpath(__file__))
# obtain full path for root directory: '.../rt-cloud'
rootPath = os.path.dirname(os.path.dirname(currPath))

# add the path for the root directory to your python path so that you can import
#   project modules from rt-cloud
sys.path.append(rootPath)
# import project modules from rt-cloud
import rtCommon.utils as utils
from rtCommon.clientInterface import ClientInterface
from rtCommon.dataInterface import uploadFilesToCloud
from rtCommon.imageHandling import getTransform

defaultConfig = os.path.join(currPath, 'conf/phantom_test.toml')
cfg = utils.loadConfigFile(defaultConfig)
cfg = initialize_cfg(cfg)
#print(cfg.roi_standard2func_nonlinear)



#dcm_eg = '0414151_strongbad01006_0003_001'
#test_reg = Nifti2MNI(dcm_eg, cfg)

#test_reg.register_new_nifti(mc = True)

#dicomScanNamePattern_refbold = utils.stringPartialFormat(cfg.dicomNamePattern, 'SCAN', cfg.refBoldScanNum)
#print(dicomScanNamePattern_refbold)
#sub_refbold = RefBOLD(dicomScanNamePattern_refbold, 6, cfg.dicomDir, cfg.codeDir, cfg.subjectName, linear=False, useFastSeg=True)
#sub_refbold.apply_transformation_info()

#roi1 = '/Users/peetal/Documents/Github/rt-cloud/projects/phantom_test/data/roi/rsc_roi_big_resampled.nii.gz'
#sub_refbold.ROI_standard2func(roi1)
#roi2 = '/Users/peetal/Documents/Github/rt-cloud/projects/phantom_test/data/roi/rsc_roi_small_resampled.nii.gz'
#sub_refbold.ROI_standard2func(roi2)

#print(np.sum(read_nifti("/Users/peetal/Documents/Github/rt-cloud/projects/phantom_test/data/sub_test/roi_standard2func/rsc_roi_big_resampled_2func_nonlinear.nii.gz")))
 

#print(np.sum(read_nifti("/Users/peetal/Documents/Github/rt-cloud/projects/phantom_test/data/roi/rsc_roi_big.nii.gz")))

data = read_nifti('/Users/peetal/Documents/Github/rt-cloud/projects/phantom_test/data/sub_test/func_nii/ref_bold/refBOLD_avg.nii.gz', get_data=False)
roi = read_nifti('/Users/peetal/Documents/Github/rt-cloud/projects/phantom_test/data/sub_test/roi_standard2func/rsc_roi_big_resampled_2func_nonlinear.nii.gz')
#check = applymask(data, roi)
print(np.sum(roi))

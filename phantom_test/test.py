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
from utils import read_nifti, getOutputFilename, applymask, config_run_dir

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

defaultConfig = os.path.join(currPath, 'conf/phantom_test_local.toml')
cfg = utils.loadConfigFile(defaultConfig)
cfg = initialize_cfg(cfg)
print(cfg.beh)

cfg = config_run_dir(cfg, 1)
#print(os.path.isdir("/Users/peetal/Documents/Github/rt-cloud/projects/phantom_test/data/sub_test2/sesson1/beh/run1"))
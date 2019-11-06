# ------------------------------------------------------------------------------------------------------------
#   Preprocessing pipeline
# ---------------------------------
#   - incorporates:
#         - registration
#         - anisotropic filter
#         - skull stripping
#         - bias field
#
# ------------------------------------------------------------------------------------------------------------

import os
import sys
import platform
import time
import ConfigParser 
from utils.preprocess import preprocess_scan
CURRENT_PATH = CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(CURRENT_PATH, 'libs'))

import json


def preprocess():
    
    options= {}
     
    #LOADs FROM NicMSLesion
    options['niftyreg_path'] = CURRENT_PATH + '/third_s/nicMSlesions/libs/linux/niftyreg'
    options['robex_path'] = CURRENT_PATH + '/third_s/nicMSlesions/libs/linux/ROBEX/runROBEX.sh'
    
    #LOADs FROM MNI
    options['MNI_Template'] = CURRENT_PATH + '/third_s/MNI_Template/icbm_avg_152_t1_tal_lin.nii.gz'
    
    #Original from NicMSLesion
    options['denoise_iter'] = 3

    #get the paths of images from json
    with open('data.json', 'r') as f:
    	data = json.load(f)
        for i, data_dict in enumerate(data):
            #path of pre-process images
            
            options['T1'] = data_dict['path_T1']
            options['T2'] = data_dict['path_T2']
            options['FLAIR'] = data_dict['path_FLAIR']
            options['MASK'] = data_dict['path_lesion']
            
            #get the final name image (original = path original, tmp_folder = pre-process folder)
            options['modalities'] = (options['T1'].split("/")[-1] + "/" + options['T2'].split("/")[-1] + "/" + options['FLAIR'].split("/")[-1]).split("/")
            options['modalities'].sort()
            
            options['original'] = data_dict['path_T1'].split("/")[:-1]
            options['original'] = '/'.join([str(elem) for elem in options['original']]) 
            
            options['tmp_folder'] = CURRENT_PATH + '/pre/' + options['original'] + "/"
            options['original'] = CURRENT_PATH + "/" + options['original'] + "/"
            
            options['pre_mask'] = data_dict['path_lesion'].split("/")[:-1]
            options['pre_mask'] = '/'.join([str(elem) for elem in options['pre_mask']]) 
            options['pre_mask'] = CURRENT_PATH + '/pre/' + options['pre_mask']

            options['mask'] = CURRENT_PATH + '/' + data_dict['path_lesion']
            
           
            #path of personal computer
            options['datasets'] = sys.argv[1]
            
            total_time = time.time()

            #just to informate the actual folder in operation             
            options['tmp_scan'] = options['original']
            options['tmp_scan'] = options['tmp_scan'].split("/")[-5:-2]
            
            #folder to raw images
            current_folder = options['datasets'] + "/" + data_dict["path_T1"]
    
            # preprocess scan
            preprocess_scan(current_folder, options)

    return options
if __name__ == '__main__':
    preprocess()
    print("Done")


# ------------------------------------------------------------------------------------------------------------
#   Preprocessing pipeline
# ---------------------------------
#   - incorporates:
#         - MRI identification
#         - registration
#         - skull stripping
#
# ------------------------------------------------------------------------------------------------------------

import os
import sys
import platform
import time
import ConfigParser
from utils.preprocess import preprocess_scan
from utils.load_options import load_options, print_options
CURRENT_PATH = CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(CURRENT_PATH, 'libs'))

import json


def get_config():
    """
    Get the configurations from file
    """
    print('Remember to set config/configuration.cfg tags!!!')
    user_config = ConfigParser.ConfigParser()
    user_config.read(os.path.join(CURRENT_PATH, 'config', 'configuration.cfg'))

    # read user's configuration file
    options = load_options(user_config)
    #options['tmp_folder'] = CURRENT_PATH + '/tmp'
    #options['tmp_folder'] = CURRENT_PATH +"/"+ data_dict['path_T1_pre']
    # if len(sys.argv) > 1:
    #     options['datasets'] = sys.argv[1] + "/" +data_dict["path_T1"]
    # else:
    #     print('How to use: python rafa_script.py /folder/to/images')

    # set paths taking into account the host OS
    host_os = platform.system()
    if host_os == 'Linux':
        options['niftyreg_path'] = CURRENT_PATH + '/libs/linux/niftyreg'
        options['robex_path'] = CURRENT_PATH + '/libs/linux/ROBEX/runROBEX.sh'
        options['test_slices'] = 256
    else:
        print "The OS system", host_os, "is not currently supported."
        exit()

    # print options when debugging
    if options['debug']:
        print_options(options)

    return options


def preprocess(options):
    
    j=0
    options['MNI_Template'] = os.path.normpath(os.path.join(os.getcwd(),'MNI_Template/icbm_avg_152_t1_tal_lin.nii.gz'))
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

            # --------------------------------------------------
            # move things to a tmp folder before starting
            # --------------------------------------------------

            #imagens             
            #options['tmp_scan'] = options['tmp_folder']
            options['tmp_scan'] = data_dict['path_T1_pre']
            options['tmp_scan'] = options['tmp_scan'].split("/")[-3:-2]
            #print(type(options['tmp_folder']))
            
            #pasta das imagens originais
            current_folder = options['datasets'] + "/" + data_dict["path_T1"] 
            # preprocess scan
            preprocess_scan(current_folder, options)

if __name__ == '__main__':
    preprocess(get_config())
    print("Done")


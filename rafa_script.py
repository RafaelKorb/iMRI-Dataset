
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
    options['tmp_folder'] = CURRENT_PATH + '/pre'
    
    if len(sys.argv) > 1:
        options['datasets'] = sys.argv[1]
    else:
        print('How to use: python rafa_script.py /folder/to/images')

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
    scan_list = os.listdir(options['datasets'])
    scan_list.sort()

    options['task'] = 'training'
    options['datasets'] = os.path.normpath(options['datasets'])

    options['MNI_Template'] = os.path.normpath(os.path.join(os.getcwd(),'MNI_Template/icbm_avg_152_t1_tal_lin.nii'))
    for scan in scan_list:

        total_time = time.time()

        # --------------------------------------------------
        # move things to a tmp folder before starting
        # --------------------------------------------------

        options['tmp_scan'] = scan
        current_folder = os.path.join(options['datasets'], scan)
        options['tmp_folder'] = os.path.normpath(os.path.join(current_folder,
                                                              'pre'))

        # preprocess scan
        preprocess_scan(current_folder, options)

if __name__ == '__main__':
    preprocess(get_config())
    print("Done")
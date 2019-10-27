import os
import shutil
import sys
import signal
import subprocess
import time
import platform
import nibabel as nib
import numpy as np
from medpy.filter.smoothing import anisotropic_diffusion as ans_dif


def get_mode(input_data):
    """
    Get the stastical mode
    """
    (_, idx, counts) = np.unique(input_data,
                                 return_index=True,
                                 return_counts=True)
    index = idx[np.argmax(counts)]
    mode = input_data[index]

    return mode

def parse_input_masks(current_folder, options):
    """
    identify input image masks parsing image name labels
    Check for input modalities. If lesiomask is not found, the mask
    is ignored

    """

    # if options['task'] == 'training':
    #     modalities = options['modalities'][:] + ['lesion']
    #     image_tags = options['image_tags'][:] + options['roi_tags'][:]
    # else:
    #     modalities = options['modalities'][:]
    #     image_tags = options['image_

    modalities = options['modalities'][:]
    image_tags = options['image_tags'][:]

    if options['debug']:
        print "> DEBUG:", "number of input sequences to find:", len(modalities)

    scan = options['tmp_scan']
    print "> PRE:", scan, "identifying input modalities"
    found_modalities = 0

    masks = [m for m in os.listdir(current_folder) if m.find('.nii') > 0]

    for t, m in zip(image_tags, modalities):

        # check first the input modalities
        # find tag

        found_mod = [mask.find(t) if mask.find(t) >= 0
                     else np.Inf for mask in masks]

        if found_mod[np.argmin(found_mod)] is not np.Inf:
            found_modalities += 1
            index = np.argmin(found_mod)
            # generate a new output image modality
            # check for extra dimensions
            input_path = os.path.join(current_folder, masks[index])
            input_sequence = nib.load(input_path)
            input_image = np.squeeze(input_sequence.get_data())
            output_sequence = nib.Nifti1Image(input_image,
                                              affine=input_sequence.affine)
            output_sequence.to_filename(
                os.path.join(options['tmp_folder'], m + '.nii.gz'))

            if options['debug']:
                print "    --> ", masks[index], "as", m, "image"
            masks.remove(masks[index])

    # check that the minimum number of modalities are used
    if found_modalities < len(modalities):
        print "> ERROR:", scan, \
            "does not contain all valid input modalities"
        sys.stdout.flush()
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)

    # check if lesion mask exists, and if not, save an empty mask
    # with same shape as T1-w

    t = options['mask_tags'][0]
    m = 'lesion'

    masks = [mask for mask in os.listdir(current_folder) if mask.find('.nii') > 0]
    found_mod = [mask.find(t) if mask.find(t) >= 0
                     else np.Inf for mask in masks]

    if found_mod[np.argmin(found_mod)] is not np.Inf:
        index = np.argmin(found_mod)
        # generate a new output image modality
        # check for extra dimensions
        input_path = os.path.join(current_folder, masks[index])
        input_sequence = nib.load(input_path)
        input_image = np.squeeze(input_sequence.get_data())
        output_sequence = nib.Nifti1Image(input_image,
                                          affine=input_sequence.affine)
        output_sequence.to_filename(
            os.path.join(options['tmp_folder'], m + '.nii.gz'))

        if options['debug']:
            print "    --> ", masks[index], "as", m, "image"
            masks.remove(masks[index])
    else:
        #ref_scan = nib.load(os.path.join(current_folder, 'tmp', 'T1.nii.gz'))
        ref_scan = nib.load(os.path.join(current_folder, 'data', 'T1.nii.gz'))
        input_image = np.zeros_like(ref_scan.get_data())
        output_sequence = nib.Nifti1Image(input_image,
                                          affine=ref_scan.affine)
        output_sequence.to_filename(
            os.path.join(options['tmp_folder'], m + '.nii.gz'))
        if options['debug']:
            print "    -->  Empty mask as", m, "image"
            masks.remove(masks[index])

def register_masks(options):
    """
    - to doc
    - moving all images to the T1 space

    """

    scan = options['tmp_scan']
    # rigid registration
    os_host = platform.system()
    if os_host == 'Linux':
        reg_exe = 'reg_aladin'
    else:
        print "> ERROR: The OS system", os_host, "is not currently supported."

    reg_aladin_path = os.path.join(options['niftyreg_path'], reg_exe)

    for mod in options['modalities']:
        if mod == 'T1':
            continue

        try:
            print "> PRE:", scan, "registering",  mod, " --> T1 space"
            subprocess.check_output([reg_aladin_path, '-ref',
                                     os.path.join(options['tmp_folder'], 'T1.nii.gz'),
                                     '-flo', os.path.join(options['tmp_folder'], mod + '.nii.gz'),
                                     '-aff', os.path.join(options['tmp_folder'], mod + '_transf.txt'),
                                     '-res', os.path.join(options['tmp_folder'], 'r' + mod + '.nii.gz')])
        except:
            print "> ERROR:", scan, "registering masks on  ", mod, "quiting program."
            time.sleep(1)
            os.kill(os.getpid(), signal.SIGTERM)

    # if training, the lesion mask is also registered through the T1 space.
    # Assuming that the refefence lesion space was FLAIR.
    if options['task'] == 'training':
        # rigid registration
        os_host = platform.system()
        if os_host == 'Windows':
            reg_exe = 'reg_resample.exe'
        elif os_host == 'Linux':
            reg_exe = 'reg_resample'
        else:
            print "> ERROR: The OS system", os_host, "is not currently supported."

        reg_resample_path = os.path.join(options['niftyreg_path'], reg_exe)

        try:
            print "> PRE:", scan, "resampling the lesion mask --> T1 space"
            subprocess.check_output([reg_resample_path, '-ref',
                                     os.path.join(options['tmp_folder'], 'T1.nii.gz'),
                                     '-flo', os.path.join(options['tmp_folder'], 'lesion'),
                                     '-trans', os.path.join(options['tmp_folder'], 'FLAIR_transf.txt'),
                                     '-res', os.path.join(options['tmp_folder'], 'lesion.nii.gz'),
                                     '-inter', '0'])
        except:
            print "> ERROR:", scan, "registering masks on  ", mod, "quiting program."
            time.sleep(1)
            os.kill(os.getpid(), signal.SIGTERM)


def register_MNI(options):
    """
    Registering to MNI_template
    """

    command01='reg_aladin -ref '+options['MNI_Template']+' -flo '+options['tmp_folder']+'/T1.nii.gz -aff '+options['tmp_folder']+'/MNI_trafo_Affine.txt -res '+options['tmp_folder']+'/rT1.nii.gz'
    print command01+'\n'
    if os.system(command01):
        raise RuntimeError('program {} failed!'.format(command01))

    print 'FIM 01 - Corregistro afim T1 para Template e geracao da matriz transformacao\n'


    command02='reg_resample -ref '+options['MNI_Template']+' -flo '+options['tmp_folder']+'/rFLAIR.nii.gz -res '+options['tmp_folder']+'/rrFLAIR.nii.gz -aff '+options['tmp_folder']+'/MNI_trafo_Affine.txt'
    print command02+'\n'
    if os.system(command02):
        raise RuntimeError('program {} failed!'.format(command02))

    print 'FIM 02 - Aplicacao da matriz transformacao na imagem flair\n'


    command03='reg_resample -ref '+options['MNI_Template']+' -flo '+options['tmp_folder']+'/rT2.nii.gz -res '+options['tmp_folder']+'/rrT2.nii.gz -aff '+options['tmp_folder']+'/MNI_trafo_Affine.txt'
    print command03+'\n'
    if os.system(command03):
        raise RuntimeError('program {} failed!'.format(command03))
    print 'FIM 03 - Aplicacao da matriz transformacao na imagem T2\n'

    command04='reg_resample -ref '+options['MNI_Template']+' -flo '+options['tmp_folder']+'/lesion.nii.gz -res '+options['tmp_folder']+'/rrlesion.nii.gz -aff '+options['tmp_folder']+'/MNI_trafo_Affine.txt'
    print command04+'\n'
    if os.system(command04):
        raise RuntimeError('program {} failed!'.format(command04))

    print 'FIM 04 - Aplicacao da matriz transformacao na mascara\n'

def denoise_masks(options):
    """
    Denoise input masks to reduce noise.
    Using anisotropic Diffusion (Perona and Malik)

    """

    for mod in options['modalities']:

        current_image ='r'+ mod + '.nii.gz' if mod == 'T1' else 'rr' + mod + '.nii.gz'

        tmp_scan = nib.load(os.path.join(options['tmp_folder'],current_image))

        tmp_scan.get_data()[:] = ans_dif(tmp_scan.get_data(),niter=options['denoise_iter'])

        tmp_scan.to_filename(os.path.join(options['tmp_folder'],'d' + current_image))
        if options['debug']:
            print "> DEBUG: Denoising ", current_image


def skull_strip(options):
    """
    External skull stripping using ROBEX: Run Robex and save skull
    stripped masks
    input:
       - options: contains the path to input images
    output:
    - None
    """

    scan = options['tmp_scan']
    t1_im = os.path.join(options['tmp_folder'], 'drT1.nii.gz')
    t1_st_im = os.path.join(options['tmp_folder'], 'T1_brain.nii.gz')

    try:
        print "> PRE:", scan, "skull_stripping the T1 modality"
        subprocess.check_output([options['robex_path'],
                                 t1_im,
                                 t1_st_im])
    except:
        print "> ERROR:", scan, "registering masks, quiting program."
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)

    brainmask = nib.load(t1_st_im).get_data() > 1
    for mod in options['modalities']:

        if mod == 'T1':
            continue

        # apply the same mask to the rest of modalities to reduce
        # computational time

        print '> PRE: ', scan, 'Applying skull mask to ', mod, 'image'
        current_mask = os.path.join(options['tmp_folder'],
                                    'drr' + mod + '.nii.gz')
        current_st_mask = os.path.join(options['tmp_folder'],
                                       mod + '_brain.nii.gz')

        mask = nib.load(current_mask)
        mask_nii = mask.get_data()
        mask_nii[brainmask == 0] = 0
        mask.get_data()[:] = mask_nii
        mask.to_filename(current_st_mask)


def preprocess_scan(current_folder, options):
    """
    Preprocess scan taking into account user options
    - input:
      current_folder = path to the current image
      options: options

    """
    preprocess_time = time.time()

    scan = options['tmp_scan']
    try:
        # os.rmdir(os.path.join(current_folder,  'tmp'))
        os.mkdir(options['tmp_folder'])     
    except:
        if os.path.exists(options['tmp_folder']) is False:
            print "> ERROR:",  scan, "I can not create tmp folder for", current_folder, "Quiting program."

        else:
            pass

    # --------------------------------------------------
    # find modalities and move everything to a tmp folder
    # --------------------------------------------------
    id_time = time.time()
    parse_input_masks(current_folder, options)
    print "> INFO:", scan, "elapsed time: ", round(time.time() - id_time), "sec"

    # --------------------------------------------------
    # register modalities
    # --------------------------------------------------
    if options['register_modalities'] is True:
        reg_time = time.time()
        #register_masks(options)
        print "> INFO:", scan, "elapsed time: ", round(time.time() - reg_time), "sec"
    else:
        try:
            for mod in options['modalities']:
                if mod == 'T1':
                    continue
                out_scan = mod + '.nii.gz' if mod == 'T1' else 'r' + mod + '.nii.gz'
                shutil.copy2(os.path.join(options['tmp_folder'],
                                         mod + '.nii.gz'),
                             os.path.join(options['tmp_folder'],
                                         out_scan))
        except:
            print "> ERROR: registration ", scan, "I can not rename input modalities as tmp files. Quiting program."

            time.sleep(1)
            os.kill(os.getpid(), signal.SIGTERM)

    # --------------------------------------------------
    # register template
    # --------------------------------------------------
    register_MNI(options)
    # --------------------------------------------------
    # noise filtering
    # --------------------------------------------------
    if options['denoise'] is True:
        denoise_time = time.time()
        denoise_masks(options)
        print "> INFO: denoising", scan, "elapsed time: ", round(time.time() - denoise_time), "sec"
    else:
        try:
            for mod in options['modalities']:
                input_scan = mod + '.nii.gz' if mod == 'T1' else 'r' + mod + '.nii.gz'
                shutil.copy(os.path.join(options['tmp_folder'],
                                         input_scan),
                            os.path.join(options['tmp_folder'],
                                         'd' + input_scan))
        except:
            print "> ERROR denoising:", scan, "I can not rename input modalities as tmp files. Quiting program."
            time.sleep(1)
            os.kill(os.getpid(), signal.SIGTERM)

    # --------------------------------------------------
    # skull strip
    # --------------------------------------------------

    if options['skull_stripping'] is True:
        sk_time = time.time()
        skull_strip(options)
        print "> INFO:", scan, "elapsed time: ", round(time.time() - sk_time), "sec"
    else:
        try:
            for mod in options['modalities']:
                input_scan = 'd' + mod + '.nii.gz' if mod == 'T1' else 'dr' + mod + '.nii.gz'
                shutil.copy(os.path.join(options['tmp_folder'],
                                         input_scan),
                            os.path.join(options['tmp_folder'],
                                         mod + '_brain.nii.gz'))
        except:
            print "> ERROR: Skull-stripping", scan, "I can not rename input modalities as tmp files. Quiting program."
            time.sleep(1)
            os.kill(os.getpid(), signal.SIGTERM)

    if options['skull_stripping'] is True and options['register_modalities'] is True:
        print "> INFO:", scan, "total preprocessing time: ", round(time.time() - preprocess_time)

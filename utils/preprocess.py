import os
import shutil
import sys
import signal
import subprocess
import time
import platform
import nibabel as nib
import numpy as np
import SimpleITK as sitk
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
        if mod == options['modalities'][1]:
            continue
        
        try:
            if mod == options['modalities'][0]:
                text="FLAIR"
            else:
                text="T2"

            maxi='5'
            print "> PRE:", scan, "registering",  mod, " --> T1 space"
            subprocess.check_output([reg_aladin_path, '-ref',
                                    options['T1'],
                                     '-rigOnly',
                                     '-noSym', 
                                     '-flo', options['original'] + mod,
                                     '-aff', options['tmp_folder'] + text + '_transf.txt',
                                     '-res', options['tmp_folder'] + 'r' + mod])
        except:
            print "> ERROR:", scan, "registering masks on ", mod, "quiting program."
            time.sleep(1)
            os.kill(os.getpid(), signal.SIGTERM)
        
    # if training, the lesion mask is also registered through the T1 space.
    # Assuming that the refefence lesion space was FLAIR.
    # rigid registration
    os_host = platform.system()
    if os_host == 'Linux':
        reg_exe = 'reg_resample'
    else:
        print "> ERROR: The OS system", os_host, "is not currently supported."

    reg_resample_path = os.path.join(options['niftyreg_path'], reg_exe)
    if options['MASK']:
        
        try:
            print "> PRE:", scan, "resampling the lesion mask --> T1 space"
            subprocess.check_output([reg_resample_path, '-ref',
                                     options['T1'],
                                     '-flo', options['mask'],
                                     '-trans', options['tmp_folder'] + 'FLAIR_transf.txt',
                                     '-res', options['pre_mask'] + 'lesion.nii.gz',
                                     '-inter', '0'])
        except:
            print "> ERROR:", scan, "registering masks on ", mod, "quiting program."
            time.sleep(1)
            os.kill(os.getpid(), signal.SIGTERM)


def register_MNI(options):
    """
    Registering to MNI_template
    """
    command01='reg_aladin -ref '+options['MNI_Template']+' -flo '+options['T1'] +' -aff '+options['tmp_folder']+'MNI_trafo_Affine.txt -res '+options['tmp_folder']+'r' + options['modalities'][1]
    print command01+'\n'
    if os.system(command01):
        raise RuntimeError('program {} failed!'.format(command01))

    print 'FIM 01 - Corregistro afim T1 para Template e geracao da matriz transformacao\n'


    command02='reg_resample -ref '+options['MNI_Template']+' -flo '+options['tmp_folder']+'r'+ options['modalities'][0] +' -res '+options['tmp_folder']+'rr' +options['modalities'][0] +' -aff '+options['tmp_folder']+'MNI_trafo_Affine.txt'
    print command02+'\n'
    if os.system(command02):
        raise RuntimeError('program {} failed!'.format(command02))

    print 'FIM 02 - Aplicacao da matriz transformacao na imagem flair\n'


    command03='reg_resample -ref '+options['MNI_Template']+' -flo '+options['tmp_folder']+'r'+ options['modalities'][2] +' -res '+options['tmp_folder']+'rr' +options['modalities'][2] +' -aff '+options['tmp_folder']+'MNI_trafo_Affine.txt'
    print command03+'\n'
    if os.system(command03):
        raise RuntimeError('program {} failed!'.format(command03))

    print 'FIM 02 - Aplicacao da matriz transformacao na imagem flair\n'

    if options['MASK']:
        command04='reg_resample -ref '+options['MNI_Template']+' -flo '+options['pre_mask']+'lesion.nii.gz -res '+options['pre_mask']+'rrlesion.nii.gz -aff '+options['tmp_folder']+'MNI_trafo_Affine.txt'
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

        current_image ='r'+ mod if mod == options['modalities'][1] else 'rr' + mod

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
    t1_im = options['tmp_folder'] +'dr'+ options['modalities'][1]
    t1_st_im = options['tmp_folder'] + options['modalities'][1] + '_brain.nii.gz'

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

        if mod == options['modalities'][1]:
            current_mask = options['tmp_folder'] + 'dr' + mod
        else:
           current_mask = options['tmp_folder'] + 'drr' + mod
            # apply the same mask to the rest of modalities to reduce
            # computational time

        print '> PRE: ', scan, 'Applying skull mask to ', mod, 'image'
        current_st_mask = options['tmp_folder']+'brain'+ mod

        mask = nib.load(current_mask)
        mask_nii = mask.get_data()
        mask_nii[brainmask == 0] = 0
        mask.get_data()[:] = mask_nii
        mask.to_filename(current_st_mask)



def N4(options):
    for mod in options['modalities']:
        print("N4 bias correction runs on" + mod)
        A = (options['tmp_folder']+ 'brain' + mod)
        A = A.encode("utf-8")
       
        inputImage = sitk.ReadImage(A)
        inputImage = sitk.Cast(inputImage,sitk.sitkFloat32)
        corrector = sitk.N4BiasFieldCorrectionImageFilter();



        output = corrector.Execute(inputImage)
        nome = options['tmp_folder']+'N4_brain' + mod
        nome = nome.encode("utf-8")
        sitk.WriteImage(output, nome)
        print("Finished N4 Bias Field Correction.....")


def preprocess_scan(current_folder, options):
    """
    Preprocess scan taking into account user options
    - input:
      current_folder = path to the current image
      options: options

    """
    preprocess_time = time.time()

    scan = options['tmp_scan']
   
    # --------------------------------------------------
    # find modalities and move everything to a tmp folder
    # --------------------------------------------------
    id_time = time.time()
    print "> INFO:", scan, "elapsed time: ", round(time.time() - id_time), "sec"
 
    # --------------------------------------------------
    # register modalities
    # --------------------------------------------------
    if options['register_modalities'] is True:
        reg_time = time.time()
        register_masks(options)
        print "> INFO:", scan, "elapsed time: ", round(time.time() - reg_time), "sec"
    else:
        try:
            for mod in options['modalities']:
                if mod == 'T1':
                    continue
                out_scan = mod  if mod == 'T1' else 'r' + mod 
                shutil.copy2(os.path.join(options['tmp_folder'],
                                         mod),
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
        # try:
        #     for mod in options['modalities']:
        #         input_scan = mod + '.nii.gz' if mod == 'T1' else 'r' + mod + '.nii.gz'
        #         shutil.copy(os.path.join(options['tmp_folder'],
        #                                  input_scan),
        #                     os.path.join(options['tmp_folder'],
        #                                  'd' + input_scan))
        # except:
            print "> ERROR denoising:", scan, "I can not rename input modalities as tmp files. Quiting program."
            time.sleep(1)
            os.kill(os.getpid(), signal.SIGTERM)


    #--------------------------------------------------
    #skull strip
    #--------------------------------------------------
   

    if options['skull_stripping'] is True:
        sk_time = time.time()
        skull_strip(options)
        print "> INFO:", scan, "elapsed time: ", round(time.time() - sk_time), "sec"
    else:
        try:
            for mod in options['modalities']:
                input_scan = 'd' + mod  if mod == options['modalities'][1] else 'dr' + mod 
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



    #--------------------------------------------------
    #N4 intensity inhomogeneity correction (Bias Field)
    #--------------------------------------------------
    N4(options)
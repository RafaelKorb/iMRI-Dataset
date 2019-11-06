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
                                     '-flo', options['original'] + mod,
                                     '-aff', options['tmp_folder'] + text + '_transf.txt',
                                     '-res', options['tmp_folder'] + 'r' + mod])
        except:
            print "> ERROR:", scan, "registering masks on ", mod, "quiting program."
            time.sleep(1)
            os.kill(os.getpid(), signal.SIGTERM)
        
  
    #lesion mask is also registered through the T1 space.
    #Assuming that the reference lesion space was FLAIR.
    
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
    Anisotropic Diffusion (Perona and Malik)
    """
    for mod in options['modalities']:

        current_image ='r'+ mod if mod == options['modalities'][1] else 'rr' + mod

        tmp_scan = nib.load(os.path.join(options['tmp_folder'],current_image))

        tmp_scan.get_data()[:] = ans_dif(tmp_scan.get_data(),niter=options['denoise_iter'])

        tmp_scan.to_filename(os.path.join(options['tmp_folder'],'d' + current_image))
   

def skull_strip(options):
    """
    External skull stripping using ROBEX: Run Robex and save skull
    stripped masks
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
        print("N4 bias correction runing on"+'\n'+mod)
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
    Function to call preprocess methods.

    """
    preprocess_time = time.time()

    scan = options['tmp_scan']
   
    # --------------------------------------------------
    # register modalities
    # --------------------------------------------------
    try:
        reg_time = time.time()
        register_masks(options)
        print "> INFO:", scan, "elapsed time: ", round(time.time() - reg_time), "sec"
    
    except:
        print "> ERROR: registration ", scan, "I can not rename input modalities as tmp files. Quiting program."
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)
 
    

    # --------------------------------------------------
    # register template
    # --------------------------------------------------
    try:
        MNI_time = time.time()
        register_MNI(options)
        print "> INFO: Register MNI", scan, "elapsed time: ", round(time.time() - MNI_time), "sec"

    except:
        print "> ERROR Register MNI:", scan, "I can not rename input modalities as tmp files. Quiting program."
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)

    
    # --------------------------------------------------
    # noise filtering
    # --------------------------------------------------
    try:
        denoise_time = time.time()
        denoise_masks(options)
        print "> INFO: denoising", scan, "elapsed time: ", round(time.time() - denoise_time), "sec"
    
    except:
        print "> ERROR denoising:", scan, "I can not rename input modalities as tmp files. Quiting program."
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)

    
    #--------------------------------------------------
    #skull strip
    #--------------------------------------------------
    try:
        sk_time = time.time()
        skull_strip(options)
        print "> INFO:", scan, "elapsed time: ", round(time.time() - sk_time), "sec"
    
    except:
        print "> ERROR: Skull-stripping", scan, "I can not rename input modalities as tmp files. Quiting program."
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)
    

    #--------------------------------------------------
    #N4 intensity inhomogeneity correction (Bias Field)
    #--------------------------------------------------
    try:
        N4_time = time.time()
        N4(options)
        print "> INFO:", scan, "elapsed time: ", round(time.time() - N4_time), "sec"
    except:
        print "> ERROR: N4", scan, "I can not rename input modalities as tmp files. Quiting program."
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)

    print "> INFO:", scan, "total preprocessing time: ", round(time.time() - preprocess_time)
    
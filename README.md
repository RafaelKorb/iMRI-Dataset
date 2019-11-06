# projeto_tcc

Algoritm based on NicMsLesions, specific to pre-process images.
Adapted to json, work whit unlimited number of datasets.

The offer json take in count 5 public data images:

SCLEROSIS:

*ISBI  
*LYUBLYANA  
*MICCAI08  
*MICCAI16

HEALTHY  
*KIRBY


Requirements
----------------------------------------------------------------
h5py  
MedPy==0.3.0  
scipy==1.0.0  
Keras==2.0.0  
nibabel==2.1.0  
numpy==1.13.3  
Pillow==5.0.0  
 
Type of images (MRI):  
FLAIR  
T1  
T2


Directory
-----------------------------------------------------------------

Build the structure folders to in/out images

DATABASE --> where you unzip the original datasets  
PRE --> where the pre-process images will be stored.


Change_extensions
-----------------------------------------------------------------

Trasform the images into "nii.gz"


Utils/preprocess
-----------------------------------------------------------------
arquive whit the preprocess functions

Protocol:  
Images rigid registered on T1 space  
Registered on MNI template  
Anysotropic filter  
Skull-stripping  
Bias field (Intensity inhomogeneity (IIH) or intensity non-uniformity)


Manipulating_data
----------------------------------------------------------------------
filter information from json to work whit the pre-process images

test and train



Main_script (main script)
-----------------------------------------------------------------

Runs the pre-process on all images of json.

Input require local machine directory, like:

python rafa_script.py home/user/main_directory/




Working
-----------------------------------------------------------------
1- Execute build_diretory.py

2- Download images and unzip inside their respective folders

3- Execute change_extensions.py

4- Execute create_json.py

5-Execute Main_script.py








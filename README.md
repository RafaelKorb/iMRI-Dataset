# projeto_tcc

Algoritm based on NicMsLesions, specific to preprocessing images.
Adapted to json, work whit unlimited number of datasets.




Datasets Images
-----------------------------

The offer json take in count 5 public data images:

-----------------------------------------
SCLEROSIS: 113 images

--------------------------------------------------------------------------------------------------------
*ISBI 2015 (Longitudinal multiple sclerosis lesion segmentation challenge)

Training: 5 patients

Test: 14 patients

---------------------------------------------------------------
*ljubljana (Laboratory of Imaging Technologies)

Whitout original separation (put on training): 30 patients

Features:

"age" 

"sex"   (7 Male -- 23 Female)

"ms_type" (24-RR / 2-CIS / 1-PR  / 2-SP / 1-N/A)

---------------------------------------------------------------
*MICCAI 2008 (International Conference on Medical Imaging and Computer Assisted Intervention - MS Lesion Segmentation Challenge)

Training: 20 patients

Test: 29 patients


---------------------------------------------------------------
*MICCAI 2016 (International Conference on Medical Imaging and Computer Assisted Intervention - MS Lesion Segmentation Challenge)

Only training: 15 patients

Features:

"age" 

"sex" (7 Male -- 8 Female)

-----------------------------------------
HEALTHY: 45

-----------------------------------------
*KIRBY (Multi-Modal MRI Reproducibility Resource)

Puting on training: 45 patients

Features:

"age"

"sex" (22 Male -- 23 Female)


---------------------------------------------------------------
*OASIS-3 (Open Access Series of Imaging Studies)


Instructions to Download
---------------------------------------------------------------------------------------------
*ISBI 2015

Link to download: https://smart-stats-tools.org/lesion-challenge

Make account on site and go to "lession challange" - sclerosis - data


------------------------------------------------------------------------------------------------------------------------------
*LJUBLJANA
Link to download: http://lit.fe.uni-lj.si/tools.php?lang=eng


Take all links from "3D MR image database of Multiple Sclerosis patients with white matter lesion segmentations"


------------------------------------------------------------------------------------------------------------------------------
*MICCAI08  
Link to download: https://www.nitrc.org/frs/?group_id=745


Download all url's from "Segmentation Challenge Data"

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*MICCAI16

Register on site here: https://portal.fli-iam.irisa.fr/msseg-challenge/overview?p_p_id=registration_WAR_fliiamportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=1&p_p_col_count=3&_registration_WAR_fliiamportlet_mvcPath=%2Fhtml%2Fregistration%2Fregistration.jsp


Link to download: https://portal.fli-iam.irisa.fr/msseg-challenge/data

---------------------------------------------------------------------------------------------

*KIRBY
Link to download: https://www.nitrc.org/frs/?group_id=313


Select all links from "Kirby 21 (2009)"

---------------------------------------------------------------------------------------------
*OASIS
Rigister on site here: https://central.xnat.org/app/template/Register.vm#!


Link to download: https://central.xnat.org/app/template/XDATScreen_report_xnat_projectData.vm/search_element/xnat:projectData/search_field/xnat:projectData.ID/search_value/OASIS3

Acess "donwload images" in box "actions"

On "2: select image data" select the boxes NIFTI, FLAIR, T1w and T2w 

On "3: download data" select "option 2: ZIP download" then submit



Requirements
----------------------------------------------------------------
h5py  
MedPy==0.3.0  
scipy==1.0.0  
Keras==2.0.0  
nibabel==2.1.0  
numpy==1.13.3  
Pillow==5.0.0  
 


Preprocessing protocol
-----------------------------------------------------------------

Locate on: Utils/preprocess.py (arquive whit the preprocess functions)

Protocol:  
Images rigid registered on T1 space  
Registered on MNI template  
Anysotropic filter  
Skull-stripping  
Bias field (Intensity inhomogeneity (IIH) or intensity non-uniformity)



Dataset images preparation
-----------------------------------------------------------------
Step 1:

Execute --> Directory.py

Build the structure folders to in/out images

DATABASE --> where you unzip the original datasets  
PRE --> where the pre-process images will be stored.

--------------------------------------------
Step 2:

Download images and unzip inside their respective folders


--------------------------------------------
Step 3:

Execute --> Change_extensions.py

Will trasform the images into "nii.gz"

--------------------------------------------
step 4:

Execute --> create json.py

Will create dictionary from data and location paths images


Running the preprocessing into images
-----------------------------------------------------------------
Execute --> main.py

Has to pass the main folder project as a parameter

Ex: python main.py home/user/main_directory/


Json manipulating data
----------------------------------------------------------------------
Execute --> Manipulating_data.py

Filter information from json to work whit the preprocessing images

Build "our_json", whit the division test/training (75%-25%)

*"our_json" is build whitout using test of original data-sets in our train.

The divison in test/train considerate 50-50 healthy and MS patients


Summarizing the execution sequences
-----------------------------------------------------------------
1- Execute build_diretory.py

2- Download images and unzip inside their respective folders

3- Execute change_extensions.py

4- Execute create_json.py

5-Execute main.py

6-Execute manipulanting_data.py 






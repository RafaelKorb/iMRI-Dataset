# projeto_tcc

Introduction
-------------------------------------------

This repository contains scripts to preprocessing MRI images of healthy and multiple sclerosis patients, based on NicMsLesions tool.
Adapted to work with json, support unlimited number of datasets.
The aim of this work is to provide a preprocessed magnetic resonance imaging base for the application of multiple sclerosis lesion classification and segmentation algorithms.


Datasets Images
-----------------------------

The preprocessing work just with the modalities T1, T2 and FLAIR, and they three has to be present.

The json dictionary offers 5 public datasets images:

-----------------------------------------
SCLEROSIS: 109 images

--------------------------------------------------------------------------------------------------------
*ISBI 2015 (Longitudinal multiple sclerosis lesion segmentation challenge)

21 images

Training: 5 patients

Test: 14 patients

---------------------------------------------------------------
*ljubljana (Laboratory of Imaging Technologies)


30 images

Only training: 30 patients


Demographics Features:

---------------------------------------------------------------
"age" 

---------------------------------------------------------------
"sex"   (7 Male("M") -- 23 Female("F"))

---------------------------------------------------------------
"ms_type" (disgnostic of desease by specialists)

Relapsing remitting("RR") - 24 cases

Clinically isolated syndrome("CIS") - 2 cases

Primary progressive("PR") - 1 case

Secondary progressive("SP") - 2 cases

Whitout diagnostic - 1 case



---------------------------------------------------------------
*MICCAI 2008 (International Conference on Medical Imaging and Computer Assisted Intervention - MS Lesion Segmentation Challenge)

51 images

Training: 20 patients

Test: 25 patients

Has no annotated features

---------------------------------------------------------------
*MICCAI 2016 (International Conference on Medical Imaging and Computer Assisted Intervention - MS Lesion Segmentation Challenge)


15 images

Only training: 15 patients

Features:

"age" 

-----------------------------------------
"sex" (7 Male -- 8 Female)

-----------------------------------------
HEALTHY: 21

-----------------------------------------
*KIRBY (Multi-Modal MRI Reproducibility Resource)


42 images

Puting on training: 21 patients

Features:

"age"

-----------------------------------------
"sex" (10 Male -- 11 Female)


---------------------------------------------------------------
*OASIS-3 (Open Access Series of Imaging Studies)

In soon

Instructions to Download
---------------------------------------------------------------------------------------------



*ISBI 2015

Link to download [here](https://smart-stats-tools.org/lesion-challenge)

Make account on site and go to "lesion challenge" - sclerosis - data


------------------------------------------------------------------------------------------------------------------------------
*LJUBLJANA
Link to download [here](http://lit.fe.uni-lj.si/tools.php?lang=eng)


Get all links from "3D MR image database of Multiple Sclerosis patients with white matter lesion segmentations"


------------------------------------------------------------------------------------------------------------------------------
*MICCAI08  

Link to download [here](https://www.nitrc.org/frs/?group_id=745)


Download all urls from "Segmentation Challenge Data"

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*MICCAI16

Register on site [here](https://portal.fli-iam.irisa.fr/msseg-challenge/overview?p_p_id=registration_WAR_fliiamportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=1&p_p_col_count=3&_registration_WAR_fliiamportlet_mvcPath=%2Fhtml%2Fregistration%2Fregistration.jsp)


Link to download [here](https://portal.fli-iam.irisa.fr/msseg-challenge/data)

---------------------------------------------------------------------------------------------

*KIRBY
Link to download [here](https://www.nitrc.org/frs/?group_id=313)


Select all links from "Kirby 21 (2009)".

---------------------------------------------------------------------------------------------
*OASIS
Rigister on site [here](https://central.xnat.org/app/template/Register.vm#!)


Link to download [here](https://central.xnat.org/app/template/XDATScreen_report_xnat_projectData.vm/search_element/xnat:projectData/search_field/xnat:projectData.ID/search_value/OASIS3)

Acess "donwload images" in box "actions.

On "2: select image data" select the boxes NIFTI, FLAIR, T1w and T2w. 

On "3: download data" select "option 2: ZIP download" then submit.



Requirements
----------------------------------------------------------------
h5py==2.10.0

MedPy==0.3.0

scipy==1.0.0

Keras==2.0.0

nibabel==2.1.0

numpy==1.13.3

Pillow==5.0.0

ConfigParser==4.0.2

SimpleITK==1.2.4

wget==1.20.3
 


Preprocessing protocol
-----------------------------------------------------------------

Located on: Utils/preprocess.py (arquive whit the preprocess functions)

Protocol:  
Images rigid registered on T1 space  
Registered on MNI template  
Anysotropic filter  
Skull-stripping  
Bias field (Intensity inhomogeneity (IIH) or intensity non-uniformity)



Preparation of the dataset images
-----------------------------------------------------------------
Step 1:

Execute --> build_directory.py

Build the structure folders to in/out images.

DATABASE --> where you unzip the original datasets.
PRE --> where the pre-process images will be stored.

--------------------------------------------
Step 2:

Download images and unzip inside their respective folders.


--------------------------------------------
Step 3:

Execute --> change_extensions.py

Will trasform the images into "nii.gz".

--------------------------------------------
step 4:

Execute --> create_json.py

Will create a dictionary from the data, including the path of images.


Running the preprocessing into images
-----------------------------------------------------------------
Execute --> main.py

Has to pass the main folder project as a parameter

Ex: python main.py home/user/main_directory/


Manipulating json data
----------------------------------------------------------------------
Execute --> Manipulating_data.py

Manipuling information from json to work whit the preprocessing images.

Build "our_json", whit the division test/training (75%-25%).

*"our_json" is build whitout using train of original data-sets in our test.

The divison in test/train considerate 50-50 healthy and MS patients.


Summarizing the execution sequences
-----------------------------------------------------------------
1- Execute build_diretory.py

2- Download images and unzip inside their respective folders

3- Execute change_extensions.py

4- Execute create_json.py

5-Execute main.py

6-Execute manipulanting_data.py 






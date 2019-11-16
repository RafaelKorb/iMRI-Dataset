# projeto_tcc

Algoritm based on NicMsLesions, specific to pre-process images.
Adapted to json, work whit unlimited number of datasets.




DATASETs Images
-----------------------------

The offer json take in count 5 public data images:

SCLEROSIS:

*ISBI 
link to download: https://smart-stats-tools.org/lesion-challenge

make account on site and go to "lession challange" - sclerosis - data


*LYUBLYANA  
link to download: http://lit.fe.uni-lj.si/tools.php?lang=eng


*MICCAI08  
link to download: https://www.nitrc.org/frs/?group_id=745
download all url's from "Segmentation Challenge Data"

*MICCAI16
Register on site here: https://portal.fli-iam.irisa.fr/msseg-challenge/overview?p_p_id=registration_WAR_fliiamportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=1&p_p_col_count=3&_registration_WAR_fliiamportlet_mvcPath=%2Fhtml%2Fregistration%2Fregistration.jsp
link to download: https://portal.fli-iam.irisa.fr/msseg-challenge/data

HEALTHY  

*KIRBY
link to download: https://www.nitrc.org/frs/?group_id=313
Select all links from "Kirby 21 (2009)"

*OASIS
Rigister on site here: https://central.xnat.org/app/template/Register.vm#!
link to download: https://central.xnat.org/app/template/XDATScreen_report_xnat_projectData.vm/search_element/xnat:projectData/search_field/xnat:projectData.ID/search_value/OASIS3

acess "donwload images" in box "actions"

select de boxes like in image:

![alt text] (https://bitbucket.org/RafaelKorb/projeto_tcc/src/working_version/oasis_download.png)


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


JSON
-----------------------------------------------------------------
Create Json build Data.json, where is use to pre-processing images

Manipulating_data build our_json, whit the division test/training (75-25)

our_json is build whitout using test of original data-sets in our train.

The divison in test/train considerate 50-50 healthy and MS patients

Working
-----------------------------------------------------------------
1- Execute build_diretory.py

2- Download images and unzip inside their respective folders

3- Execute change_extensions.py

4- Execute create_json.py

5-Execute Main_script.py

6-Execute manipulanting_data.py 






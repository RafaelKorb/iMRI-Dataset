#!/usr/bin/python

import os
import sys
import csv
import subprocess
import threading
import thread
import multiprocessing
import SimpleITK as sitk
from subprocess import Popen

path=os.path.abspath(__file__);
path2= os.path.dirname(path);

image_folder=path2

# image_folder= sys.argv[1]
# mask_folder= sys.argv[2]


for dirname, dirnames, filenames in os.walk(image_folder):
    for filename in filenames:
        file=os.path.join(dirname, filename)
        
        #nhdr to nii.gz
        if ".nhdr" in file:
            img = sitk.ReadImage(file)
            sitk.WriteImage(img, file[:-5]+".nii.gz", True)
            os.remove(file)
            os.remove(file[:-5]+".raw")
   


        #nii to nii.gz
        if ".nii" in file:
            if ".nii.gz" in file:
                continue
            else:
                img = sitk.ReadImage(file)
                sitk.WriteImage(img, file + ".gz", True)
                print(file)
                os.remove(file)




    # Advanced usage:
    # editing the 'dirnames' list will stop os.walk() from recursing into there.
    # if '.git' in dirnames:
    #     # don't go into any .git directories.
    #     dirnames.remove('.git')


# i=0
# for image_folder, subdirs, filenames in os.walk(image_folder):
#     sub=os.listdir(image_folder+"/")
#     for each in sub:
#         if ".nhdr" in each:
#             file = os.path.abspath(each)
#             print file
#             img = sitk.ReadImage(file)
#             #sitk.WriteImage(file[:-5]+".nii.gz")
#             print file[:-5]+".nii.gz"


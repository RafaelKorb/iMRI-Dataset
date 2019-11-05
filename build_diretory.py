import wget
import os , sys
import json


#buildin folder to pre-process images
with open('data.json', 'r') as f:
    data = json.load(f)
    path=('pre')
     
    if os.path.isdir(path):
            print("directory already exists, delete folder pre to build new one") 

    else:        
        for i, data_dict in enumerate(data):
            data_dict["path_T1_pre"] = data_dict['path_T1_pre'].split("/")[:-1]
            data_dict['path_T1_pre'] = '/'.join([str(elem) for elem in data_dict['path_T1_pre']])
             
            os.makedirs(data_dict["path_T1_pre"])   


#links to Download images, liubliana can be automatic downloaded if up lines 25,26,27,28,29 and 53,54,55

liubliana = [
# 'http://lit.fe.uni-lj.si/contents/tools/3D-MS-DB/DB/patient01-05.zip',
# 'http://lit.fe.uni-lj.si/contents/tools/3D-MS-DB/DB/patient06-10.zip',
# 'http://lit.fe.uni-lj.si/contents/tools/3D-MS-DB/DB/patient11-15.zip',
# 'http://lit.fe.uni-lj.si/contents/tools/3D-MS-DB/DB/patient16-20.zip',
# 'http://lit.fe.uni-lj.si/contents/tools/3D-MS-DB/DB/patient26-30.zip',
]

# ISBI = [
# ]

# MICCAI08 = [
# ]

# MICCAI16 = [
# ]


with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

    path = ["DATABASE/Sclerosi/liubliana", 'DATABASE/Sclerosi/ISBI', 'DATABASE/Sclerosi/MICCAI08', 'DATABASE/Sclerosi/MICCAI16'] 

    exists = os.path.exists("DATABASE")
    if exists == True:
            print("directory already exists, delete folder DATABASE to build new one")
    else:
        for directory in path:
            os.makedirs(directory)
            
            # if directory == 'DATABASE/Esclerose/liubliana':
            #     for links in liubliana:
              #       filename = wget.download(links, directory)
        # if directory == 'DATABASE/Esclerose/ISBI':
      #       for links in ISBI:
        #         filename = wget.download(links, directory)
        #  if directory == 'DATABASE/Esclerose/MICCAI08':
        #      for links in MICCAI08:
         #         filename = wget.download(links, directory)
        # if directory == 'DATABASE/Esclerose/MICCAI16':
        #     for links in MICCAI16:
        #         filename = wget.download(links, directory)




          

import wget
import os , sys

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



path = ["DATABASE/Esclerose/liubliana", 'DATABASE/Esclerose/ISBI', 'DATABASE/Esclerose/MICCAI08', 'DATABASE/Esclerose/MICCAI16'] 

for directory in path:

     exists = os.path.exists(directory)
     if exists == True:
         print("diretorio de imagens existente, delete caso queria baixar")
     else:
        os.makedirs(directory)
        
        if directory == 'DATABASE/Esclerose/liubliana':
            for links in liubliana:
     	        filename = wget.download(links, directory)
     	# if directory == 'DATABASE/Esclerose/ISBI':
      #       for links in ISBI:
     	#         filename = wget.download(links, directory)
     	#  if directory == 'DATABASE/Esclerose/MICCAI08':
     	#      for links in MICCAI08:
    	 #         filename = wget.download(links, directory)
     	# if directory == 'DATABASE/Esclerose/MICCAI16':
     	#     for links in MICCAI16:
     	#         filename = wget.download(links, directory)

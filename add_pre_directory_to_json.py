import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from pandas import DataFrame
import os , sys

import json


def pre_json():
    with open('data.json', 'r') as f:
        data = json.load(f)
        #buildin json whit folder 'pre'
        for i, data_dict in enumerate(data):
            #data_dict["path_T1_pre"] = data_dict['path_T1'].split("/")[:-1]
            #data_dict['path_T1_pre'] = '/'.join([str(elem) for elem in data_dict['path_T1_pre']]) 
            
            data_dict["path_T1_pre"] = "pre/"+data_dict["path_T1"]
            data_dict["path_FLAIR_pre"] = "pre/"+data_dict["path_FLAIR"]
            data_dict["path_T2_pre"] = "pre/"+data_dict["path_T2"]
            
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile) 

        

        




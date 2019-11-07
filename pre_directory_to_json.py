import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from pandas import DataFrame
import os , sys

import json


def pre_json():
    with open('data.json', 'r') as f:
        data = json.load(f)
        full_data = data[0]

        training = full_data['training']
        test=full_data['test']

        full_data=[]
        full_data.extend(training)
        full_data.extend(test)
        
    	for i, data_dict in enumerate(full_data):
            
            data_dict["path_T1_pre"] = "pre/"+data_dict["path_T1"]
            data_dict["path_FLAIR_pre"] = "pre/"+data_dict["path_FLAIR"]
            data_dict["path_T2_pre"] = "pre/"+data_dict["path_T2"]
            
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile) 

        

        




import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from pandas import DataFrame
import os , sys

import json


def pre_json():
    with open('data.json', 'r') as f:
    	data = json.load(f)
    	training = data[0]
    	test = data[1]
    	test2 = test["test"]
    	training2 = training["training"]
    	
        training2.extend(test2)
        
    	for i, data_dict in enumerate(training2):
            
            data_dict["path_T1_pre"] = "pre/"+data_dict["path_T1"]
            data_dict["path_FLAIR_pre"] = "pre/"+data_dict["path_FLAIR"]
            data_dict["path_T2_pre"] = "pre/"+data_dict["path_T2"]
            
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile) 

        

        




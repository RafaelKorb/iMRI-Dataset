import os
import sys
import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split
import json

with open('data.json', 'r') as f:
    data = json.load(f)
    training = data[0]
    test = data[1]
    test2 = test["test"]
    training2 = training["training"]
    
    full_data=[]
    full_data.extend(training2)
    full_data.extend(test2)
    
    final=[]

    

    #Search in all values 
    # for i, data_dict in enumerate(full_data):
    #     if data_dict['MS'] == 'True':
    #         len=len+1
    #         #print(data_dict['path_T1'])
    #         normals = data_dict['path_T1']


    # print(len)
########################################################

    #Search in training values
    for i, data_dict in enumerate(training2):
        if data_dict['age'] == '36':
            #print(data_dict['path_T1'])
            final.append(data_dict['path_T1'])
            
    #size = len(final)
    #print(size)
########################################################

    # Search in test values
    # for i, data_dict in enumerate(test2):
    #     if data_dict['age'] == '36':
    #         print(data_dict['path_T1'])
    # print(len)



train, test = train_test_split(final, test_size=0.25)

print 'Train:',len(train)
print 'Test:',len(test) 
print "Test size is 25 per cent and Train is 75 per cent, as defined."

#print first row
print(train[0])

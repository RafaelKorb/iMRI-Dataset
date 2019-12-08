import os
import sys
import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split
import json

with open('data.json', 'r') as f:
    data = json.load(f)
    full_data = data[0]

    training = full_data['training']
    test=full_data['test']

    full_data=[]
    full_data.extend(training)
    full_data.extend(test)
    
    #manipulating list's
    healthy=[]
    MS=[]
    restrict_healthy=[]
    restrict_MS=[]

    all_data=[]


    #Search in all values
    for i, data_dict in enumerate(full_data):
        if data_dict['MS'] == 'False':
            healthy.append(data_dict)
        if data_dict['MS'] == 'True':
        	MS.append(data_dict)

    
########################################################


    # Search in training values (to not use original test values on or train)
    for an, only_train in enumerate(training):
        if only_train['MS'] == 'False':
            restrict_healthy.append(only_train)
        if only_train['MS'] == 'True':
        	restrict_MS.append(only_train)



healthy_size=len(healthy)
MS_size=len(MS)


#take the total_size of elements, double of the minimum between MS and healthy
if healthy_size < MS_size:
    total_size=healthy_size*2
else:
	total_size=MS_size*2


#separate test and train sizes (75%-25%)
test_size=(total_size//4)*3
train_size=(total_size)//4

#Make the Train folder
healthy_train_size = train_size//2
ms_train_size = train_size//2
final_train=[]

while healthy_train_size > 0: 
    aa = random.choice(restrict_healthy)
    if aa['path_T1'] not in final_train:
        final_train.append(aa)    
        healthy_train_size=healthy_train_size-1
        
while ms_train_size > 0:
	ll = random.choice(restrict_MS)
	if ll['path_T1'] not in final_train:
		final_train.append(ll)
		ms_train_size = ms_train_size-1



#Make the Test folder
healthy_test_size = test_size//2
ms_test_size = test_size//2
final_test=[]

while healthy_test_size > 0: 
    i = random.choice(healthy)
    if i['path_T1'] not in final_train:
        if i['path_T1'] not in final_test:
            final_test.append(i)
            healthy_test_size=healthy_test_size-1   

while ms_test_size > 0:
	n = random.choice(MS)
	if n['path_T1'] not in final_test:
		final_test.append(n)
		ms_test_size = ms_test_size-1



#Example print the path_T1 of all test elements and the size of 'test'
# for h, algo in enumerate(final_train):
#     print(algo['path_T1'])
#     size_train = h

# for h, algo in enumerate(final_test):
#     print(algo['path_T1'])
#     size_test = h

# print(total_size)
# print(size_test)
# print(size_train)

print("division done, results in final_test and final_train")

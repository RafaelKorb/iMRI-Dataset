import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

dataframe = pd.read_json('data.json')

#only_females = dataframe.loc[dataframe['sex']=='F']
#only_age_major_than_30 = dataframe.loc[dataframe['age'] >='30']

#select the patients that you want
normals = dataframe.loc[dataframe['MS']=='False']
ms = dataframe.loc[dataframe['MS']=='True']


#construct subset dataframe with random 30 normals and random 30 MS
dataframe2=pd.DataFrame(columns=dataframe.columns)
chosen_idx = np.random.choice(len(normals), replace=False, size=30) #rand numbers
#dataframe2 = dataframe2.append(normals.iloc[chosen_idx])
#chosen_idx = np.random.choice(len(ms), replace=False, size=30) #rand numbers
dataframe2 = dataframe2.append(ms.iloc[chosen_idx])

#separate in test train
train, test = train_test_split(dataframe2, test_size=0.25)

print 'Train:',len(train)
print 'Test:',len(test) 
print "Test size is 25 per cent and Train is 75 per cent, as defined."

#print first row
print dataframe2.iloc[0] 

print 'path_T1 of first row:',dataframe2['path_T1_pre'].iloc[0] 

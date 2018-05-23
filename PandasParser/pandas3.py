# -*- coding: utf-8 -*-
"""
Created on Tue May  1 08:17:44 2018
@author: striteskyt
"""
import pandas as pd
import time
import datetime


#file location
path = '/run/user/1000/gvfs/smb-share:server=srcryapp13,share=departments/Molding Center/PredictiveMaintenance/Test1/'
#File name
ps_file = 'plantstar.csv'
#pandas dataform
df = pd.read_csv(path + ps_file)
#Pandas get needed variables for Initial State
data1 = df[['Date','Cycle ID','CycleTime']]
#Find last Cyle ID 
data2 = df[['Cycle ID']]
max_id = data2.max()
start = max_id.iloc[0]
#Starting Cylcle ID for next data sent to Initial State 
nextdata = start + 1

d2 = data2[df['Cycle ID'] > start]

s = pd.Series(start)
s.to_csv(path + 'start1.csv', index=False)
max_id.to_csv(path + 'max1.csv',header=False, index=False)


#print data1
print max_id
#print data2
print start
print nextdata
#print d2




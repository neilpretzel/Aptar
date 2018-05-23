# -*- coding: utf-8 -*-
"""
Created on Tue May  1 08:17:44 2018
@author: striteskyt
"""
import pandas as pd


#file location
path = '/run/user/1000/gvfs/smb-share:server=srcryapp13,share=departments/Molding Center/PredictiveMaintenance/Test1/'
#File name
ps_file = 'plantstar.csv'

df = pd.read_csv(path + ps_file,index_col=None)
df.set_index('Cycle ID',drop=False,append=True)


data1 = df[['Date','Cycle ID','CycleTime']]
data2 = df[['Cycle ID']]

start = 39063
d2 = data2[df['Cycle ID'] > start]

top = d2.head(1)
bottom = data2.tail(1)
max_id = data2.max()

data_1 = data2['Cycle ID']
#data_2 = data_1.iloc[bottom]
print d2
print bottom
print max_id
max1 = max_id.iloc[0]
print max1



a = bottom[0:1]
print a
#print df
#print d2
print data1



#print('Shape', df.shape)
#print('-------------------------')
#print('Number of rows', len(df))
print('-------------------------')
#print('Column headers', df.columns)
#print('-------------------------')
#print('Data types', df.dtypes)
#print('-------------------------')
#print('Index', df.index)
#print('-------------------------')


# -*- coding: utf-8 -*-
"""
Created on Tue May  1 08:17:44 2018
@author: striteskyt
"""
import pandas as pd

#Read starting row for Initail Satate export






#file location /run/user/1000/gvfs/
path = 'smb-share:server=srcryapp13,share=departments/Molding Center/PredictiveMaintenance/Test1/'
#File name
ps_file = 'plantstar.csv'
#pandas dataform
df = pd.read_csv(path + ps_file)
#Pandas get needed variables for Initial State



#Find last Cycle ID 
c_id_last = df[['Cycle ID']].max()
c_id_last.to_csv(path + 'last.csv',mode='a',header=False, index=False)
print c_id_last
#Find next cycle id to start next export "This needs to be cleaned up"
nd = c_id_last.iloc[0]
nextdata = nd - 2 #change this to + 1 after start files are created
data3 = df[['Cycle ID']]
data4 = data3[df['Cycle ID'] > nextdata]
data4.to_csv(path + 'next.csv',mode='a',header=False, index=False)
print nextdata
print data4

#Export Data
initialS = df[['Date','Cycle ID','CycleTime']]
#print initialstate_export

#df.loc[;,['Cycle ID']] = nextdata[['Cycle ID']].values
#df['Cycle ID' <= 39080].value






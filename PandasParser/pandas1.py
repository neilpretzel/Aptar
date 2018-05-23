# -*- coding: utf-8 -*-
"""
Created on Tue May  1 08:17:44 2018

@author: striteskyt
"""

import pandas as pd
import matplotlib.pyplot as plt



path = '/run/user/1000/gvfs/smb-share:server=srcryapp13,share=departments/Molding Center/PredictiveMaintenance/Test1/'

ps_file = "plantstar.csv"

df = pd.read_csv(path + ps_file, )
dfb = pd.read_csv(path + ps_file, header=None, index_col=None)

data1 = df[["Date","Cycle ID","CycleTime"]]
data2 = df[["Cycle ID"]]


#print data1
##print s
#st = s[:5] 
#print st


start = 39063
s2 = data1[df["Cycle ID"] > start]

top = s2.head(1)
bottom = data2.tail(1)

print s2
#print top
#print bottom
#print dfb




#data1.set_index("Date", inplace=True)
#data1.plot()
#plt.show()


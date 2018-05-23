# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 11:44:41 2018

@author: striteskyt
"""

import csv
import itertools
 
#csv file name
filename = "/run/user/1000/gvfs/smb-share:server=wcnl2h72,share=vmware_ubuntu/Test1/plantstar.csv"

# Make an empty list
processdata = []
idstamp = []
fields = []

with open(filename,"r") as process_data:
 
     # Set up CSV reader and process the header
    csvReader = csv.reader(process_data)
    header = csvReader.next()
    date_time = header.index('Date')
    cycle_time = header.index('CycleTime')
    cycle_id = header.index('Cycle ID')
 
# Loop through the lines in the file 

    for row in csvReader:
        cycle = row[cycle_time]
        cycleid = row[cycle_id]
        time_stamp = row[date_time]
        processdata.append([time_stamp,cycleid,cycle])
        
    # Print the coordinate list
print processdata
print len(processdata)
print cycleid
print("Total no. of rows: %d"%(csvReader.line_num))  

for row in processdata[:2]:
    for col in row:
       # print ('\n')
        print ("%7s"%col) #indents
        #print ('\n')
        
        
# https://codereview.stackexchange.com/questions/142142/extracting-specific-rows-and-columns-from-a-csv-file
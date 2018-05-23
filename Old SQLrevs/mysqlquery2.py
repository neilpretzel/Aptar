# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 11:01:20 2018

@author: striteskyt
"""
#from __future__ import print_function
import datetime
import mysql.connector
from mysql.connector import errorcode



try:

    config = {
        'host':'172.20.1.21',
        'user':'report',
        'passwd':'report',
        'db':'focus2000',   
        
    }
    
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    querry = ("SELECT idx, sample_time, sample_1, sample_2, sample_3, sample_4, sample_5 "
              "FROM spc_hist ORDER by sample_time desc "
              "LIMIT 10")
    
    cursor.execute(querry)
     
    result = cursor.fetchall()
    #result = cursor.fetchmany(size=20)
    
    print "Raw Data"
    for row in result:
      print(row)
    
    print""
    print "Touple format"
    for (idx, sample_time, sample_1, sample_2, sample_3, sample_4, sample_5) in result:
        print("{:%U %x %X}   {}, {}, {}, {},{}, {},".format(sample_time, idx, sample_1, sample_2, sample_3, sample_4, sample_5))
      
      
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
    
  else:
    print(err)
    
else: 
   
    cursor.close()
    cnx.close()
    
    
    
    
    
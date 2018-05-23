# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 09:42:32 2018

@author: striteskyt
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 16:45:51 2018
@author: striteskyt
"""
import datetime
import time
import mysql.connector
from mysql.connector import errorcode
import csv


machine = 'IC000001'
begin_date = datetime.date(2018, 4, 12) # year, month, day ####, ##, ##
end_date = ''
first_idx = '1'
last_idx = '12'
limit_size = 200


try:
    start = time.time() #timer for script
    
    config = {
        'host':'172.20.1.21',
        'user':'report',
        'passwd':'report',
        'db':'focus2000',      
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    cursor.execute("SELECT "
                  "jts_hist_base.job_seq, "
                  "jts_hist_base.mach_seq, "
                  "jts_hist_base.mach_name, " 
                  "spc_hist.sample_time, "
                  "spc_hist.idx, "
                  "spc_hist.sample_1, "
                  "spc_hist.sample_2, "
                  "spc_hist.sample_3, "
                  "spc_hist.sample_4, "
                  "spc_hist.sample_5 "
             
             "From "
                  "jts_hist_base "  
                  
             "JOIN "                   
                  "spc_hist "
                  
             "ON "
                  "jts_hist_base.job_seq = spc_hist.job_seq "
                  
             "WHERE jts_hist_base.mach_name = %s AND  spc_hist.sample_time >= %s AND spc_hist.idx BETWEEN %s AND %s" # machine,firts_index,last_index  
            
             "ORDER BY "
                  "sample_time DESC, "
                  "spc_hist.idx ASC " #remove to speed up query
                  
              "Limit "
                '%s ',[(machine),(begin_date),(first_idx),(last_idx),(limit_size)]) #limit_size
  
    result = cursor.fetchall()   
 
    for (job_seq, mach_seq, mach_name, sample_time, idx, sample_1, sample_2, sample_3, sample_4, sample_5) in result:   
      print("{:%x %X} {}, {}, {}, {}, {}, {}, {}, {}, {}".format(sample_time, mach_name, job_seq, mach_seq, idx, sample_1, sample_2, sample_3, sample_4, sample_5))  
    
    print '\nIt took', time.time()-start, 'seconds to run this querry on', datetime.datetime.now().strftime("%x %X"),'\n'     
    
      
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
    
    
    
    
    
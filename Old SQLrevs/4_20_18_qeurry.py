# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 15:14:34 2018

@author: striteskyt
"""

import datetime
import time
import mysql.connector
from mysql.connector import errorcode
import csv
from ISStreamer.Streamer import Streamer

machine = 3613947
begin_date = datetime.date(2018, 4, 17) # year, month, day ####, ##, ##
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
                    "job_cur_base.job_seq, "
                    "job_cur_base.mach_seq, "
                    "spc_hist.idx, "
                    "mach_def.mach_name, "
                    "MAX(spc_hist.sample_time), "
                    "spc_hist.sample_1, "
                    "spc_hist.sample_2, "
                    "spc_hist.sample_3, "
                    "spc_hist.sample_4, "
                    "spc_hist.sample_5 "
                             
             "From spc_hist "  
                  
             "JOIN job_cur_base ON spc_hist.job_seq = job_cur_base.job_seq "
             "JOIN mach_def ON job_cur_base.mach_seq = mach_def.mach_seq "
             "JOIN job_cur_pvar ON job_cur_base.mach_seq = job_cur_pvar.mach_seq "
                  
             "WHERE job_cur_base.mach_seq = %s "
            
             "GROUP BY spc_hist.idx "
             
             "ORDER BY sample_time DESC, spc_hist.idx ASC " 
                  
    ,[(machine)])
               
   
    result = cursor.fetchall()
    
    for (job_seq, mach_seq, idx, mach_name, sample_time, sample_1, sample_2, sample_3, sample_4, sample_5) in result:   
      print("{:%x %X} {}, {}, {}, {}, {}, {}, {}, {}, {}".format(sample_time, job_seq, mach_seq, mach_name, idx, sample_1, sample_2, sample_3, sample_4, sample_5))  
    
    print '\nIt took', time.time()-start, 'seconds to run this querry on', datetime.datetime.now().strftime("%x %X"),'\n'     
      
    fp = open('plantstar2.csv', 'a')
    myFile = csv.writer(fp)
    myFile.writerows(result)
    fp.close()  
     
      
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
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 11:35:28 2018

@author: pretkelisn
"""

from __future__ import division
import time
import mysql.connector
from mysql.connector import errorcode
from ISStreamer.Streamer import Streamer

# https://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python
# https://www.esri.com/arcgis-blog/products/product/analytics/scheduling-a-python-script-or-model-to-run-at-a-prescribed-time/

try:
    
    # connect to mySQL database
    config = {
        'host':'172.20.1.21',
        'user':'report',
        'passwd':'report',
        'db':'focus2000',      
    }
    
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
     
    cursor.execute("""
    SELECT
    
        spc_hist.sample_time,
        spc_hist.sample_1,
        spc_hist.sample_2,
        spc_hist.sample_3,
        spc_hist.sample_4,
        spc_hist.sample_5
            
    FROM spc_hist
       
    JOIN job_cur_base ON spc_hist.job_seq = job_cur_base.job_seq 
    JOIN mach_def ON job_cur_base.mach_seq = mach_def.mach_seq 
       
    WHERE mach_def.mach_name = 'IC000008' 
       
    ORDER BY sample_time DESC, spc_hist.idx ASC
       
    LIMIT 1500;
    """)
   
    result = cursor.fetchall() 
    
#        dt = result[0][0]
#        data_time = time.mktime(dt.timetuple()) - 7200
#        data_time_alt = totimestamp(result[0][0])
    
    #streamer = Streamer(bucket_name= "Machine 8", bucket_key= "SNSQ7RXYS8GF", access_key= "w5fQGZJFbysVOi2Hw9jQeKLYYAhJdQb7")
    streamer = Streamer(bucket_name= "Testing3", bucket_key= "P36WQPGBHQFT", access_key= "w5fQGZJFbysVOi2Hw9jQeKLYYAhJdQb7")
    
    for x in range(0, 1500):
        idx_number = x%15 + 1;
        if idx_number >= 9:
            idx_number += 1
        string = "idx"+`idx_number`
        for y in range(1, 6):
            data = result[x][y]
            dt = result[x][0]
            data_time = time.mktime(dt.timetuple()) - 7200
            streamer.log(string, data, data_time)
            time.sleep(0.01)
        time.sleep(0.01)
        
#        print result[0][0]
#        print data_time 
#        print data_time_alt
    
    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")

  elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")

  else:
      print(err)
      #time.sleep(300)
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 11:35:28 2018

@author: Neil Pretkelis
"""

from __future__ import division
import sys
import time
import logging
import mysql.connector
from mysql.connector import errorcode
from ISStreamer.Streamer import Streamer

# https://www.esri.com/arcgis-blog/products/product/analytics/scheduling-a-python-script-or-model-to-run-at-a-prescribed-time/
logging.basicConfig(filename='exceptions.log', level=logging.DEBUG)

while True:
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
    
        # execute this SQL code, mach_name will change based on what machine
        # you want data from. This code will grab the datetime of the most 
        # recent sample. This code can be copied and pasted into mySQL.
        cursor.execute("""
        SELECT spc_hist.sample_time 
        FROM spc_hist
        JOIN job_cur_base ON spc_hist.job_seq = job_cur_base.job_seq 
        JOIN mach_def ON job_cur_base.mach_seq = mach_def.mach_seq 
        WHERE mach_def.mach_name = 'IC000008'
        ORDER BY sample_time DESC 
        LIMIT 1;
        """)
        
        # set a variable equal to the most recent sample time
        check_time = cursor.fetchall()
        
        # set a variable equal to the last sample time taken, held in txt file
        readfile = open('current_txt_time_IS.txt', 'r')
        current_time = readfile.read()
        readfile.close
    
        # if the last data taken from Plantstar is not the most recent
        if str(check_time) != str(current_time):
            
            # This makes sure the txt file rewrites to match the current date
            # Without this it would only work 2/3rds of the time likely due to
            # timing or memory issue
            while True:
                writefile = open('current_txt_time_IS.txt', 'w')
                writefile.write(str(check_time))
                writefile.close
                readfile = open('current_txt_time_IS.txt', 'r')
                current_time = readfile.read()
                readfile.close
                
                # if the txt date and Plantstar date match, exit while-loop
                if str(check_time) == str(current_time): 
                    break
                
            # this executes SQL code to be written into a CSV file. 
            # mach_name would need to be changed for each machine.                          
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
               
            LIMIT 15;
            """)
           
            result = cursor.fetchall() 
            
            dt = result[0][0]
            data_time = time.mktime(dt.timetuple()) - 7200
            
            #streamer = Streamer(bucket_name= "Machine 8", bucket_key= "SNSQ7RXYS8GF", access_key= "w5fQGZJFbysVOi2Hw9jQeKLYYAhJdQb7")
            streamer = Streamer(bucket_name= "Testing2", bucket_key= "ET8L9R3LVVA3", access_key= "w5fQGZJFbysVOi2Hw9jQeKLYYAhJdQb7", debug_level=1)
            
            for x in range(0, 15):
                idx_number = x + 1;
                if idx_number >= 9:
                    idx_number += 1
                string = "idx"+`idx_number`
                for y in range(1, 6):
                    data = result[x][y]
                    streamer.log(string, data, data_time)
            
            print result[0][0]
            print data_time
    
        cursor.close()
        cnx.close()
    
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print "Something is wrong with your user name or password"
          logging.info("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
          print "Database does not exist"
          logging.info("Database does not exist")
      else:
          print "An unknown mySQL database error occured"
          logging.info("An unknown mySQL database error occured")
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
        logging.info("I/O error({0}): {1}".format(errno, strerror))
    except:
        print "Unexpected error:", sys.exc_info[0]
        logging.info("Unexpected error:", sys.exc_info[0])
        raise
    time.sleep(300)
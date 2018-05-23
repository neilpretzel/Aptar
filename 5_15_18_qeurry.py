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

while True:
    
    try:
        start = time.time() #timer for script
        
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
        readfile = open('\\current_txt_time.txt', 'r')
        current_time = readfile.read()
        readfile.close
        
        # These prints are for visualization of code as it is running
#        print "Time from txt file:", current_time
#        print "Time from database:", check_time
    
        # if the last data taken from Plantstar is not the most recent
        if str(check_time) != str(current_time):
            
            # This makes sure the txt file rewrites to match the current date
            # Without this it would only work 2/3rds of the time likely due to
            # timing or memory issue
            while True:
                writefile = open('current_txt_time.txt', 'w')
                writefile.write(str(check_time))
                writefile.close
                readfile = open('current_txt_time.txt', 'r')
                current_time = readfile.read()
                readfile.close
                
                # if the txt date and Plantstar date match, exit while-loop
                if str(check_time) == str(current_time): 
                    break
                
            # this executes SQL code to be written into a CSV file. 
            # mach_name would need to be changed for each machine.
            cursor.execute("""
            SELECT
                mach_def.mach_name,
                spc_hist.idx,
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
            
            # This is for visualization of code working and how fast it takes
#            print '\nIt took', time.time()-start, 
#            'seconds to run this querry on',
#            datetime.datetime.now().strftime("%x %X"),'\n'     
              
            # Open the CSV file and write (append) to it the SQL data
            fp = open('plantstar.csv', 'a')
            myFile = csv.writer(fp)
            myFile.writerows(result)
            fp.close()
            
        cursor.close()
        cnx.close()
        
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("Something is wrong with your user name or password")
    
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
          print("Database does not exist")
    
      else:
          print(err)
    time.sleep(600)
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 16:31:17 2018

@author: striteskyt
"""

import pymysql


# open connection to the database  
conn = pymysql.connect(host='172.20.1.21',  
                       port=3306,  
                       user='report',  
                       passwd='report',  
                       db='focus2000',  
                       charset='utf8')  
cur = conn.cursor()  

#sql = "SELECT * FROM <your_favourite_table>"  
sql = "SELECT * FROM focus2000.eos_hist;"
cur.execute(sql)  

print(cur.description)
print()

for row in cur:
    print(row)



# close connection to the database  
cur.close()  
conn.close(  )

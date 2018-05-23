# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 21:27:51 2018
 
@author: striteskyt
"""
from __future__ import print_function
import MySQLdb as my
 
db = my.connect(host="172.20.1.21",
user="report",
passwd="report",
db="focus2000"
)
 
#cursor = db.cursor()
# 
#number_of_rows = cursor.execute("select * from eos_hist");
# 
#result = cursor.fetchall()
# 
#print(result)
# 
#db.close()


 
cursor = db.cursor()
 
number_of_rows = cursor.execute("select * from eos_hist limit 100");
 
result = cursor.fetchall()

for row in result:
  print(row)
 
db.close()
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:56:36 2018

@author: Cameron
"""

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","pythonUser","abc","dddm" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "SELECT * FROM PLANT_LOCATIONS \
       WHERE State = 'LA'"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
      # Now print fetched result
      print( "Facility Name=%s" % ('Facility Name'))
except:
   print( "Error: unable to fecth data")

# disconnect from server
db.close()
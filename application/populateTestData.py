# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 17:10:08 2018

@author: Beth
"""

import mysqlConnection as md
import pandas as pd
import populateModelData as model

def populateData(radius, actualValue):
    
    #select all zipcodes from table
    query = "select Zip FROM dddm.test_zips"
    data = pd.read_sql(query, md.connect())
    
    allzipList = data['Zip'].tolist()
    print(len(allzipList))
    
    #select inserted zipcodes
    #query2 = "SELECT distinct(zip) FROM dddm.test_zip_data"
    #q2data = pd.read_sql(query2, md.connect())
    
    #storedZip = q2data['zip'].tolist()
    #print(len(storedZip))
        
    for zipcode in allzipList:
        updatedZip = str(int(zipcode)) 
        if len(str(int(zipcode))) == 3:
            updatedZip = str(0) + str(0) + updatedZip
        elif len(str(int(zipcode))) == 4:
            updatedZip = str(0) + updatedZip
        model.addToTestTable(updatedZip, radius, actualValue)
        print("Processed " + updatedZip)
    
#populateData(50, 'None')
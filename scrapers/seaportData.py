# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 18:05:15 2018

@author: Cameron
"""

import mysqlConnection as md
import zipcodeDistance as zd

def getSeaPortData(zipcode, radius):
    engine = md.connect()
    
    zipdf = zd.getZipcodes(zipcode, radius)
    
    #parse dataframe zipdf to extract zipcodes
    zipList = zipdf['zip_code'].tolist()
    #print(zipList)
    
    #extract landprices from mysql by zipcodes from land_prices_final table
    query = "SELECT * from dddm.seaports_final where ZIPCODE in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
    print('Query: ' + str(query))
    
    with engine.connect() as con:
        data = con.execute(query)
        
    rowCount = 0
    for row in data:
        rowCount += 1
     
    return rowCount

print('Number of ports: ' + str(getSeaPortData('78402', 10)))
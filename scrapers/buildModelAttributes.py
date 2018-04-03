# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 18:35:16 2018

@author: Cameron


This program builds attributes for each input into the model.
All functions are called at the bottom.

"""

import mysqlConnection as md
import zipcodeDistance as zd
import pandas as pd

def getSeaPortData(engine, zipcode, zipList):    
    #extract landprices from mysql by zipcodes from land_prices_final table
    query = "SELECT * from dddm.seaports_final where ZIPCODE in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
    
    with engine.connect() as con:
        data = con.execute(query)
        
    rowCount = 0
    for row in data:
        rowCount += 1
     
    return rowCount

def getLandPricesData(engine, zipcode, zipList):    
    #extract landprices from mysql by zipcodes from land_prices_final table
    query = "SELECT * from dddm.land_prices_final where zip in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
        
    data = pd.read_sql(query, engine)
    avgCostIndex = data['Land Price Index Normalized'].mean()
    return avgCostIndex

def getOilReservesData(engine, zipcode, zipList):
    #extract landprices from mysql by zipcodes from land_prices_final table
    query = "SELECT * from dddm.oil_reserve_final where zip in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
    
    with engine.connect() as con:
        data = con.execute(query)
        
    maxOilReserves = 0
    rowCount = 0
    for row in data:
        if int(row['year16'].replace(',','')) > maxOilReserves:
            maxOilReserves = int(row['year16'].replace(',',''))
        rowCount += 1
     
    return maxOilReserves

def buildAll(zipcode, radius):
    
    # Gets zipcode right here to only call API once per run
    engine = md.connect()
    zipdf = zd.getZipcodes(zipcode, radius)
    zipList = zipdf['zip_code'].tolist()
    
    #print('Number of sea ports: ' + str(getSeaPortData(engine, zipcode, zipList)))
    print('Land price rating: ' + str(getLandPricesData(engine, zipcode, zipList)))
    #print('Oil reserves available: ' + str(getOilReservesData(engine, zipcode, zipList)))

""" For testing purposes only """
buildAll('75098', 20)
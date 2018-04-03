# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 18:35:16 2018

@author: Cameron


This program builds attributes for each input into the model.
All functions are called at the bottom.

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
    
    with engine.connect() as con:
        data = con.execute(query)
        
    rowCount = 0
    for row in data:
        rowCount += 1
     
    return rowCount

def getLandPricesData(zipcode, radius):
    engine = md.connect()
    
    zipdf = zd.getZipcodes(zipcode, radius)
    
    #parse dataframe zipdf to extract zipcodes
    zipList = zipdf['zip_code'].tolist()
    #print(zipList)
    
    #extract landprices from mysql by zipcodes from land_prices_final table
    query = "SELECT * from dddm.land_prices_final where zip in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
    
    with engine.connect() as con:
        data = con.execute(query)
        
    landPriceSum = 0
    rowCount = 0
    for row in data:
        landPriceSum += row[6]
        rowCount += 1
    
    if rowCount == 0:
        return 0
     
    return landPriceSum/rowCount

def getOilReservesData(zipcode, radius):
    engine = md.connect()
    
    zipdf = zd.getZipcodes(zipcode, radius)
    
    #parse dataframe zipdf to extract zipcodes
    zipList = zipdf['zip_code'].tolist()
    #print(zipList)
    
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
    print('Number of sea ports: ' + str(getSeaPortData(zipcode, radius)))
    print('Land price rating: ' + str(getLandPricesData(zipcode, radius)))
    print('Oil reserves available: ' + str(getOilReservesData(zipcode, radius)))
    # Needs to be finished ...

""" To run full model """
#buildAll('78390', 50)

""" For testing purposes only """
#print('Number of sea ports: ' + str(getSeaPortData('78402', 10)))
#print('Land price rating: ' + str(getLandPricesData('14208', 10)))
#print('Oil reserves available: ' + str(getOilReservesData('78390', 10)))
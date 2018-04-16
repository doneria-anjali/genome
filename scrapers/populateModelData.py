#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 21:56:28 2018

@author: anjali
"""
import mysqlConnection as md;
import zipcodeDistance as zd
import pandas as pd
import buildModelAttributes as attr

def getDFForZip(zipcode, radius, actualVal):
    engine = md.connect()
    zipdf = zd.getZipcodes(zipcode, radius)
    zipList = zipdf['zip_code'].tolist()
    
    df = pd.DataFrame(columns=['zip','seaport','landprice','oilreserve',
                               'existingplants','disasters','railroad',
                               'populationdensity', 'actual','elevation'])
    listData = pd.DataFrame([[zipcode,
                attr.getSeaPortData(engine, zipcode, zipList),
                attr.getLandPricesData(engine, zipcode, zipList),
                attr.getOilReservesData(engine, zipcode, zipList),
                attr.getExistingPlants(engine, zipcode, zipList),
                attr.getDisasterData(engine, zipcode, zipList),
                attr.getRailroadData(engine, zipcode, zipList),
                attr.getPopulationDensityData(engine, zipcode, zipList),
                actualVal,
                attr.fetch_elevation_data(engine, zipcode)]], 
                columns=['zip','seaport','landprice','oilreserve',
                               'existingplants','disasters','railroad',
                               'populationdensity', 'actual','elevation'])
    df = df.append(listData, ignore_index=True)
    return engine, df

def addToTable(zipcode, radius=50, actualVal='N'):
    engine, df = getDFForZip(zipcode, radius, actualVal)
    df.to_sql(name='model_data', con=engine, if_exists='append', index=False)
    print("Added " + str(zipcode) + " successfully.")
    
#addToTable('27606', actualVal='N')
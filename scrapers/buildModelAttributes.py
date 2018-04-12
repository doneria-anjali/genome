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
    query = "SELECT * from dddm.seaports_final where ZIPCODE in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
        
    data = pd.read_sql(query, engine)
    num = len(data.index)
    if num == 0:
        return 1
    elif num < 2:
        return 2
    return 3

def getLandPricesData(engine, zipcode, zipList):
    query = "SELECT * from dddm.land_prices_final where zip in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
        
    data = pd.read_sql(query, engine)
    
    #Account for missing data by return -1
    if len(data.index) == 0:
        return -1
    
    avgCostIndex = data['structure_cost_norm'].mean()
    if avgCostIndex < 0.33:
        return 3
    elif avgCostIndex < 0.67:
        return 2
    return 1

def getOilReservesData(engine, zipcode, zipList):
    query = "SELECT * from dddm.oil_reserve_final where zip in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
        
    data = pd.read_sql(query, engine)
    oilReserves = data['year16_norm'].max()
    if oilReserves == 0:
        return 1
    elif oilReserves < .5:
        return 2
    return 3

def getExistingPlants(engine, zipcode, zipList):
    query = "SELECT * from dddm.plant_locations where zip_code in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
        
    data = pd.read_sql(query, engine)
    num = len(data.index)
    if num == 0:
        return 1
    elif num < 3:
        return 2
    return 3

def getDisasterData(engine, zipcode, zipList):
    query = "SELECT * from dddm.disaster_data_final where zip in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
        
    data = pd.read_sql(query, engine)
    #Account for missing data by return 3 because no natural disasters
    if len(data.index) == 0:
        return 3
    
    fireMentions = data['NumFireReferences'].mean()
    floodMentions = data['NumFloodReferences'].mean()
    hurricaneMentions = data['NumHurricaneReferences'].mean()
    
    overallMean = (fireMentions + floodMentions + hurricaneMentions) / 3
    if overallMean == 0:
        return 3
    elif overallMean < .5:
        return 2
    return 1

def getRailroadData(engine, zipcode, zipList):
    query = "SELECT * from dddm.railroad_data_final where zip in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
        
    data = pd.read_sql(query, engine)
    #Account for missing data by return 3 because no natural disasters
    if len(data.index) == 0:
        return -1
    
    avgFreightTons = data['Tons_norm'].mean()

    if avgFreightTons == 0:
        return 1
    elif avgFreightTons < .3:
        return 2
    return 3

def getPopulationDensityData(engine, zipcode, zipList):
    query = "SELECT * from dddm.population_density_final where zip in ("
    query += "'" + zipcode + "',"
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
        
    data = pd.read_sql(query, engine)
    #Account for missing data by return 3 because no natural disasters
    if len(data.index) == 0:
        return -1
    
    density = data['density_norm'].mean()

    if .2 < density < .5:
        return 3
    elif .1 < density < .6:
        return 2
    return 1

def getDFForZip(zipcode, radius, actualVal):
    engine = md.connect()
    zipdf = zd.getZipcodes(zipcode, radius)
    zipList = zipdf['zip_code'].tolist()
    
    df = pd.DataFrame(columns=['zip','seaport','landprice','oilreserve',
                               'existingplants','disasters','railroad',
                               'populationdensity', 'actual'])
    listData = pd.DataFrame([[zipcode,
                getSeaPortData(engine, zipcode, zipList),
                getLandPricesData(engine, zipcode, zipList),
                getOilReservesData(engine, zipcode, zipList),
                getExistingPlants(engine, zipcode, zipList),
                getDisasterData(engine, zipcode, zipList),
                getRailroadData(engine, zipcode, zipList),
                getPopulationDensityData(engine, zipcode, zipList),
                actualVal]], 
                columns=['zip','seaport','landprice','oilreserve',
                               'existingplants','disasters','railroad',
                               'populationdensity', 'actual'])
    df = df.append(listData, ignore_index=True)
    return df

def addToTable(zipcode, radius=50, actualVal='N'):
    df = getDFForZip(zipcode, radius, actualVal)
    print(df)
    
addToTable('10001')
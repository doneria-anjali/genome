# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 18:35:16 2018

@author: Cameron


This program builds attributes for each input into the model.
All functions are called at the bottom.

"""

import mysqlConnection as md
#import zipcodeDistance as zd
import pandas as pd
import simplejson
import urllib.request

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
        return 3
    elif num < 3:
        return 2
    return 1

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
        return -1
    
    fireMentions = data['NumFireReferences_norm'].mean()
    floodMentions = data['NumFloodReferences_norm'].mean()
    hurricaneMentions = data['NumHurricaneReferences_norm'].mean()
    
    overallMean = (fireMentions + floodMentions + hurricaneMentions) / 3
    if overallMean < .2:
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
    #Account for missing data by return -1
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

    if .000000001 < density < .01:
        return 3
    elif density < .03:
        return 2
    return 1

def fetch_earthquake_data(zipcode):
    engine = md.connect()
    #fetch latitude and longitude for zipcode
    query1 = "SELECT * FROM dddm.zip_lookup where zip = '" + zipcode + "'"
    zip_data = pd.read_sql(query1, engine)
    
    coord = 2.5
    lat_range1 = str(int(zip_data['lat']) + coord)
    lat_range2 = str(int(zip_data['lat']) - coord)
    
    lng_range1 = str(int(zip_data['lng']) + coord)
    lng_range2 = str(int(zip_data['lng']) - coord)
    
    query2 = "SELECT * from dddm.earthquake_data where latitude BETWEEN '" 
    + lat_range2 + "' and '" + lat_range1 + "' AND longitude BETWEEN '" 
    + lng_range2 + "' and '" + lng_range1 + "'"
    earthquake_data = pd.read_sql(query2, engine)        
    
    return earthquake_data

#fetch rules
#Qualitative Data
def fetch_rules():
    engine = md.connect()
    query = "SELECT * FROM dddm.rules"
    rules_data = pd.read_sql(query, engine)
    
    return rules_data
    
#fetch water data
def fetch_water_data(zipcode):
    engine = md.connect()
    query1 = "SELECT * FROM dddm.zip_lookup where zip = '" + zipcode + "'"
    zip_data = pd.read_sql(query1, engine)
    
    coord = 2.5
    lat_range1 = str(int(zip_data['lat']) + coord)
    lat_range2 = str(int(zip_data['lat']) - coord)
    
    lng_range1 = str(int(zip_data['lng']) + coord)
    lng_range2 = str(int(zip_data['lng']) - coord)
    
    query2 = "SELECT * FROM dddm.water_locations where LatitudeMeasure BETWEEN '" 
    + lat_range2 + "' and '" + lat_range1 + "' AND LongitutdeMeasure BETWEEN '" 
    + lng_range2 + "' and '" + lng_range1 + "'"
    water_data = pd.read_sql(query2, engine)
    
    return water_data
    
#fetch elevation data from google API
def fetch_elevation_data(engine, zipcode):
    #engine = md.connect()
    zipcode = str(int(zipcode))
    print(zipcode)
    query = "SELECT * FROM dddm.zip_lookup where zip = '" + zipcode + "' OR zip='0" + zipcode +"' OR zip = '00" + zipcode +"'"
    zip_data = pd.read_sql(query,engine)
    
    if len(zip_data.index) == 0:
        return -1
    #print(zip_data)
    
    latitude = str(zip_data.iloc[0]['lat'])
    longitude = str(zip_data.iloc[0]['lng'])
    
    base_url = "https://maps.googleapis.com/maps/api/elevation/json?locations="
    key_url = "&key=AIzaSyAbFTeYx8kS0d7jH20xcm05QEUCDcdhL3U"
    location = latitude + "," + longitude
    api_url = base_url + location +key_url
    
    json_output = simplejson.load(urllib.request.urlopen(api_url))
    result = float(json_output["results"][0]["elevation"])
    
    if(-1 < result <= 1029.00):
        return 3
    elif(1029.00 < result <= 2058):
        return 2
    return 1

#fetch weather data
def fetch_weather_data(zipcode):
    engine = md.connect()
    query1 = "SELECT * FROM dddm.zip_lookup where zip = '" + zipcode + "'"
    zip_data = pd.read_sql(query1, engine)
    
    state = str(int(zip_data['state_id']))
    
    query2 = "SELECT * FROM dddm.weather_observations where State = '" + state + "'"
    weather_data = pd.read_sql(query2, engine)
    
    return weather_data

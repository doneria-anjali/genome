#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 20:54:12 2018

@author: anjali
"""

import mysqlConnection as md
import buildModelAttributes as attr
import zipcodeDistance as zd
import pandas as pd

def connect():
    return md.connect()

#method to fetch attributes of a given zipcode at runtime
def fetch_features(zipcode, radius):
    engine = connect()
    zipdf = zd.getZipcodes(zipcode, radius)
    zipList = zipdf['zip_code'].tolist()
    
    listData = [[zipcode,
                attr.getSeaPortData(engine, zipcode, zipList),
                attr.getLandPricesData(engine, zipcode, zipList),
                attr.getOilReservesData(engine, zipcode, zipList),
                attr.getExistingPlants(engine, zipcode, zipList),
                attr.getDisasterData(engine, zipcode, zipList),
                attr.getRailroadData(engine, zipcode, zipList),
                attr.getPopulationDensityData(engine, zipcode, zipList),
                attr.fetch_elevation_data(engine, zipcode)]]
    
    return listData

#method to fetch features from DB
def fetch_features_from_db(zipcode):
    engine = connect()
    query = "SELECT seaport, landprice, oilreserve, existingplants, disasters,railroad,populationdensity,elevation from dddm.test_zip_data where zip = '" + str(zipcode) + "' or zip = '" + str(0) + str(zipcode) + "'"
    #query = "SELECT seaport, landprice, oilreserve, existingplants, disasters,railroad,populationdensity,elevation from dddm.test_zip_data_all where zip = '" + str(zipcode) + "' or zip = '" + str(0) + str(zipcode) + "'"
    test_df = pd.read_sql(query, engine)
    #print(test_df)
    df = [[test_df.iloc[0]['seaport'], 
           test_df.iloc[0]['landprice'], 
           test_df.iloc[0]['oilreserve'], 
           test_df.iloc[0]['existingplants'],
           test_df.iloc[0]['disasters'],
           test_df.iloc[0]['railroad'],
           test_df.iloc[0]['populationdensity'],
           test_df.iloc[0]['elevation']]]
    
    #print(df)
    return df
    
def run_model_for_prediction(zipcode, model):
    #fetch all the features for zipcode to run the model
    #test_df = fetch_features(zipcode, radius)
    test_df = fetch_features_from_db(zipcode)
    
    #predict
    prediction = model.predict(test_df)
    #print(prediction)
    return prediction, test_df
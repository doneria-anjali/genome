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
                attr.getPopulationDensityData(engine, zipcode, zipList)]]
    
    return listData

    
def run_model_for_prediction(zipcode, radius, model):
    #fetch all the features for zipcode to run the model
    test_df = fetch_features(zipcode, radius)
    print(test_df)
    #predict
    prediction = model.predict(test_df)
    
    return prediction, test_df
    
    
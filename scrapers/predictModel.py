#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 20:54:12 2018

@author: anjali
"""

import mysqlConnection as md
import buildModelAttributes as bmod
import zipcodeDistance as zd
import pandas as pd

def connect():
    return md.connect()

def fetch_features(zipcode, radius):
    engine = connect()
    zipdf = zd.getZipcodes(zipcode, radius)
    zipList = zipdf['zip_code'].tolist()
    
    df = pd.DataFrame(columns=['zip','seaport','landprice','oilreserve',
                               'existingplants','disasters','railroad',
                               'populationdensity'])
    listData = pd.DataFrame([[zipcode,
                bmod.getSeaPortData(engine, zipcode, zipList),
                bmod.getLandPricesData(engine, zipcode, zipList),
                bmod.getOilReservesData(engine, zipcode, zipList),
                bmod.getExistingPlants(engine, zipcode, zipList),
                bmod.getDisasterData(engine, zipcode, zipList),
                bmod.getRailroadData(engine, zipcode, zipList),
                bmod.getPopulationDensityData(engine, zipcode, zipList)]], 
                columns=['zip','seaport','landprice','oilreserve',
                               'existingplants','disasters','railroad',
                               'populationdensity'])
    df = df.append(listData, ignore_index=True)
    return df

    
def run_model_for_prediction(zipcode, radius, model):
    #fetch all the features for zipcode to run the model
    test_df = fetch_features(zipcode, radius)
    
    #TODO : finish prediction fxn call on gaussian model
    
    
    return prediction, test_df
    
    
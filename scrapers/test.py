#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 21:45:17 2018

@author: anjali
"""

import application as app
import pandas as pd
import mysqlConnection as md
import predictModel as predict
import buildModel as build

def test():
    #fetch all the zipcodes for project
    query = "SELECT Zip FROM dddm.test_zips"
    zip_df = pd.read_sql(query, md.connect())
    zip_list = zip_df['Zip'].tolist()
    
    #build a dataframe and push to table
    df = pd.DataFrame(columns=['zip','seaport','landprice','oilreserve',
                               'existingplants','disasters','railroad',
                               'populationdensity', 'elevation', 'water', 
                               'weather', 'rules','earthquake','prediction'])
    
    for zipcode in zip_list:
        result = app.app(zipcode, 50)
        listData = pd.DataFrame([[zipcode,
                                  result.prediction_df['seaport'],
                                  result.prediction_df['landprice'],
                                  result.prediction_df['oilreserve'],
                                  result.prediction_df['existingplants'],
                                  result.prediction_df['disasters'],
                                  result.prediction_df['railroad'],
                                  result.prediction_df['populationdensity'],
                                  result.elevation_data,
                                  result.water_data,
                                  result.weather_data,
                                  result.rules,
                                  result.earthquake_data,
                                  result.prediction]], 
                                columns=['zip','seaport','landprice','oilreserve',
                               'existingplants','disasters','railroad',
                               'populationdensity', 'elevation', 'water', 
                               'weather', 'rules','earthquake','prediction'])
        df = df.append(listData, ignore_index=True)
        df.to_sql(name='test_data', con=md.connect(), if_exists='append', index=False)
        
def test_data():
    #fetch all the zipcodes for project
    query = "SELECT Zip FROM dddm.test_zips"
    zip_df = pd.read_sql(query, md.connect())
    zip_list = zip_df['Zip'].tolist()
    
    model = build.build_gaussian_model()
    
    for zipcode in zip_list:
        prediction, prediction_df = predict.run_model_for_prediction(zipcode, 50, model)
        print("zip:" + str(zipcode) + ", prediction:" + prediction[0])
        print()
        
test_data()
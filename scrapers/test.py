#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 21:45:17 2018

@author: anjali
"""

import application as app
import pandas as pd
import mysqlConnection as md

def test():
    #fetch all the zipcodes for project
    query = "SELECT zip FROM dddm.zips_for_project"
    zip_df = pd.read_sql(query, md.connect())
    zip_list = zip_df['zip'].tolist()
    
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
        
test()
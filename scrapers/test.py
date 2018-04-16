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
import csv

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
        
def test_data_gaussian():
    #fetch all the zipcodes for project
    query = "SELECT Zip FROM dddm.test_zips"
    zip_df = pd.read_sql(query, md.connect())
    zip_list = zip_df['Zip'].tolist()
    
    #file = open("output/gaussian.csv", "w")
    #writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    
    #Train over Gaussian NB model
    model = build.build_gaussian_model()
    for zipcode in zip_list:
        prediction, prediction_df = predict.run_model_for_prediction(zipcode, model)
        string = str(zipcode) + "," + prediction[0]
        print(string)
        #writer.writerow(string)
    #file.close()

def test_data_adaboost():
    #fetch all the zipcodes for project
    query = "SELECT Zip FROM dddm.test_zips"
    zip_df = pd.read_sql(query, md.connect())
    zip_list = zip_df['Zip'].tolist()
    
    #Train over Adaboost model
    model = build.build_adaboost_model()
    for zipcode in zip_list:
        prediction, prediction_df = predict.run_model_for_prediction(zipcode, model)
        string = str(zipcode) + "," + prediction[0]
        print(string)

def test_data_decision_tree():
    #fetch all the zipcodes for project
    query = "SELECT Zip FROM dddm.test_zips"
    zip_df = pd.read_sql(query, md.connect())
    zip_list = zip_df['Zip'].tolist()
    
    model = build.build_decision_tree_model()
    for zipcode in zip_list:
        prediction, prediction_df = predict.run_model_for_prediction(zipcode, model)
        string = str(zipcode) + "," + prediction[0]
        print(string)
        
def test_data_random_forest():
    #fetch all the zipcodes for project
    query = "SELECT Zip FROM dddm.test_zips"
    zip_df = pd.read_sql(query, md.connect())
    zip_list = zip_df['Zip'].tolist()
    
    model = build.build_random_forest_model()
    for zipcode in zip_list:
        prediction, prediction_df = predict.run_model_for_prediction(zipcode, model)
        string = str(zipcode) + "," + prediction[0]
        print(string)
    
#test_data_gaussian()
#test_data_adaboost()
#test_data_decision_tree()
#test_data_random_forest()
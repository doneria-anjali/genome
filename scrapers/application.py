#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 21:34:35 2018

@author: anjali
"""
import predictModel as predict
import buildModel as build
import buildModelAttributes as attr
import populateGoodData as good
import populateBadData as bad
#import pandas as pd
import time

#define class to hold all the data in the object
class result_data():
    #declare attributes
    #declare two constructors
    def __init__(self,elevation_data, water_data, weather_data, earthquake_data, rules, prediction_df):
      self.elevation_data = elevation_data
      self.water_data = water_data
      self.weather_data = weather_data
      self.earthquake_data = earthquake_data
      self.rules = rules
      self.prediction_df = prediction_df
      
    def __init__(self,prediction_df):
        self.prediction_df = prediction_df
        
    #declare print()
    def print():
        print("Elevation Data - " + elevation_data)
        print("Water_data - " + water_data)
        print("Weather_data - " + weather_data)
        print("Earthquake_data - " + earthquake_data)
        print("Rules - " + rules)
        print("Feature set - " + prediction_df)
    
def app(zipcode, radius):
    start_time = time.time()
    
    #1. populate data in model_data for given radius
    #good data
    good.populateData(radius, 'Y')
    #bad data
    bad.populateData(radius, 'N')
    
    #2. Build model and train it
    model = build.build_gaussian_model()
    
    #3. Test model for given zipcode and radius
    prediction, prediction_df = predict.run_model_for_prediction(zipcode, radius, model)
    
    #if prediction is Yes 
    #check for elevation data
    if prediction == 'Y':
        elevation_data = attr.fetch_elevation_data(zipcode)
        #fetch water data
        water_data = attr.fetch_water_data(zipcode)
        #fetch weather data
        weather_data = attr.fetch_weather_data(zipcode)
        #fetch water rules
        earthquake_data = attr.fetch_earthquake_data(zipcode)
        #fetch rules for drilling oil reserves
        rules = attr.fetch_rules()
        
        #make result object
        result = result(elevation_data, water_data, weather_data, earthquake_data, rules, prediction_df)
    else:
        result = result(prediction_df)
    
    #print execution time
    print()
    print("--- %s seconds ---" % (time.time() - start_time))
        
    return prediction, result
    

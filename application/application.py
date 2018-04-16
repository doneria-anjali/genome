#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 21:34:35 2018

@author: anjali
"""
import predictModel as predict
import buildModel as build
import buildModelAttributes as attr
#import populateGoodData as good
#import populateBadData as bad
#import pandas as pd
import time

#define class to hold all the data in the object
class result_data():
    #declare attributes
    #declare two constructors
    def __init__(self, water_data, 
                 weather_data, earthquake_data, rules, prediction_df, prediction, zipcode):
      self.water_data = water_data
      self.weather_data = weather_data
      self.earthquake_data = earthquake_data
      self.rules = rules
      self.prediction_df = prediction_df
      self.prediction = prediction
      self.zipcode = zipcode
      
    
def app(zipcode, radius):
    start_time = time.time()
    
    #1. populate data in model_data for given radius
    #good data
    #good.populateData(radius, 'Y')
    #bad data
    #bad.populateData(radius, 'N')
    
    #2. Build model and train it
    model = build.build_gaussian_model()
    
    #3. Test model for given zipcode and radius
    prediction, prediction_df = predict.run_model_for_prediction(zipcode, model)
    
    #if prediction is Yes 
    #check for elevation data
    if prediction[0] == 'Y':
        #elevation_data = attr.fetch_elevation_data(zipcode)
        #fetch water data
        water_data = attr.fetch_water_data(zipcode)
        #fetch weather data
        weather_data = attr.fetch_weather_data(zipcode)
        #fetch water rules
        earthquake_data = attr.fetch_earthquake_data(zipcode)
        #fetch rules for drilling oil reserves
        rules = attr.fetch_rules()
        
        #make result object
        resultData = result_data(water_data, weather_data, 
                                 earthquake_data, rules, prediction_df, prediction[0], zipcode)
    else:
        resultData = result_data(None, None, None, None, prediction_df, prediction[0],
                                 zipcode)
    
    #print execution time
    print("--- %s seconds ---" % (time.time() - start_time))
        
    return resultData

#app('12288', 50)


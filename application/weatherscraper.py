# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:09:26 2018

@author: Beth
"""

import pandas as pd
import mysqlConnection as md

def import_weather(file_name):
    df_weather = pd.read_csv("resources/" + file_name, low_memory=False)
    df_weather = df_weather[['StationName', 'Date', 'ObsType', 'Value', 'S-Flag', 'City', 'State']]  
    
    md.create_table(md.connect(), df_weather, 'weather_observations')

import_weather('10citiesweather.csv')
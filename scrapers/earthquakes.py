# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 21:02:31 2018

@author: Beth
"""

import pandas as pd
import mysqlConnection as md

def import_earthquakes():
    df_earthquakes = pd.read_csv("resources/USEarthquakes.csv", low_memory=False)
    df_earthquakes = df_earthquakes[['time', 'latitude', 'longitude', 'mag', 'magType', 'place']]  
    df_earthquakes2 = pd.read_csv("resources/AKEarthquakes.csv", low_memory=False)
    df_earthquakes2 = df_earthquakes2[['time', 'latitude', 'longitude', 'mag', 'magType', 'place']]
    df_earthquakes.append(df_earthquakes2)
    md.create_table(md.connect(), df_earthquakes, 'earthquake_data')

import_earthquakes()
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 03:53:33 2018

@author: Beth
"""

import pandas as pd
import mysqlConnection as md

def import_water_data(file_name):
    data = pd.read_csv('resources/' + file_name)
    data = data[['MonitoringLocationTypeName', 'LatitudeMeasure', 'LongitudeMeasure']]
    #data.to_sql(name='water_locations', con=dbEngine, if_exists = 'replace')
    md.create_table(md.connect(), data, 'water_locations')

import_water_data('waterlocations.csv')
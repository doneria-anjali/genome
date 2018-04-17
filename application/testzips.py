# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 16:46:40 2018

@author: Beth
"""

import pandas as pd
import mysqlConnection as md

def import_smaller_zips(file_name):
    data = pd.read_csv('resources/' + file_name)
    data = data[['City', 'State', 'Zip']]
    #data.to_sql(name='water_locations', con=dbEngine, if_exists = 'replace')
    md.create_table(md.connect(), data, 'test_zips')

import_smaller_zips('testProjectZips.csv')
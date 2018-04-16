# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:15:22 2018

@author: Cameron
"""

import pandas as pd
import mysqlConnection as md

def import_existing_plants(file_name):
    plant_locations = pd.read_csv('resources/' + file_name)
    plant_locations = plant_locations[['Facility Name', 'Deregistered (Yes/No)','City', 'State', 'Zip Code', 
                                       'Parent Company', 'Latitude','Longitude', 'Number of RMP Submissions']]
    plant_locations = plant_locations[plant_locations.State.notnull()]
    #plant_locations.to_sql(name='plant_locations', con=dbEngine, if_exists = 'replace')
    
    md.create_table(md.connect(), plant_locations, 'plant_locations')
    
import_existing_plants('plant_locations.csv')
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:15:22 2018

@author: Cameron
"""

import pandas as pd

def main():
    plant_locations = pd.read_csv("plant_locations.csv")
    plant_locations = plant_locations[plant_locations.State.notnull()]
    print(plant_locations.shape)
    
    # low_memory=False : fixes warnings about mixed types because dropping those columns in next step anyways
    railroad_locations = pd.read_csv("Railroad_Crossings.csv", low_memory=False) 
    railroad_locations = railroad_locations[['RAILROAD', 'StateCode','LATITUDE', 'LONGITUD']]
    print(railroad_locations.shape)
    
main()
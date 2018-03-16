# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:45:40 2018

@author: Cameron
"""

import pandas as pd

def main():
    
    # low_memory=False : fixes warnings about mixed types because dropping those columns in next step anyways
    railroad_locations = pd.read_csv("Railroad_Crossings.csv", low_memory=False) 
    railroad_locations = railroad_locations[['RAILROAD', 'StateCode','LATITUDE', 'LONGITUD']]
    print(railroad_locations.shape)
    
main()
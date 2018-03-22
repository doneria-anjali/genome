# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:15:22 2018

@author: Cameron
"""

import pandas as pd

def main():
    plant_locations = pd.read_csv("resources/plant_locations.csv")
    plant_locations = plant_locations[plant_locations.State.notnull()]
    print(plant_locations.shape)
    
main()
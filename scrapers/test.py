#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 21:45:17 2018

@author: anjali
"""

import application as app
import pandas as pd
import mysqlConnection as md

def test():
    #fetch all the zipcodes for project
    query = "SELECT zip FROM dddm.test_zips"
    zip_df = pd.read_sql(query, md.connect())
    zip_list = zip_df['Zip'].tolist()
    
    result_list = []
    for zipcode in zip_list:
        result = app.app(zipcode, 50)
        result_list.append(result)
        
test()
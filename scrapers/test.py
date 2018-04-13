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
    query = "SELECT zip FROM dddm.zips_for_project"
    zip_df = pd.read_sql(query, md.connect())
    zip_list = zip_df['zip'].tolist()
    
    result_list = []
    for zipcode in zip_list:
        result = app.app(zipcode, 50)
        result.print()
        result_list.append(result)
        
test()
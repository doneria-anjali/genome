# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 16:07:40 2018

@author: Cameron
"""

import pandas as pd
import mysqlConnection as md
        
def import_land_prices(file_name):
    df_landprices = pd.read_excel('resources/' + file_name)
    md.create_table(md.connect(), df_landprices, 'railroad_data')
    
import_land_prices('railroad_data.xlsx')   
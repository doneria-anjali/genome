# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:09:43 2018

@author: adity
"""

import pandas as pd
import mysqlConnection as md
        
def import_land_prices(file_name):
    df_landprices = pd.read_excel('resources/' + file_name, skiprows=[0], parse_cols="A,B,C,D,E,H,I")
    df_landprices = df_landprices.loc[df_landprices['Date'] == '2015Q4']
    df_landprices['MSA'] = df_landprices.MSA.str.replace(' ', '')
    #df_landprices.to_sql(name='land_prices', con=dbEngine, index=False, if_exists = 'replace')
    md.create_table(md.connect(), df_landprices, 'land_prices')
    
import_land_prices('landdata-msas-2016q1.xls')      

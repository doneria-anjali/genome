# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:56:33 2018

@author: adity
"""

import mysqlConnection as md
import pandas as pd

def import_seaports(file_name):
    df_ports = pd.read_csv("resources/" + file_name, low_memory=False)
    df_ports = df_ports[['LATITUDE1', 'LONGITUDE1', 'CITY_OR_TO', 'STATE_POST', 'ZIPCODE', 'PORT_NAME']]  
    #df_ports.to_sql(name='seaports', con=dbEngine, if_exists = 'replace')
    
    md.create_table(md.connect(), df_ports, 'seaports')

import_seaports('Ports.csv')
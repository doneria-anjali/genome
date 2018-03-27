# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:56:33 2018

@author: adity
"""

from sqlalchemy import create_engine
import pandas as pd

def connect():
    """ Connect to MySQL database after filling out below parameters"""
    engine = create_engine('mysql+pymysql://pythonUser:abc@localhost:3306/dddm?charset=utf8', encoding='utf-8')
    return engine
        
def create_table(dbEngine):
    df_ports = pd.read_csv("resources/Ports.csv", low_memory=False)
    df_ports = df_ports[['LATITUDE1', 'LONGITUDE1', 'CITY_OR_TO', 'STATE_POST', 'ZIPCODE', 'PORT_NAME']]  
    df_ports.to_sql(name='seaports', con=dbEngine, if_exists = 'replace')
        
engine = connect()
create_table(engine)
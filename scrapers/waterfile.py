# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 03:53:33 2018

@author: Beth
"""

import pandas as pd
from sqlalchemy import create_engine

def connect():
    """ Connect to MySQL database after filling out below parameters"""
    engine = create_engine('mysql+pymysql://pythonUser:abc@localhost:3306/dddm?charset=utf8', encoding='utf-8')
    return engine
        
def create_table(dbEngine):
    data = pd.read_csv('resources/waterlocations.csv') 
    data = data[['MonitoringLocationTypeName', 'LatitudeMeasure', 'LongitudeMeasure']]
    data.to_sql(name='water_locations', con=dbEngine, if_exists = 'replace')
        
engine = connect()
create_table(engine)
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 14:15:22 2018

@author: Cameron
"""

from sqlalchemy import create_engine
import pandas as pd


def connect():
    """ Connect to MySQL database after filling out below parameters"""
    engine = create_engine('mysql+pymysql://pythonUser:abc@localhost:3306/dddm?charset=utf8', encoding='utf-8')
    return engine
        
def create_table(dbEngine):
    plant_locations = pd.read_csv("resources/plant_locations.csv")
    plant_locations = plant_locations[['Facility Name', 'Deregistered (Yes/No)','City', 'State', 'Zip Code', 
                                       'Parent Company', 'Latitude','Longitude', 'Number of RMP Submissions']]
    plant_locations = plant_locations[plant_locations.State.notnull()]
    plant_locations.to_sql(name='plant_locations', con=dbEngine, if_exists = 'replace')
    
engine = connect()
create_table(engine)
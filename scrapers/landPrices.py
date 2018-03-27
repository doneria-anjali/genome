# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:09:43 2018

@author: adity
"""

import pandas as pd
from sqlalchemy import create_engine

def connect():
    """ Connect to MySQL database after filling out below parameters"""
    engine = create_engine('mysql+pymysql://pythonUser:abc@localhost:3306/dddm?charset=utf8', encoding='utf-8')
    return engine
        
def create_table(dbEngine):
    df_landprices = pd.read_excel("resources/landdata-msas-2016q1.xls", skiprows=[0], parse_cols="A,B,C,D,E,H,I")
    df_landprices = df_landprices.loc[df_landprices['Date'] == '2015Q4']
    df_landprices['MSA'] = df_landprices.MSA.str.replace(' ', '')
    df_landprices.to_sql(name='land_prices', con=dbEngine, index=False, if_exists = 'replace')
        
engine = connect()
create_table(engine)
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 17:29:35 2018

@author: Cameron
"""

import mysqlConnection as md
import pandas as pd

def add_bad_data(engine):
    df = pd.read_csv('exported_data/model_bad.csv')
    df.to_sql(name='model_data', con=engine, if_exists='append', index=False)
    
def add_good_data(engine):
    df = pd.read_csv('exported_data/model_good.csv')
    df.to_sql(name='model_data', con=engine, if_exists='append', index=False)

def add_all_data(engine):
    df = pd.read_csv('exported_data/model_data.csv')
    df.to_sql(name='model_data', con=engine, if_exists='append', index=False)

def add_test_data(engine):
    df = pd.read_csv('exported_data/test_data.csv')
    df.to_sql(name='test_zip_data', con=engine, if_exists='append', index=False)
    
""" Comment out the data already imported """
engine = md.connect()
#add_bad_data(engine)
#add_good_data(engine)
add_all_data(engine)
add_test_data(engine)
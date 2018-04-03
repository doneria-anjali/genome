# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 17:15:49 2018

@author: adity
"""

import mysqlConnection as md
import pandas as pd

def normalize_all():
    engine = md.connect()
    df = pd.read_sql_table('land_prices', engine)
    df['Home Value-norm'] = (df['Home Value'] - df['Home Value'].min())/(df['Home Value'].max() - df['Home Value'].min())
    df['Structure Cost-norm'] = (df['Structure Cost'] - df['Structure Cost'].min())/(df['Structure Cost'].max() - df['Structure Cost'].min())
    md.create_table(engine, df, 'land_prices')
    
    df = pd.read_sql_table('oil_reserve_final', engine)
    df['year16'] = df['year16'].str.replace(',','').astype(float)
    df['year16_norm'] = (df['year16'] - df['year16'].min())/(df['year16'].max() - df['year16'].min())
    md.create_table(engine, df, 'oil_reserve_final')
    
    
normalize_all()
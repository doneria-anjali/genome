# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 17:15:49 2018

@author: adity
"""

import mysqlConnection as md
import pandas as pd

def normalize_all():
    engine = md.connect()
    #normalize land prices
    df = pd.read_sql_table('land_prices_final', engine)
    df['home_value_norm'] = (df['Home Value'] - df['Home Value'].min())/(df['Home Value'].max() - df['Home Value'].min())
    df['structure_cost_norm'] = (df['Structure Cost'] - df['Structure Cost'].min())/(df['Structure Cost'].max() - df['Structure Cost'].min())
    md.create_table(engine, df, 'land_prices_final')
    
    #normalize oil reserve data
    df = pd.read_sql_table('oil_reserve_final', engine)
    df['year16'] = df['year16'].str.replace(',','').astype(float)
    df['year16_norm'] = (df['year16'] - df['year16'].min())/(df['year16'].max() - df['year16'].min())
    md.create_table(engine, df, 'oil_reserve_final')
    
    #normalize disaster data
    df = pd.read_sql_table('disaster_data_final', engine)
    df['NumFireReferences_norm'] = (df['NumFireReferences'] - df['NumFireReferences'].min())/(df['NumFireReferences'].max() - df['NumFireReferences'].min())
    df['NumFloodReferences_norm'] = (df['NumFloodReferences'] - df['NumFloodReferences'].min())/(df['NumFloodReferences'].max() - df['NumFloodReferences'].min())
    df['NumHurricaneReferences_norm'] = (df['NumHurricaneReferences'] - df['NumHurricaneReferences'].min())/(df['NumHurricaneReferences'].max() - df['NumHurricaneReferences'].min())
    md.create_table(engine, df, 'disaster_data_final')
    
    #normalize railroad data
    df = pd.read_sql_table('railroad_data_final', engine)
    df['Tons_norm'] = (df['Tons'] - df['Tons'].min())/(df['Tons'].max() - df['Tons'].min())
    md.create_table(engine, df, 'railroad_data_final')
    
    #normalize population density data
    df = pd.read_sql_table('population_density', engine)
    df['density_norm'] = (df['density'] - df['density'].min())/(df['density'].max() - df['density'].min())
    md.create_table(engine, df, 'population_density_final')
    
normalize_all()
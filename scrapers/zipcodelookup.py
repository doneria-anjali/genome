# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:52:33 2018

@author: Cameron
"""

import pandas as pd
from sqlalchemy import create_engine

def main():
    initial = pd.read_csv('resources/uscitiesdata.csv')
    initial['city'] = initial['city'].str.replace(' ', '').str.upper()
    
    seperatedZips = (initial['zip'].str.strip()).str.split(expand=True)
    
    fullData = pd.concat([initial, seperatedZips], axis=1)
    fullData = fullData.drop(['zip'], axis=1)
    
    idvars = ['city', 'state_id', 'state_name', 'county_name', 
              'lat', 'lng', 'population']
    
    allZips = pd.melt(fullData, id_vars=idvars, value_name='zip')
    allZips = allZips.drop(['variable'], axis=1)
    
    # Drops columns with missing zip code values
    allZips = allZips[pd.notnull(allZips.zip)]
    
    engine = create_engine('mysql+pymysql://pythonUser:abc@localhost:3306/dddm?charset=utf8', encoding='utf-8')
    allZips.to_sql(name='zip_lookup', con=engine, if_exists = 'replace')
    
    """ Zip Code lookup table complete, Ready to be joined """
    
    
    """
    Tests joining with land cost data by City and State
    """
    
#    # Reads in land cost data (Need to manuall add States)
#    #    Still needs to finish adding in state codes
#    df_landprices = pd.read_excel("landdata-msas-2016q1.xls", skiprows=[0], parse_cols="A,B,C,D,E,H,I")
#    df_landprices = df_landprices.loc[df_landprices['Date'] == '2015Q4']
#    
#    # Merges data based on city (Still need to make case match to get results)
#    df = pd.merge(df_landprices, allZips,  how='left', left_on=['MSA','State'], right_on = ['city','state_id'])
#    print(df.head(20))
    
    
main()
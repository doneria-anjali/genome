# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:56:36 2018

@author: Cameron
"""

import pymysql
from sqlalchemy import create_engine
import pandas as pd

"""
Before running this, open Anaconda Prompt and run:

conda install -c anaconda sqlalchemy
conda install -c anaconda pymysql

- Create schema called dddm for this project
- Fill in the below parameters in the create_engine method
to match your DB credentials.
"""

def connect():
    """ Connect to MySQL database after filling out below parameters"""
    engine = create_engine('mysql+pymysql://anjali:spring2018@localhost:3306/dddm')
    return engine
        
def create_table(dbEngine):
    df = pd.read_csv('resources/UNdata_Export_20180314_030619219.txt', sep="|", header=None, 
                            names=["Year","Sex","City","Source Year","Value","Value Footnotes"])
    df_copy = df.drop(['Value Footnotes','Source Year'], axis = 1)
    print(len(df_copy))
    print(df_copy.head(5))
    df_copy.to_sql(name='us_census_data', con=dbEngine, if_exists = 'replace')
        
engine = connect()
# Below does not work yet
create_table(engine)
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
    engine = create_engine('mysql+pymysql://[username]:[password]@localhost:3306/dddm')
    return engine
        
def create_table(dbEngine):
    data = pd.read_csv('uscitiesdata.csv')
    data.to_sql(name='sample_table', con=dbEngine, if_exists = 'repalace')
        
engine = connect()
# Below does not work yet
#create_table(engine)
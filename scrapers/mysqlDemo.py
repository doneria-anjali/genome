# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 11:56:36 2018

@author: Cameron
"""

import mysqlConnection as md
import pandas as pd
    
def test(file_name):
    data = pd.read_csv('resources/' + file_name)
    engine = md.connect()
    md.create_table(engine, data, 'sample_table2')

test('uscitiesdata.csv')
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 16:21:48 2018

@author: Cameron
"""

import pandas as pd
import mysqlConnection as md

df = pd.read_csv('resources/population_density.csv', sep=",")  
md.create_table(md.connect(), df, 'population_density')
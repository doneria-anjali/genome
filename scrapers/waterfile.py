# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 03:53:33 2018

@author: Beth
"""

import pandas as pd

df = pd.read_csv('/Users/Beth/CSC495/waterlocations.csv')
df
print(df.head(50)) 
print(len(df))
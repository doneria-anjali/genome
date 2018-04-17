# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 13:29:55 2018

@author: Beth
"""

import pandas as pd
import mysqlConnection as md

df = pd.read_csv('resources/BadZipCodes.csv', sep=",")  
md.create_table(md.connect(), df, 'unfavorable_zipcodes')
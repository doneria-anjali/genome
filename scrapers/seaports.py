# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:56:33 2018

@author: adity
"""

import pandas as pd

df_ports = pd.read_csv("C:/Users/adity/Downloads/NCSU Study/Semester II/Data Driven Decision Making/Project/Ports.csv")

df_ports = df_ports.iloc[:,(2,10,11,12,13,18,19,25)]

print(df_ports)

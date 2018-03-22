# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:09:26 2018

@author: Beth
"""

import pandas as pd

df3 = pd.read_csv('/Users/Beth/CSC495/genome/resources/smallerweather2016.csv') 
print(len(df3))
df3 = df3.drop(df3[df3.index > 12561444].index)
print(df3.head(50)) 
print(len(df3))
df3.to_csv('../resources/smallerweather2016part1.csv')

df4 = pd.read_csv('/Users/Beth/CSC495/genome/resources/smallerweather2016.csv') 
print(len(df4))
df4 = df4.drop(df4[df4.index < 12561445].index)
print(df4.head(50)) 
print(len(df4))
df4.to_csv('../resources/smallerweather2016part2.csv')

df = pd.read_csv('/Users/Beth/CSC495/genome/resources/smallerweather2017.csv') 
print(len(df))
df = df.drop(df[df.index > 12359466].index)
print(df.head(50)) 
print(len(df))
df.to_csv('../resources/smallerweather2017part1.csv')

df2 = pd.read_csv('/Users/Beth/CSC495/genome/resources/smallerweather2017.csv') 
print(len(df2))
df2 = df2.drop(df2[df2.index < 12359467].index)
print(df2.head(50)) 
print(len(df2))
df2.to_csv('../resources/smallerweather2017part2.csv')
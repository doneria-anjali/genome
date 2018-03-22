# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:09:43 2018

@author: adity
"""

import pandas as pd

def main():
   df_landprices = pd.read_excel("resources/landdata-msas-2016q1.xls", parse_cols="A,B,E")

   df_landprices['Year'] = df_landprices.Date.str[:4]

   df_landprices = df_landprices.drop(['Date'], axis=1)

   df_landprices = df_landprices.groupby(['MSA','Year']).mean()

   print(df_landprices)
   
main()
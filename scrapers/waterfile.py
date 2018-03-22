# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 03:53:33 2018

@author: Beth
"""

import pandas as pd

def main():
   df = pd.read_csv('resources/waterlocations.csv')
   print(df.head(50)) 
   print(len(df))
   
main()
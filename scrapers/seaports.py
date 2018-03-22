# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 11:56:33 2018

@author: adity
"""

import pandas as pd

def main():
   df_ports = pd.read_csv("resources/Ports.csv")

   df_ports = df_ports.iloc[:,(2,10,11,12,13,18,19,25)]

   print(df_ports)

main()
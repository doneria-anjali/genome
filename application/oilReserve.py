# -*- coding: utf-8 -*-
"""
@author: Anjali
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import mysqlConnection as md

class OilReserveData:
    def __init__(self, state, year11, year12, year13, year14, year15, year16):
        self.state = state
        self.year11 = year11
        self.year12 = year12
        self.year13 = year13
        self.year14 = year14
        self.year15 = year15
        self.year16 = year16

    def to_dict(self):
        return {
            'state': self.state,
            'year11': self.year11,
            'year12': self.year12,
            'year13': self.year13,
            'year14': self.year14,
            'year15': self.year15,
            'year16': self.year16,
        }

def import_oil_reserve(name):
    page = requests.get(name)

    soup = BeautifulSoup(page.content, 'lxml')

    table = soup.find('table', attrs={'class': 'data1'})

    rows = table.findAll('tr', attrs={'class' : 'DataRow'})

    values = []

    for tr in rows:
        state = tr.find('td', attrs={'class' : 'DataStub1'}).get_text()

        otherYear = tr.findAll('td', attrs={'class' : 'DataB'})
        y11 = otherYear[0].get_text()
        y12 = otherYear[1].get_text()
        y13 = otherYear[2].get_text()
        y14 = otherYear[3].get_text()
        y15 = otherYear[4].get_text()

        current = tr.find('td', attrs={'class' : 'Current2'}).get_text()

        values.append(OilReserveData(state, y11, y12, y13, y14, y15, current))

    df = pd.DataFrame.from_records([s.to_dict() for s in values])

    md.create_table(md.connect(), df, 'oil_reserve')
    #df.to_sql(name='oil_reserve', con=engine, if_exists = 'replace')


import_oil_reserve('http://www.eia.gov/dnav/ng/ng_enr_sum_a_EPG0_R21_BCF_a.htm')


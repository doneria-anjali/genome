# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 13:32:33 2018

@author: Cameron
"""

import requests
import json
import pandas as pd

key = 'HQSYxGwUOWqXzEKasRoRSwmxgnSYJWCzr9BS3hFUqrFUbNeGiXIIATRYz3FLQJRU'
#zipcode = '27518'
#radius = 5

def getZipcodes(zipcode, radius):
    url = 'https://www.zipcodeapi.com/rest/' + key + '/radius.json/' + zipcode + '/' + str(radius) + '/miles'

    response = requests.get(url)

    # For successful API call, response code will be 200 (OK)
    if(response.ok):

        jData = json.loads(response.content)
        zipCodeResponse = jData['zip_codes']
        dfResponse = pd.DataFrame(zipCodeResponse)
        #print(dfResponse)

    # If response code is not ok (200), print the resulting http error code with description
    else:
        response.raise_for_status()
    
    return dfResponse
        
        
print(getZipcodes('14208', 10))
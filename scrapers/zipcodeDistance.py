# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 13:32:33 2018

@author: Cameron
"""

import requests
import json
import pandas as pd

#Cameron
#key = 'HQSYxGwUOWqXzEKasRoRSwmxgnSYJWCzr9BS3hFUqrFUbNeGiXIIATRYz3FLQJRU'
#key = 'NOdiwrYn7IPVDqnNrZKeE6fapsffVUceXVbSMgVe2Hc8P0bKS9veH7gwYVhff8hO'

#Anjali
key = 'Y6VXTVs1carp0WhJ6OM3l8gsg8477wHTY3Hg0RVmUZonmjVxegve518oC5QFp0kC'
#key = 'JQpX0MtDR3FWIJI61mvGAOR5YsMi8jw8HeSgrVtvv6toWkN4DUHwZgJWJUORimx5'
#key = 'JdY2oWbDTkWbNd9J46JDtWxLHvdUGN0RVAKoqOLIHjPKemygxdVGoyHrbQXDeDDz'

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
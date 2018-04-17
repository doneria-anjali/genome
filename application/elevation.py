# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 16:36:30 2018

@author: adity
"""
#import googlemaps
import simplejson
import urllib.request
#from datetime import datetime

#gmaps = googlemaps.Client(key='AIzaSyAbFTeYx8kS0d7jH20xcm05QEUCDcdhL3U')

# Geocoding an address
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
BASE_URL = "https://maps.googleapis.com/maps/api/elevation/json?locations="
KEY_URL = "&key=AIzaSyAbFTeYx8kS0d7jH20xcm05QEUCDcdhL3U"
LOCATIONS_URL = "23.66,45.77"

FINAL_URL = BASE_URL + LOCATIONS_URL + KEY_URL

#print(FINAL_URL)

json_output = simplejson.load(urllib.request.urlopen(FINAL_URL))

#print(json_output)

print(json_output["results"][0]["elevation"])
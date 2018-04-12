import mysqlConnection as md
import zipcodeDistance as zd
import pandas as pd
import buildModelAttributes as model

def populateData(radius, actualValue):
    #select zipcodes from table
    query = "select distinct(zip_code) FROM dddm.plant_locations limit 0,50"
    data = pd.read_sql(query, md.connect())
    
    zipList = data['zip_code'].tolist()
    
    for zipcode in zipList:
        model.addToTable(zipcode, radius, actualValue)
        print("Processed " + zipcode)
        break
    
populateData(50, 'Y')
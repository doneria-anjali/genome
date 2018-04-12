import mysqlConnection as md
import zipcodeDistance as zd
import pandas as pd
import buildModelAttributes as model

def populateData(radius, actualValue):
    #select zipcodes from table
    query = "select distinct(zip_code) FROM dddm.plant_locations limit 0,40"
    data = pd.read_sql(query, md.connect())
    
    zipList = data['zip_code'].tolist()
        
    for zipcode in zipList:
        updatedZip = str(int(zipcode))
        if len(str(int(zipcode))) == 3:
            updatedZip = str(00) + updatedZip
        elif len(str(int(zipcode))) == 4:
            updatedZip = str(0) + updatedZip
        model.addToTable(updatedZip, radius, actualValue)
        print("Processed " + updatedZip)
    
populateData(50, 'Y')
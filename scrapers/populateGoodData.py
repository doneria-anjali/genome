import mysqlConnection as md
import zipcodeDistance as zd
import pandas as pd
import buildModelAttributes as model

def populateData(radius, actualValue):
    #select all zipcodes from table
    query = "select distinct(zip_code) FROM dddm.plant_locations order by zip_code asc"
    data = pd.read_sql(query, md.connect())
    
    allzipList = data['zip_code'].tolist()
    print(len(allzipList))
    
    #select inserted zipcodes #Anjali
    query2 = "SELECT distinct(zip) FROM dddm.model_data"
    q2data = pd.read_sql(query2, md.connect())
    
    storedZip = q2data['zip'].tolist()
    print(len(storedZip))
        
    for zipcode in allzipList:
        if not zipcode in storedZip:
            updatedZip = str(int(zipcode))
            if len(str(int(zipcode))) == 3:
                updatedZip = str(0) + str(0) + updatedZip
            elif len(str(int(zipcode))) == 4:
                updatedZip = str(0) + updatedZip
            model.addToTable(updatedZip, radius, actualValue)
            print("Processed " + updatedZip)
    
populateData(50, 'Y')
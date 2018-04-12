import mysqlConnection as md
import pandas as pd
import buildModelAttributes as model

def populateData(radius, actualValue):
    
    #select all zipcodes from table
    query = "select distinct(zip_code) FROM dddm.plant_locations limit 0,49"
    data = pd.read_sql(query, md.connect())
    
    allzipList = data['zip_code'].tolist()
    print(len(allzipList))
    for zipcode in allzipList:
        updatedZip = str(int(zipcode))
        if len(str(int(zipcode))) == 3:
            updatedZip = str(0) + str(0) + updatedZip
        elif len(str(int(zipcode))) == 4:
            updatedZip = str(0) + updatedZip
        model.addToTable(updatedZip, radius, actualValue)
        print("Processed " + updatedZip)
    
populateData(50, 'Y')
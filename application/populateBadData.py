import mysqlConnection as md
import pandas as pd
import populateModelData as model

def populateData(radius, actualValue):
    
    #select all zipcodes from table
    query = "select Zipcode FROM dddm.unfavorable_zipcodes order by Zipcode asc"
    data = pd.read_sql(query, md.connect())
    
    allzipList = data['Zipcode'].tolist()
    print(len(allzipList))
    
    #select inserted zipcodes
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
    
#populateData(50, 'N')
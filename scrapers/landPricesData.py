import mysqlConnection as md
import zipcodeDistance as zd

def getLandPricesData(zipcode, radius):
    engine = md.connect()
    
    zipdf = zd.getZipcodes(zipcode, radius)
    
    #parse dataframe zipdf to extract zipcodes
    zipList = zipdf['zip_code'].tolist()
    #print(zipList)
    
    #extract landprices from mysql by zipcodes from land_prices_final table
    query = "SELECT * from dddm.land_prices_final where zip in ("
    for zip in zipList:
        query += "'" + zip +  "',"
    
    query = query[:-1]
    query += ")"
    print(query)
    
    with engine.connect() as con:
        data = con.execute(query)
        
    landPriceSum = 0
    rowCount = 0
    for row in data:
        landPriceSum += row[6]
        rowCount += 1
     
    return landPriceSum/rowCount

print(getLandPricesData('14208', 10))
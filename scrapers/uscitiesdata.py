import pandas as pd
from sqlalchemy import create_engine

def connect():
    """ Connect to MySQL database after filling out below parameters"""
    engine = create_engine('mysql+pymysql://pythonUser:abc@localhost:3306/dddm?charset=utf8', encoding='utf-8')
    return engine
        
def create_table(dbEngine):
    df = pd.read_csv('resources/uscitiesdata.csv', sep=",", header=1,
                            names=["City","State ID","State Name","County Name","Zipcode","Latitude","Longitude","Population"])  
    df.to_sql(name='us_cities', con=dbEngine, if_exists = 'replace')
        
engine = connect()
create_table(engine)
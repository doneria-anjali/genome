import pandas as pd
from sqlalchemy import create_engine

def connect():
    """ Connect to MySQL database after filling out below parameters"""
    engine = create_engine('mysql+pymysql://pythonUser:abc@localhost:3306/dddm?charset=utf8', encoding='utf-8')
    return engine
        
def create_table(dbEngine):
    df = pd.read_csv('resources/UNdata_Export_20180314_030619219.txt', sep="|", header=None, 
                            names=["Year","Sex","City","Source Year","Value","Value Footnotes"])

    df = df.drop(['Value Footnotes','Source Year'], axis = 1)
    df.to_sql(name='census', con=dbEngine, if_exists = 'replace')
        
engine = connect()
create_table(engine)
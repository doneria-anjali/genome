import pandas as pd

df = pd.read_csv('/home/anjali/Desktop/genome/resources/uscitiesdata.csv', sep=",", header=None, 
                         names=["City","State ID","State Name","County Name","Zipcode","Latitude","Longitude","Population"])

print(len(df))
print(df.head(10))

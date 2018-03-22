import pandas as pd

def main():
   df = pd.read_csv('resources/uscitiesdata.csv', sep=",", header=None, 
                            names=["City","State ID","State Name","County Name","Zipcode","Latitude","Longitude","Population"])

   print(len(df))
   print(df.head(10))

main()
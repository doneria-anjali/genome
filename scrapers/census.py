import pandas as pd

df = pd.read_csv('/home/anjali/UNdata_Export_20180314_030619219.txt', sep="|", header=None, 
                         names=["Year","Sex","City","Source Year","Value","Value Footnotes"])

df_copy = df.drop(['Value Footnotes','Source Year'], axis = 1)

print(len(df_copy))
print(df_copy.head(10))

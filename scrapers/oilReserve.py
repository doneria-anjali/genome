import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "http://www.eia.gov/dnav/ng/ng_enr_sum_a_EPG0_R21_BCF_a.htm"

df_list = pd.read_html(url, attrs={'class': 'data1'}, keep_default_na=False)

print(df_list)


import pandas as pd
import mysqlConnection as md

def read_state_codes(file_name):
    state_code = pd.read_csv('resources/' + file_name, sep = '|')
    print(state_code.head(5))
    md.create_table(md.connect(), state_code, 'state_codes')
    

read_state_codes('statecodemapping.txt')
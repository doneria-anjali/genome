import pandas as pd
import mysqlConnection as md
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
        
def import_rules(file_name):
    data = open('resources/' + file_name).read()
    sent = sent_tokenize(data)
    #print(sent)
    
    #clean sentence and filter based on keywords
    keywords = ['well', 'wells', 'oil', 'drill', 'drilled']
    sentence_list = []
    for sentence in sent:
        sentence = sentence.replace("\n", "")
        for word in keywords:
            if word in sentence:
                sentence_list.append(sentence)
                break
           
        
    d = {'rule' : sentence_list}
    df = pd.DataFrame(data=d)
    df.to_sql('rules', md.connect(), schema='dddm')
        
        #intid = 3
        #query = "INSERT INTO rules(id, description, type) VALUES(" + intid + "," + sentence + ", secondary)"
    
    
    
    
    
import_rules('rules.txt') 

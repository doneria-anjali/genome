# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 17:19:52 2018

@author: Beth
"""

from nltk.tokenize import sent_tokenize
import pandas as pd
import mysqlConnection as md

data = open('resources/firedata.txt').read()
sent=sent_tokenize(data)
data2 = open('resources/firedata2.txt').read()
sent2=sent_tokenize(data2)
data3 = open('resources/hurricanedata.txt').read()
sent3=sent_tokenize(data3)
data4 = open('resources/hurricanedata2.txt').read()
sent4=sent_tokenize(data4)
data5 = open('resources/flooddata.txt').read()
sent5=sent_tokenize(data5)

state=['California','Sacramento']    

lines=[]
hurlines=[]
floodlines=[]
for line in sent:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent2:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent3:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent4:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent5:
    for word in state:
        if word in line:
            floodlines.append(line)
california = len(lines)
hurca = len(hurlines)
floodca = len(floodlines)

state=['Louisiana','New Orleans']    

lines=[]
hurlines=[]
floodlines=[]
for line in sent:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent2:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent3:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent4:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent5:
    for word in state:
        if word in line:
            floodlines.append(line)
louisiana = len(lines)
hurla = len(hurlines)
floodla = len(floodlines)

state=['New York','Albany']    
bad= 'New York Times'
bad2 = 'DATELINE: New York'
lines=[]
hurlines=[]
floodlines=[]
for line in sent:
    for word in state:
        if word in line:
            if bad not in line:
                if bad2 not in line:
                    lines.append(line)
for line in sent2:
    for word in state:
        if word in line:
            if bad not in line:
                if bad2 not in line:
                    lines.append(line)
for line in sent3:
    for word in state:
        if word in line:
            if bad not in line:
                if bad2 not in line:
                    hurlines.append(line)
for line in sent4:
    for word in state:
        if word in line:
            if bad not in line:
                if bad2 not in line:
                    hurlines.append(line)
for line in sent5:
    for word in state:
        if word in line:
            if bad not in line:
                if bad2 not in line:
                    floodlines.append(line)
newyork = len(lines)
hurny = len(hurlines)
floodny = len(floodlines)

state=['Alaska','Juneau']    

lines=[]
hurlines=[]
floodlines=[]
for line in sent:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent2:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent3:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent4:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent5:
    for word in state:
        if word in line:
            floodlines.append(line)
alaska = len(lines)
hurak = len(hurlines)
floodak = len(floodlines)

state=['Texas','Pasadena']    

lines=[]
hurlines=[]
floodlines=[]
for line in sent:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent2:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent3:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent4:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent5:
    for word in state:
        if word in line:
            floodlines.append(line)
texas = len(lines)
hurtx = len(hurlines)
floodtx = len(floodlines)

state=['North Carolina','Cary']    

lines=[]
hurlines=[]
floodlines=[]
for line in sent:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent2:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent3:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent4:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent5:
    for word in state:
        if word in line:
            floodlines.append(line)
northcarolina = len(lines)
hurnc = len(hurlines)
floodnc = len(floodlines)

state=['Ohio','Columbus']    

lines=[]
hurlines=[]
floodlines=[]
for line in sent:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent2:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent3:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent4:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent5:
    for word in state:
        if word in line:
            floodlines.append(line)
ohio = len(lines)
huroh = len(hurlines)
floodoh = len(floodlines)

state=['Massachusetts','Boston']    

lines=[]
hurlines=[]
floodlines=[]
for line in sent:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent2:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent3:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent4:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent5:
    for word in state:
        if word in line:
            floodlines.append(line)
massachusetts = len(lines)
hurma = len(hurlines)
floodma = len(floodlines)

state=['Utah','Salt Lake City']    

lines=[]
hurlines=[]
floodlines=[]
for line in sent:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent2:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent3:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent4:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent5:
    for word in state:
        if word in line:
            floodlines.append(line)
utah = len(lines)
hurut = len(hurlines)
floodut = len(floodlines)


state=['South Dakota','Pierre']    

lines=[]
hurlines=[]
floodlines=[]
for line in sent:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent2:
    for word in state:
        if word in line:
            lines.append(line)
for line in sent3:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent4:
    for word in state:
        if word in line:
            hurlines.append(line)
for line in sent5:
    for word in state:
        if word in line:
            floodlines.append(line)
southdakota = len(lines)
hursd = len(hurlines)
floodsd = len(floodlines)

states=['California','Louisiana','New York','Alaska','Texas','North Carolina', 'Ohio', 'Massachusetts', 'Utah', 'South Dakota']
firelengths=[california,louisiana,newyork,alaska,texas,northcarolina,ohio,massachusetts,utah,southdakota]
hurlengths=[hurca, hurla, hurny, hurak, hurtx, hurnc, huroh, hurma, hurut, hursd]
floodlengths=[floodca, floodla, floodny, floodak, floodtx, floodnc, floodoh, floodma, floodut, floodsd]
statecodes=['CA', 'LA', 'NY', 'AK', 'TX', 'NC', 'OH', 'MA', 'UT', 'SD']

df_disaster = pd.DataFrame(
    {'State': states,
     'StateCode': statecodes,
     'NumFireReferences': firelengths,
     'NumHurricaneReferences': hurlengths,
     'NumFloodReferences': floodlengths
    })

md.create_table(md.connect(), df_disaster, 'disaster_data')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 11:45:51 2021

@author: lorenzomanduca
"""

from pytimeextractor import ExtractionService, PySettingsBuilder
import pandas as pd
from datetime import date
import string    
import inquirer

settings = (PySettingsBuilder()
#.addRulesGroup('DateGroup')
.excludeRules("durationRule")
.excludeRules("repeatedRule")
.excludeRules("timeIntervalRule")
#.addUserDate("2017-10-23T18:40:40.931Z")
#.addTimeZoneOffset("2")
#.includeOnlyLatestDates(True)
.build()
)

"WHEN: Eliminazione caratteri speciali ed Estrazione delle date"
def WHEN(text):
    textElim=''.join(i for i in text if i in string.printable)    #Eliminazione caratteri speciali 
    
    result = ExtractionService.extract(textElim, settings);
    
    NoTime={'temporalExpression': 'No Time Identified', 'fromPosition': 0, 'toPosition': 0, 'classOfRuleType': 'No Time', 'temporal': [{'rule': 'holidaysRule', 'group': 'DateGroup', 'duration': None, 'durationInterval': None, 'set': None, 'type': 'DATE', 'startDate': {'time': {'hours': 0, 'minutes': 0, 'seconds': 0, 'timezoneName': None, 'timezoneOffset': 0}, 'date': {'year': 0000, 'month': 00, 'day': 00, 'dayOfWeek': None, 'weekOfMonth': None}, 'relative': True}, 'endDate': {'time': {'hours': 00, 'minutes': 0, 'seconds': 00, 'timezoneName': None, 'timezoneOffset': 0}, 'date': {'year': 0000, 'month': 00, 'day': 00, 'dayOfWeek': None, 'weekOfMonth': None}, 'relative': True}}], 'confidence': 0.99, 'locale': 'en_US', 'rule': {'rule': "((halloween)|(christmas eve)|(christmas day)|(christmas)|(new year's day)|(new year day)|(New Year s' Eve)|(New Year's Eve)|(new year)|(independence day)|(thanksgiving day)|(thanksgiving)|(Veterans Day)|(Columbus Day)|(Labor Day)|(Memorial Day)|(Washington's Birthday)|(Martin Luther King, Jr. Day)|(Martin Luther King Day)|(Inauguration Day)|((st[.]?|saint)[\\s]*(valentine|valentine's|valentines)[\\s]*(day)?))", 'priority': 1, 'confidence': 0.99, 'locale': 'en_US', 'type': 'DATE', 'id': 'fdc63959-88e4-4859-bbed-7ba071d90593', 'example': 'Christmas, New Year, Thanksgiving Day, Memorial Day, etc.', 'groupAndRule': {'rule': 'holidaysRule', 'group': 'DateGroup'}}}
    result.append(NoTime)
    
    
    df_date= pd.DataFrame(columns = ['TemporalExpression', 'day', 'month', 'year'])
    df_date.head()
    
    
    df_date1=pd.concat([pd.DataFrame([elem['temporalExpression']], columns=['TemporalExpression']) for elem in result], ignore_index=True)
    
    df_date2=pd.concat([pd.DataFrame([(((elem['temporal'][0])['endDate'])['date'])['day']], columns = ['day']) for elem in result], ignore_index=True)
    df_date3=pd.concat([pd.DataFrame([(((elem['temporal'][0])['endDate'])['date'])['month']], columns = ['month']) for elem in result], ignore_index=True)
    df_date4=pd.concat([pd.DataFrame([(((elem['temporal'][0])['endDate'])['date'])['year']], columns = ['year']) for elem in result], ignore_index=True)
    df_date=df_date1.join(df_date2['day'])
    df_date=df_date.join(df_date3['month'])
    df_date=df_date.join(df_date4['year'])
      
    
    
    "Creazione data completa ed inserimento No time identified"
    df_date["fullDate"] = df_date['day'].map(str) + '-' + df_date['month'].map(str) + '-' + df_date['year'].map(str)
    df_date.loc[df_date['TemporalExpression'] == 'No Time Identified', 'fullDate'] = 'No time identified'
    df_date=df_date.drop_duplicates(subset=['fullDate'], keep='first', inplace=False)


    "Scegliere un tempo per evitare disambiguazione"
    
    questions = [
      inquirer.List('tempo',
                    message="Which of these is the time of the events in the article?",
                    choices=df_date['fullDate'].tolist(),
                ),
    ]
    answers = inquirer.prompt(questions)

    
    giornoDataEstratta=int(df_date.loc[df_date['fullDate'] == answers["tempo"], 'day'])
    meseDataEstratta=int(df_date.loc[df_date['fullDate'] == answers["tempo"], 'month'])
    annoDataEstratta=int(df_date.loc[df_date['fullDate'] == answers["tempo"], 'year'])
    
    
    
    "Estrazione della data odierna"
    today = date.today()
    giorno=(today.day)
    mese=(today.month)
    anno=(today.year)


    "Calcolo differenza in giorni"
    d1 = date(anno, mese, giorno)
    
    
    if (annoDataEstratta == 0 and meseDataEstratta==0 and giornoDataEstratta == 0):
        days_diff=("Unknown date")
        score=0
    else:
       d0 = date(annoDataEstratta, meseDataEstratta, giornoDataEstratta)
       delta = d1 - d0
       days_diff=(delta.days)
       if days_diff < 180:
           score=1
       elif (days_diff < 730 and days_diff > 179):
           score=1.15
       else:
           score=1.35
    return(days_diff, score)
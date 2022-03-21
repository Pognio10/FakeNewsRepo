#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 13:59:03 2021

@author: lorenzomanduca
"""
import spacy
import pandas as pd
import geopy 
import math as Math
import inquirer
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim




"WHERE: Estrazione delle località"
def WHERE(text):
    locations = []
    
    nlp_wk = spacy.load('xx_ent_wiki_sm')
    doc = nlp_wk(text)
    locations.extend([[ent.text, ent.start, ent.end] for ent in doc.ents if ent.label_ in ['LOC']])
    locations.append(['No Location identified', 0, 0])
    
    "Creazione del dataframe ed inserimento delle coordinate"
    
    df = pd.DataFrame(locations, columns=['Location', 'start','end'])
    df.head()
    
    df2 = pd.DataFrame([['No Location identified', 0, 0, 0, 0, 0, 0 ,0]], columns=['Location', 'start','end','address','coordinates','latitude', 'longitude', 'altitude'])
    
    
    if len(locations) > 0:
        locator = geopy.geocoders.Nominatim(user_agent="mygeocoder")
        geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
        df["address"] = df["Location"].apply(geocode)
        df['coordinates'] = df['address'].apply(lambda loc: tuple(loc.point) if loc else None)
        df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['coordinates'].tolist(), index=df.index)
        df.latitude.isnull().sum()
        df = df[pd.notnull(df["latitude"])]
        df=df.drop_duplicates(subset=['Location'], keep='first', inplace=False)
        df=df.append(df2)
        
        "Scegliere una Località per evitare disambiguazione"
        
        questions = [
          inquirer.List('localita',
                        message="Which of the following is the location of the events in the article?",
                        choices=df['Location'].tolist(),
                    ),
        ]
        answers = inquirer.prompt(questions)
        
        print(answers)
        latitudineLocalita=float(df.loc[df['Location'] == answers["localita"], 'latitude'])
        longitudineLocalita=float(df.loc[df['Location'] == answers["localita"], 'longitude'])
        if (latitudineLocalita == 0 and longitudineLocalita == 0):
                        distance=("No Location identified")
                        score=0
        else:  
            
            geolocator = Nominatim(user_agent="mygeocoder")
            address=input("Please enter your location: ")
            local = [address]
            if address != '':
                location = geolocator.geocode(address)
                try:
                    latitudineIndirizzo=location.latitude
                    longitudineIndirizzo=location.longitude
                    if (latitudineIndirizzo != 0 and longitudineIndirizzo != 0):
                    
                            lat1=latitudineIndirizzo
                            lon1=-longitudineIndirizzo
                            lat2=latitudineLocalita
                            lon2=-longitudineLocalita
                            R = 6371 
                            dLat = (lat2-lat1)*(Math.pi/180)  
                            dLon = (lon2-lon1)*(Math.pi/180) 
                            a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(lat1*(Math.pi/180)) * Math.cos(lat2*(Math.pi/180)) * Math.sin(dLon/2) * Math.sin(dLon/2)
                            c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)) 
                            d = R * c 
                            distance=d
                            if distance < 1650:
                                score=1
                            elif(distance > 1649 and distance < 6000 ):
                                score=1.15
                            else:
                                score=1.35
                    else:
                        score = 1
                        distance=("No Location identified")
                except AttributeError:
                    score = 1
                    distance=("No Location identified")
                
            else: 
                score = 1
                distance=("No Location identified")

    else:
        score = 0
        distance=("No Location identified")
    return(distance, score)        
        

# -*- coding: utf-8 -*-

"WHO e preprocessing (Scraper di un URL per estrarre titolo, autore e testo)"

from goose3 import Goose
from bs4 import BeautifulSoup #Import stuff
import requests
import os
from pathlib import Path
import shutil
from newspaper import Article
import nltk


def WHO(url):
    g = Goose()
    article = g.extract(url=url)
    text=article.cleaned_text
    title=(article.title)
#    print(article.authors)

    articleN = Article(url)
    articleN.download() #Downloads the linkâ€™s HTML content
    articleN.parse() #Parse the article
    nltk.download('punkt')#1 time download of the sentence tokenizer
    articleN.nlp()#  Keyword extraction wrapper
    # print(articleN.nlp())
    # print(articleN.summary)
    # summary=articleN.summary
      
   
    
    
    r  = requests.get(url) #Download website source
    data = r.text  #Get the website source as text

    'Scaricamento immagini'

    soup = BeautifulSoup(data, 'html.parser') 
    links = []

    for link in soup.find_all('img'): 
        imgSrc = link.get('src')   
        links.append(imgSrc)    

    
    if not os.path.isdir("articleImage/"):
        os.mkdir("articleImage/")
    else:
        dir_path=Path("articleImage/")
        shutil.rmtree(dir_path)
        os.mkdir("articleImage/")
    
    countImage=1
    for el in links:
        if el.startswith("http") == True:
            response = requests.get(el)
            fi=open("articleImage/image"+str(countImage)+".jpg", "wb")
            fi.write(response.content)
            fi.close()
            countImage+=1
        else:
            continue
    
    #print(article.tweets)
    
    if (article.authors == []):
        auth=("Unrecognised author")
        score=0
    else:
        auth=("Author Found!", article.authors)
        score=1
        

    return(text, auth, score, title, links)




















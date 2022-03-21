from goose3 import Goose
from bs4 import BeautifulSoup #Import stuff
import requests
import os
from pathlib import Path
import shutil
from newspaper import Article
from langdetect import detect
from deep_translator import GoogleTranslator


'Scaricamento immagini'
def DOWN_IMAGES(data)
soup = BeautifulSoup(data, 'html.parser') #Setup a "soup" which BeautifulSoup can search
links = []

for link in soup.find_all('img'):  #Cycle through all 'img' tags
    imgSrc = link.get('src')   #Extract the 'src' from those tags
    links.append(imgSrc)    #Append the source to 'links'


if not os.path.isdir("articleImage/"):
    os.mkdir("articleImage/")
else:
    dir_path=Path("articleImage/")
    shutil.rmtree(dir_path)
    os.mkdir("articleImage/")

countImage=1
for el in links:
    if el.startswith("http") == True:
        # Save the captured image into the datasets folder
        response = requests.get(el)
        fi=open("articleImage/image"+str(countImage)+".jpg", "wb")
        fi.write(response.content)
        fi.close()
        countImage+=1
    else:
        continue
return(links)
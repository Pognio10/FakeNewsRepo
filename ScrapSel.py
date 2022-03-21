import os
from selenium import webdriver
import requests
import inquirer
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from os import listdir
from os.path import join, isfile


def ImageAnalize():

	scores=0
	path_1 = "articleImage/"
	if len(os.listdir(path_1)) != 0:
	
		onlyfiles = [i for i in listdir(path_1) if isfile(join(path_1, i))] 
		print(onlyfiles)
		contScore=0
		scorePar=0
		for elem in onlyfiles:

			filePath = path_1 + elem
			searchUrl = 'http://www.google.com/searchbyimage/upload'
			multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
			response = requests.post(searchUrl, files=multipart, allow_redirects=False)
			fetchUrl = response.headers['Location']
			



			options = Options()
			options.add_argument('--headless')
			options.add_argument('--disable-gpu')  # Last I checked this was necessary.
			driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

			#Specify Search URL 
			search_url=fetchUrl 
			driver.get(search_url.format())

			df = pd.DataFrame(columns = ['Link'])
			df2 = pd.DataFrame([['No Link identified']], columns=['Link'])



			ricResult=driver.find_elements_by_xpath("//a[contains(@class,'fKDtNb')]")
			totalricResults=len(ricResult)

			if totalricResults != 0:    
				for ei in ricResult:
					ser_correlated = ei.text
					questions = [inquirer.List('risposta', message="Is the topic of the article referring to? " + str(ser_correlated) + "?", choices=['Yes', 'No'],),]
					answers = inquirer.prompt(questions)
			   	

					if answers["risposta"] == "Yes":
						scorePar = scorePar + 1
						contScore = contScore + 1


					else:
						linResult=driver.find_elements_by_css_selector('div.g')
						if len(linResult) != 0:
							for els in linResult:
								link = els.find_element_by_tag_name("a")
								href = link.get_attribute("href")
								df = df.append({'Link': href}, ignore_index=True)
								df2 = df2.append(df)
								df2 = df2.drop_duplicates(subset=['Link'], keep='first', inplace=False)

								


							df2 = df2.drop(df2.index[len(linResult)])
							questions = [inquirer.List('linktit', message="Which of these is closest to the image?", choices=df2['Link'].tolist(),),]
							answers = inquirer.prompt(questions)
					   	

							if answers["linktit"] == "No Link identified":
								scorePar = scorePar + 0
								contScore = contScore +1

							else:
								scorePar = scorePar + 1
								contScore = contScore +1
								
						else:
							scorePar= scorePar + 0
							contScore= contScore + 1
			else:
				scorePar= scorePar + 0
				contScore= contScore + 1
	else:
		scores = 1

	if scores==0:
		score = scorePar/contScore
	else:
		score=scores
	print(score) 	
	return score   

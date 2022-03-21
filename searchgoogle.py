from googlesearch import search 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import inquirer

def searchG(textN):  
# to search 
	query = textN
	  
	j=search(query, num_results=5) 

	res_link={}
	link_tot=[]
	title_tot=[]
	for elem in j: 
		reqs = requests.get(elem) 
		# using the BeaitifulSoup module 
		soup = BeautifulSoup(reqs.text, 'html.parser') 
		# displaying the title 
		for title in soup.find_all('title'): 
		    titolo=(title.get_text())
		link_tot.append(elem)
		title_tot.append(titolo)

		res_link['Link'] = link_tot
		res_link['Title'] = title_tot
	#print(res_link)
	df2 = pd.DataFrame([['No Link identified', 'No Title Identified']], columns=['Link', 'Title'])

	df = pd.DataFrame.from_dict(res_link, orient='columns') 
	df = df.drop_duplicates(subset=['Link'], keep='first', inplace=False)
	df = df.append(df2)
	df["LinkTitle"] = df['Link'].map(str) + ' || ' + df['Title'].map(str) 



	"Scegliere un link per evitare disambiguazioe"

	questions = [inquirer.List('linktitle', 
		message="Which of these is closest to the news?", 
		choices=df['LinkTitle'].tolist(),),]
	answers=inquirer.prompt(questions)
	


	linkestratto=str(df.loc[df['LinkTitle'] == answers["linktitle"], 'Link'])


	if answers["linktitle"] == "No Link identified || No Title Identified": 
		score = 0
	else:
		score = 1

	#df = pd.DataFrame.from_dict(res_link)
	return df, score 
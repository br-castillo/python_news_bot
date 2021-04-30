from newsapi import NewsApiClient
import datetime as dt
import pandas as pd
import requests
import json
import time

def news_grabber():
	loop_on = True

	while loop_on == True:
		newsapi = NewsApiClient(api_key="f29f4293ed7f4289a5c53711d4408d5c")
		top_headlines = newsapi.get_top_headlines(sources= "bloomberg, business-insider, fortune, the-wall-street-journal")

		# list to save articles in 
		articles = top_headlines['articles']

		'''# iteration of articles through list to print them from
		for x, y in enumerate(articles):
	    	print(f"{x}     {y['title']}")'''

		# to get data from each article
		for x in range(0, 10):
			for key, value in articles[x].items():
				print(f"\n{key.ljust(15)} {value}")

		'''# converting data to dataframe with pandas
		df = pd.DataFrame(articles)
		print(df)'''

		# exporting to JSON
		with open('data.json', 'w') as json_file:
			json.dump(top_headlines, json_file)

		loop_on = False
		#time.sleep(900)

'''
FORMAT OF THE DICT

{'source': {'id': None, 'name': 'Esri.com'},
 'author': 'Orhun Aydin, Orhun Aydin',
 'title': 'R Notebooks in ArcGIS Pro for Spatial Data Science',
 'description': 'Some long desc',
 'url': 'https://www.castellphotos.com',
 'urlToImage': 'https://www.somesampleurl.org',
 'publishedAt': '2020-15-12T18:07:19Z',
 'content': 'Some other content...... [+540 chars]'} '''
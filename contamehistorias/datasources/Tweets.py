# -*- coding: utf-8 -*-
from .models import *
import requests
import time
import json
import re

class Tweets():
	DATETIME_FORMAT = '%yy-%m-%d' #'2017-12-01'

	def __init__(self):
		with open(r'C:\Users\iremg\Desktop\data_djokovic_2007_2012.json','r') as jsonFile: #C:\Users\iremg\Desktop\covid19_tweets.json
			self.tweets = json.load(jsonFile)
		self.max_documents = 2000

	def parse_news_article(self, item):

		#date = datetime.strptime(item["date"], '%Y-%m-%d %H:%M:%S') #covid tweets
		date = datetime.strptime(item["created_at"], '%Y-%m-%dT%H:%M:%S.000Z') #djokovic tweets

		text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",item['text']).split())


		result_item = ResultHeadLine(headline=text, datetime=date, domain=item["username"], url='twitter')
		return result_item

	def getResult(self, query, **kwargs):

		search_results = self.tweets

		num_pages = int(len(search_results)/ 100)
		print("num_pages",num_pages)
		page_size = 100

		#first page rows
		results = []

		#for i in range(len(search_results)):covid tweets
			#results.append(self.parse_news_article(search_results[str(i)]))
		for i in range(len(search_results)):
			for j in search_results[i].values():
				results.append(self.parse_news_article(j))

		#next pages if available
		for page in range(0, num_pages + 1)[:200]:

			#response = requests.get(search_url, headers=headers, params=params)
			if(page % 3 == 0):
				print("sleep")
				time.sleep(0.5)

			search_results = self.tweets

			#for i in range(len(search_results)):covid tweets
				#results.append(self.parse_news_article(search_results[str(i)]))
			for i in range(len(search_results)):
				for j in search_results[i].values():
					results.append(self.parse_news_article(j))

			if(len(results) > self.max_documents ):
				break

		return results

# -*- coding: utf-8 -*-
from .models import *
import requests
import time

class NewsSearchAPI(BaseDataSource):
	URL_REQUEST = 'https://newsapi.org/v2/everything'
	DATETIME_FORMAT = '%yy-%m-%d' #'2017-12-01'
	
	def __init__(self, params, processes=4):
		BaseDataSource.__init__(self, 'GoogleNewsSearchAPI')
		self.api_key = params["api_key"]

		self.dateFrom = params["from"].strftime(NewsSearchAPI.DATETIME_FORMAT)
		self.dateTo = params["to"].strftime(NewsSearchAPI.DATETIME_FORMAT)
		self.language = params["language"]
		self.processes = processes
		self.max_documents = 2000

	def parse_news_article(self, item):
		
		#pubdate = datetime.strptime(item["publishedAt"].replace(':[0-9]?[0-9]?Z',''), '%Y-%m-%dT%H:%M:%S')
		pubdate = datetime.strptime(item["publishedAt"].replace('Z',''), '%Y-%m-%dT%H:%M:%S')
		domain_name = item["source"]["name"]

		result_item = ResultHeadLine(headline=item['title'], datetime=pubdate, domain=domain_name, url=item['url'])
		return result_item

	def getResult(self, query, **kwargs):
		
		params  = {"q": query,
				   "language":self.language,
				   "from": self.dateFrom,
				   "to": self.dateTo,
				   "sortBy": 'relevancy',
				   "apiKey" : self.api_key}
		response = requests.get(NewsSearchAPI.URL_REQUEST, params=params)
		response.raise_for_status()
		search_results = response.json()

		base_search_query_url = search_results["status"]
		print(base_search_query_url)

		num_pages = int(search_results["totalResults"] / 100)
		print("num_pages",num_pages)
		page_size = 100

		#first page rows
		results = []		
		
		for article in search_results["articles"]:
			results.append(self.parse_news_article(article))

		#next pages if available
		for page in range(0, num_pages + 1)[:200]:
			offset = page * page_size
			params["offset"] = offset
		
			#response = requests.get(search_url, headers=headers, params=params)
			print (base_search_query_url,"offset:"+str(offset))
		
			if(page % 3 == 0):
				print("sleep")
				time.sleep(0.5)
		
			response = requests.get(NewsSearchAPI.URL_REQUEST, params=params)
			response.raise_for_status()
			search_results = response.json()

			for article in search_results["articles"]:
				results.append(self.parse_news_article(article))

			if(len(results) > self.max_documents ):
				break

		return results

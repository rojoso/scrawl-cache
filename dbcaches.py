import os 
import re
from urllib.parse import *
import zlib

from datetime import datetime,timedelta

import pickle
from pymongo import MongoClient

class DiskCache:
	def __init__(self,cache_dir = 'cache',max_length = 225,expires = timedelta(days = 30),client = None):
		self.cache_dir = cache_dir
		self.max_length = max_length

		self.expires = expires
		self.client = MongoClient('localhost',27017) if client is None else client
		self.db = self.client.mydb
		self.db.test_set.create_index('timestamp_4',expireAfterSeconds = expires.total_seconds())

	def url_to_path(self,url):

		components = urlsplit(url)

		path = components.path
		if not path:

			path = '/.index.html'

		elif path.endswith('/'):
			path += 'index.html'

		filename = components.netloc + path+components.query

		filename = re.sub(r'[^0-9a-zA-Z\-.,;_ ]','_',filename)

		filename = '_'.join(seg[:225] for seg in filename.split('/') ) 

		return filename

	def __getitem__(self,url):

		path = self.url_to_path(url)

		record = self.db.test_set.find_one({'_id':path})
		if record:
			return record['html']
		else:
			raise KeyError(url + 'dont exsits')

	def __setitem__(self,url,result):

		path = self.url_to_path(url)

		timestamp = datetime.utcnow()

		record = {'html':result,'timestamp':timestamp}

		self.db.test_set.update({'_id':path},{'$set':record},upsert = True)


	








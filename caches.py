import os 
import re
from urllib.parse import *
import zlib

from datetime import datetime,timedelta

import pickle

class DiskCache:
	def __init__(self,cache_dir = 'cache',max_length = 225,expires = timedelta(days = 30)):
		self.cache_dir = cache_dir
		self.max_length = max_length

		self.expires = expires

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

		if os.path.exists(path):
			with open(path,'rb') as rp:

				data = zlib.decompress(rp.read())

				result,timestamp = pickle.loads(data) 
				if self.has_expired(timestamp):
					raise KeyError('it has been expires')
					pass
				else:
					return	result
		else:
			raise KeyError(url + 'dont exsits')

	def __setitem__(self,url,result):

		path = self.url_to_path(url)

		timestamp = datetime.utcnow()
		data = pickle.dumps((result,timestamp))
		with open(path,'wb') as wp:

			wp.write(zlib.compress(data))

	def has_expired(self,timestamp):

		#返回是否已经过期的信息
		return datetime.utcnow() > timestamp+self.expires

















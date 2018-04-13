import os 
import re
from urllib.parse import *
import zlib

import pickle

class DiskCache:
	def __init__(self,cache_dir = 'cache',max_length = 225):
		self.cache_dir = cache_dir
		self.max_length = max_length

	def url_to_path(self,url):

		components = urlsplit(url)

		path = components.path
		if not path:

			path = '/.index.html'

		elif path.endswith('/'):
			path += 'index.html'

		filename = components.netloc + path+components.query

		filename = re.sub(r'[^0-9a-zA-Z\-.,;_ ]','_',filename)

		filename = '/'.join(seg[:225] for seg in filename.split('/') ) 

		return filename

	def __getitem__(self,url):

		path = self.url_to_path(url)

		if os.path.exists(path):
			with open(path,'rb') as rp:
				return pickle.loads(zlib.decompress(rp.read()))

		else:
			raise KeyError(url + 'dont exsits')

	def __setitem__(self,url,result):

		path = self.url_to_path(url)
		with open(path,'wb') as wp:

			wp.write(zlib.compress(pickle.dumps(result)))










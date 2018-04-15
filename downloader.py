from urllib import request
import urllib
from urllib import parse
import time
from datetime import datetime
import dbcaches

class Throttle:
	''' add a delay between downloads to smoe domain '''

	def __init__(self,delay):
		self.delay = delay

		self.domains = {}

	def wait(self,url):

		domain = parse.urlparse(url).netloc
		last_accessed = self.domains.get(domain)

		if self.delay>0 and last_accessed is not None:

			sleep_sec = self.delay - (datetime.now()-last_accessed).seconds

			if sleep_sec > 0 :
				time.sleep(sleep_sec)

		self.domains[domain] = datetime.now()

class Downloader:

	def __init__(self,headers = [('User_agent','Moll')],proxy = {},num_retries = 3,delay = 5,cache = None):
		
		self.headers = headers
		self.proxy = proxy
		self.num_retries = num_retries
		self.thethrottle = Throttle(delay)
		self.cache = cache

	def __call__(self,url):

		result = None
		if self.cache is None:

			result = self.download(url,self.headers,self.proxy,self.num_retries)

			self.cache[url] = result

		elif self.cache is not None:
			try:
				result = self.cache[url]
			except KeyError:
				print('there is no cache yet')
				result = self.download(url,self.headers,self.proxy,self.num_retries)
				self.cache[url] = result

		return result

	def download(self,url,headers,proxy,num_retries):
		print('downloading:',url)
		
		self.thethrottle.wait(url)
		opener = request.FancyURLopener(proxy)
		opener.addheaders = headers
		try:
			with opener.open(url) as f:
				html = f.read().decode()
		except urllib.error.URLError as e:
			print('downloading failes:',e.reason)
			html = None
			if num_retries > 0:
				if hasattr(e,'code') and 500 <= e.code <600:
					Download(url,headers,proxy,num_retries -1)

		return html



thedownload = Downloader(cache = dbcaches.DiskCache())

html = thedownload('http://www.sohu.com')

print(html)






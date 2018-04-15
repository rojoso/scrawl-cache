from urllib import request
import urllib
from urllib import parse
import time
from datetime import datetime

class Throttle:
	''' add a delay between downloads to smoe domain '''

	def __init__(self,delay):
		self.delay = delay

		self.domains = {}

	def wait(self,url):

		domain = parse.urlparse(url).netloc
		last_accessed = self.domains.get(domain)

		if self.delay>0 and last_accessed is not None:

			#说明最近这个url被访问过

			sleep_sec = self.delay - (datetime.now()-last_accessed).seconds

			if sleep_sec > 0 :
				time.sleep(sleep_sec)

		self.domains[domain] = datetime.now()

class Downloader:

	def __init__(self,url,headers = [('User_agent','Moll')],proxy = {},num_retries = 3,delay = 5,cache = None):
		self.url = url
		self.headers = headers
		self.proxy = proxy
		self.num_retries = num_retries
		self.thethrottle = Throttle(delay)
		self.cache = cache

	def __call__(self,url):

		result = None
		if self.cache is None:

			result = self.download(self.)





def Download(url,headers = ('User_agent','Moll'),proxy = {},num_retries = 10,delay = 5):

	print('downloading:',url)
	thethrottle = Throttle(delay)
	thethrottle.wait(url)

	opener = request.FancyURLopener(proxy)
	opener.addheaders = [headers]

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


#以下是程序正文

html = Download('https://baike.baidu.com/item/%E7%A9%BA%E4%B8%AD%E5%AE%A2%E8%BD%A6%E5%85%AC%E5%8F%B8')

print(html)






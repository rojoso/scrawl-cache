import caches

from datetime import datetime,timedelta

cache = caches.DiskCache(expires = timedelta(seconds = 5))
url = 'www.baidu.com/rit/err/ss/'

html = 'this  is a test wnbe'

cache[url] = html

url1 = 'http://www.souhu.com/hh/ss'

html1 = 'hfushhwhwhhhkkjkjkjkj'
cache[url1] = html1

ti = cache[url]

import time 

time.sleep(8)
t2 = cache[url]




import caches

cache = caches.DiskCache()
url = 'www.baidu.com/rit/err/ss/'

html = 'this  is a test wnbe'

cache[url] = html

url1 = 'http://www.souhu.com/hh/ss'

html1 = 'hfushhwhwhhhkkjkjkjkj'
cache[url1] = html1

ti = cache[url]

print(ti)

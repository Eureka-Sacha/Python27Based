# -*- coding: utf-8 -*-
from urllib2 import urlopen
from urllib2 import Request

__author__ = '奎'

old_url = 'http://rrurl.cn/b1UZuP'
req = Request(old_url)
response = urlopen(req)
print 'Old url :' + old_url
print 'Real url :' + response.geturl()
print('info')
print response.info()
# -*- coding: utf-8 -*-
import string
import re
import urllib2
__author__ = '奎'

def getImg(html):
    reg = r'data-src="(.+?\.gif)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    print(imglist)
    x=0
    for i in imglist:
        urllib2.urlretrieve(i,'%s.jpg' % x)
        f=open(i,'w+')
        f.write(i)
        f.close()
    print('存储结束')
    return list

old_url = 'http://www.fanjian.net'
req = urllib2.Request(old_url)
response = urllib2.urlopen(req)
# print 'Old url :' + old_url
# print 'Real url :' + response.geturl()
print('请求信息')
print response.info()
# print('网页信息')
# print response.read()
print('图片信息')
getImg(response.read())
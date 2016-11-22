# -*- coding: utf-8 -*-
# python 2.7.9
from sgmllib import SGMLParser

__author__ = '奎'

import re
import urllib2


class Html_Parse(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.tr = []
        self.td = []
        self.country = ''
        self.imgurl = ''
        self.flag = False
        self.getdata = False
        # self.temp = 0
        self.trflag = False

    def start_table(self, attrs):
        for k, v in attrs:
            if k == 'id' and v == 'ip_list':
                self.flag = True

    def start_tr(self, attrs):
        if self.flag:
            self.td = []
            self.trflag = True

    def start_td(self, attrs):
        if self.trflag:
            self.getdata = True

    def start_img(self, attrs):
        if self.getdata:
            for k, v in attrs:
                if k == 'alt':
                    self.country = v
                if k == 'src':
                    self.imgurl = v

    def end_td(self):
        if self.getdata:
            self.getdata = False

    def end_tr(self):
        if self.trflag:
            self.td.append(self.country)
            self.tr.append(self.td)
            self.trflag = False

    def end_table(self):
        if self.flag:
            self.flag = False

    def handle_data(self, text):
        if self.getdata and re.match(ur'\s', text, re.S) is None:
            self.td.append(re.sub(ur'\s', '', text, re.S))

    def print_text(self):
        for td in self.tr:
            print td


url = 'http://www.xicidaili.com/nn/'
headers = {  # header
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Accept-Language': 'zh-CN,zh;q=0.8',
             'Referer': 'http://www.xicidaili.com/nn/',
             }
req = urllib2.Request(url, headers=headers)
res = urllib2.urlopen(req)
page = res.read()
unicodePage = page.decode('UTF-8')

html_parse = Html_Parse()
html_parse.feed(unicodePage)
html_parse.print_text()
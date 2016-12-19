# -*- coding: utf-8 -*-
# python 2.7.9

from sgmllib import SGMLParser
from datetime import datetime
# import socket
import time
import random
from Demo import TestProxyIp
from Demo.RecordSet import RecordSet
from Demo.TableGrid_Parse import TableGridParse

__author__ = '奎'

import re
import urllib2


class Html_Parse(SGMLParser):
    """
    sgmlparser简单实现
    """

    def __init__(self):
        SGMLParser.__init__(self)  # 记成sgml构造函数
        self.tr = []  # 记录行数据
        self.td = []  # 记录列数据
        self.country = ''  # 记录国家
        self.imgurl = ''  # 记录图片url
        self.flag = False  # table Flag
        self.getdata = False  # td flag
        # self.temp = 0
        self.trflag = False  # tr flag

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
        if self.trflag and self.td:
            self.td.append(self.country)
            self.tr.append(self.td)
            self.trflag = False

    def end_table(self):
        if self.flag:
            self.flag = False

    def handle_data(self, text):
        temp = re.sub(ur'\s', '', text, re.S)
        if self.getdata and temp != '' and temp is not None:
            self.td.append(re.sub(ur'\s', '', text, re.S).encode('utf-8'))

    def print_text(self):
        for td in self.tr:
            print td

    def get_values(self):
        return self.tr


class ProxyIPSpider():
    """
    代理IP爬取
    """

    def __init__(self):
        """构造函数,初始化参数"""
        self._version = '代理IP爬虫v1.1'
        self._url = 'http://www.xicidaili.com/nn/'
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'http://www.xicidaili.com/nn/',
        }
        self._nowpage = 1  # 当前页数
        self._startpage = 1  # 开始页数
        self._maxpage = 101  # 最大查询页数
        self._erro = []  # 错误信息
        self._array = []  # 爬取到的数据
        self._count = 0  # 已保存的条数
        self.__getproxypool()

    def __getproxypool(self):
        """
        从数据库获取代理IP 放到list中充当代理池
        """
        self._proxypool = []
        rs = RecordSet()
        rs.execute_sql('select * from proxyip where flag=1 and type="HTTP"')
        while rs.next():
            proxyip = TestProxyIp.proxyIp(id=rs.getvalue('id'), ip=rs.getvalue('ip') + ':' + str(rs.getvalue('prot')))
            self._proxypool.append(proxyip)


    def __destroyproxy(self, proxyip):
        """
        从数据库和本地代理池删除失效的代理IP
        """
        if not TestProxyIp.proxyIp.test_http_proxyip(proxyip, testurl='http://www.xicidaili.com/'):
            self._proxypool.remove(proxyip)
            return True
        return False

    def __get_page_old(self):
        """
        v0.1  单线程无代理爬取
        """
        while self._nowpage < self._maxpage:
            # urllib2.install_opener(opener)# 将opener实例设置为全局
            req = urllib2.Request(self._url, headers=self._headers)
            res = urllib2.urlopen(req)
            page = res.read()
            unicodePage = page.decode('UTF-8')
            html_parse = Html_Parse()
            html_parse.feed(unicodePage)
            self._array = html_parse.get_values()
            # html_parse.print_text()
            self.__data_save_old()
            self._nowpage += 1
            self._url = self._headers['Referer'] + str(self._nowpage)
            time.sleep(random.random() * 3)  # 随机延迟 防止被T
        print '共爬取并导入成功代理IP%d条' % self._count

    def __get_page(self):
        """
        v1.0    单线程代理爬取
        """
        while self._nowpage < self._maxpage:
            flag = True
            while flag and len(self._proxypool) > 0:
                proxyip = random.choice(self._proxypool)  # 随机取一个代理IP
                proxy = urllib2.ProxyHandler({'http': proxyip})  # 代理handler
                opener = urllib2.build_opener(proxy)  # 使用proxy处理创建opener实例

                def parser_headers():
                    templist = []
                    for k, v in self._headers.items():
                        templist.append((k, v))
                    return templist

                # print parserheaders()
                opener.addheaders = parser_headers()  # 为opener实例添加header
                # urllib2.install_opener(opener)# 将opener实例设置为全局
                # req = urllib2.Request(self._url, headers=self._headers)
                try:
                    res = opener.open(self._url, timeout=1)  # 使用opener的open方法代替urlopen()
                    # res = urllib2.urlopen(req)
                    page = res.read()
                except:
                    # 如果读取超时或者失败,则重新开始循环
                    self.__destroyproxy(proxyip)
                    continue
                unicodePage = page.decode('UTF-8')
                html_parse = Html_Parse()
                html_parse.feed(unicodePage)
                self._array = html_parse.get_values()
                # html_parse.print_text()
                self.__data_save_old()
                flag = False  # 不出任何意外就退出循环.
            self._nowpage += 1
            self._url = self._headers['Referer'] + str(self._nowpage)
            time.sleep(random.random() * 3)  # 随机延迟 防止被T
        print '共爬取并导入成功代理IP%d条' % self._count

    def __get_page2(self):
        """
        v1.1    使用新的sgml实现类分析html
        """
        while self._nowpage < self._maxpage:
            flag = True
            while flag and len(self._proxypool) > 0:
                proxyip = random.choice(self._proxypool)  # 随机取一个代理IP
                proxy = urllib2.ProxyHandler({'http': proxyip})  # 代理handler
                opener = urllib2.build_opener(proxy)  # 使用proxy处理创建opener实例

                def parser_headers():
                    templist = []
                    for k, v in self._headers.items():
                        templist.append((k, v))
                    return templist

                opener.addheaders = parser_headers()  # 为opener实例添加header
                try:
                    res = opener.open(self._url, timeout=1)  # 使用opener的open方法代替urlopen()
                    page = res.read()
                except Exception, e:
                    # 如果读取超时或者失败,则重新开始循环
                    print e
                    self.__destroyproxy(proxyip)
                    continue
                unicodePage = page.decode('UTF-8')
                Html_Parse = TableGridParse()
                Html_Parse.feed(unicodePage)
                array = Html_Parse.get_array()
                # html_parse.print_text()
                self.__data_save(array)
                flag = False  # 不出任何意外就退出循环.
            self._nowpage += 1
            self._url = self._headers['Referer'] + str(self._nowpage)
            time.sleep(random.random() * 3)  # 随机延迟 防止被T
        print '共爬取并导入成功代理IP%d条' % self._count

    def __data_save_old(self):
        """
        v0.1 v1.0 使用的数据更新新增方法
        v1.1 之后使用新的__data_save(array)
        """
        rs = RecordSet()
        _insert = []
        _update = []
        update = ur'update proxyIP set ip=%s,prot=%s,incognito=%s,type=%s,address=%s,verificationtime=%s,flag=%s,others=%s where id =%s'
        insert = ur'insert into proxyIP(ip,prot,incognito,type,address,verificationtime,flag,others)  values(%s,%s,%s,%s,%s,%s,%s,%s)'
        for td in self._array:
            # print td
            if not td[3] == '高匿':
                print td
                continue
            select_sql = ur'select id from proxyip where ip =%s and prot=%s'
            if rs.execute_sql(select_sql, (td[0], td[1])) and int(rs.getvalue('id')) > 0:
                _update.append(
                    (td[0], td[1], td[3], td[4], td[2], datetime.now(), '3',
                     '',
                     rs.getvalue('id')))
            else:
                _insert.append(
                    (td[0], td[1], td[3], td[4], td[2], datetime.now(), '2',
                     ''))

        for i in _insert:
            # print i
            if not rs.execute_sql(insert, param=i):
                self._erro.append(i)
            else:
                print 'IP:', str(i[0]), ':', str(i[1]), '  已添加'
                self._count += 1
                # for u in _update:
                # if not rs.execute_sql(update, param=u):
                # self._erro.append(u)
                # else:
                # print "IP:%s  已更新" % str(u[0])
                # self._count += 1

    def __data_save(self, array):
        """
        v1.1 以后使用此方法新增与更新数据
        """
        rs = RecordSet()
        _insert = []
        _update = []
        update = ur'update proxyIP set ip=%s,prot=%s,incognito=%s,type=%s,address=%s,verificationtime=%s,flag=%s,others=%s where id =%s'
        insert = ur'insert into proxyIP(ip,prot,incognito,type,address,verificationtime,flag,others)  values(%s,%s,%s,%s,%s,%s,%s,%s)'
        for rows1, rows2 in array:
            select_sql = ur'select id from proxyip where ip =%s and prot=%s'
            if rs.execute_sql(select_sql, (rows1[1]['values'], rows1[2]['values'])) and int(rs.getvalue('id')) > 0:
                address = rows2[6][0]['values']
                if address or address == '':
                    address = rows1[6]['values']
                temp_value = (rows1[1]['values'], rows1[2]['values'], rows1[4]['values'], rows1[5]['values'],
                              address, datetime.now(), '3', self._url)
                _update.append(temp_value)
            else:
                address = rows2[6][0]['values']
                if address or address == '':
                    address = rows1[6]['values']
                temp_value = (rows1[1]['values'], rows1[2]['values'], rows1[4]['values'], rows1[5]['values'],
                              address, datetime.now(), '2', self._url)
                _insert.append(temp_value)
        for i in _insert:
            # print i
            if not rs.execute_sql(insert, param=i):
                self._erro.append(i)
            else:
                print 'IP:', str(i[0]), ':', str(i[1]), '  已添加'
                self._count += 1
                # 更新操作暂时封印
                # for u in _update:
                # if not rs.execute_sql(update, param=u):
                # self._erro.append(u)
                # else:
                # print "IP:%s  已更新" % str(u[0])
                # self._count += 1

    def start_model(self):
        """
        爬虫入口
        """
        print '------%s启动------' % self._version
        if self._proxypool:
            self.__get_page2()
        else:
            print '------代理池为空,开始调用旧版方法------'
            self.__get_page_old()
        print '------%s完成------' % self._version


def test_proxy_ip():
    rs = RecordSet()
    rs.execute_sql('select * from proxyip where flag in (2,3) and type="HTTP"')
    while rs.next():
        proxy = urllib2.ProxyHandler({'http': rs.getvalue('ip') + ':' + str(rs.getvalue('prot'))})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        try:
            response = urllib2.urlopen('http://httpbin.org/ip', timeout=1)
            print response.read()
        except:
            print 'IP:', rs.getvalue('ip') + ':' + str(rs.getvalue('prot')), '已失效'
            rs2 = RecordSet()
            t = (datetime.now(), '0', rs.getvalue('id'))
            rs2.execute_sql(ur'update proxyIP set verificationtime=%s,flag=%s where id =%s', t)


def parserheaders(header):
    templist = []
    for key, value in headers.items():
        templist.append((key, value))
    return templist


if __name__ == '__main__':
    test_proxy_ip()
    # proxyIPS = ProxyIPSpider()
    # proxyIPS.start_model()
    # url = 'http://www.xicidaili.com/nn/'
    # headers = {  # header
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Language': 'zh-CN,zh;q=0.8',
    # 'Referer': 'http://www.xicidaili.com/nn/',
    # }
    # req = urllib2.Request(url, headers=headers)
    # res = urllib2.urlopen(req)
    # page = res.read()
    # unicodePage = page.decode('UTF-8')
    #
    # html_parse = Html_Parse()
    # html_parse.feed(unicodePage)
    # html_parse.print_text()
    # print '中文'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Referer': 'http://www.xicidaili.com/nn/',
    }
    # for k, v in headers:
    # t = (k, v)
    # print t
    # print parserheaders(headers)
    # x = random.choice(headers.items())
    # print x
    # s = [TestProxyIp.proxyIp(), TestProxyIp.proxyIp]
    # proxyip = TestProxyIp.proxyIp()
    # s.append(proxyip)
    # print s
    # s.remove(proxyip)
    # print s
    # s1=random.choice(s)
    # print s1
    # proxy = urllib2.ProxyHandler({'http': '113.14.43.254:8998'})
    # opener = urllib2.build_opener(proxy)
    # res = opener.open('https://www.zhihu.com/')
    # print res.code
    # print res.read()



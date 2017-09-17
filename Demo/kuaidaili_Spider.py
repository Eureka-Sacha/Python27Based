# -*- coding: utf-8 -*-
import StringIO
import gzip
import random
import urllib2
import time
from datetime import datetime
from Demo import TestProxyIp
from Demo.RecordSet import RecordSet
from Demo.TableGrid_Parse import TableGridParse

__author__ = '奎'


class KuaiDaiLi():
    def __init__(self):
        """构造函数,初始化参数"""
        self._version = '代理IP爬虫v1.1'
        self._url = 'http://www.kuaidaili.com/free/inha/1/'
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Referer': 'http://www.kuaidaili.com/free/inha/1/',
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
            proxyip = TestProxyIp.ProxyIp(id=rs.getvalue('id'), ip=rs.getvalue('ip') + ':' + str(rs.getvalue('prot')))
            self._proxypool.append(proxyip)


    def __destroyproxy(self, proxyip):
        """
        从数据库和本地代理池删除失效的代理IP
        """
        if not TestProxyIp.ProxyIp.test_http_proxyip(proxyip, testurl='http://www.kuaidaili.com/free/inha/1/'):
            self._proxypool.remove(proxyip)
            return True
        return False

    def __gzdecode(self, data):
        compressedstream = StringIO.StringIO(data)
        gziper = gzip.GzipFile(fileobj=compressedstream)
        data2 = gziper.read()  # 读取解压缩后数据
        return data2

    def __get_page_old(self):
        """
        v0.1  单线程无代理爬取
        """
        while self._nowpage < self._maxpage:
            # urllib2.install_opener(opener)# 将opener实例设置为全局
            req = urllib2.Request(self._url, headers=self._headers)
            res = urllib2.urlopen(req)
            ecnoding = res.headers.get('Accept-Encoding')
            if ecnoding and str(ecnoding).index('gzip') > -1:
                page = self.__gzdecode(res.read())
            else:
                page = res.read()
            unicodePage = page.decode('utf-8')
            html_parse = TableGridParse(table_attr={'class': 'table table-bordered table-striped'})
            html_parse.feed(unicodePage)
            self._array = html_parse.get_array()
            # html_parse.print_text()
            self.__data_save(self._array)
            self._nowpage += 1
            self._url = self._headers['Referer'] + str(self._nowpage)
            time.sleep(random.random() * 10)  # 随机延迟 防止被T
        print '共爬取并导入成功代理IP%d条' % self._count

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
            if rs.execute_sql(select_sql, (rows1[0]['values'], rows1[1]['values'])) and int(rs.getvalue('id')) > 0:
                address = rows1[4]['values']
                temp_value = (rows1[0]['values'], rows1[1]['values'], rows1[2]['values'], rows1[3]['values'],
                              address, datetime.now(), '3', self._url)
                _update.append(temp_value)
            else:
                address = rows1[4]['values']
                temp_value = (rows1[0]['values'], rows1[1]['values'], rows1[2]['values'], rows1[3]['values'],
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
        self.__get_page_old()
        print '------%s完成------' % self._version


if __name__ == '__main__':
    k = KuaiDaiLi()
    k.start_model()
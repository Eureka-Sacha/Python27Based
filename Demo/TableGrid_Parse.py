# -*- coding: utf-8 -*-
# python 2.7.9
from sgmllib import SGMLParser
import re
import urllib2
import time
from Demo.RecordSet import RecordSet

__author__ = '奎'


class TableGridParse(SGMLParser):
    def __init__(self, table_attr, tr_attr=None, td_attr=None, limit=None):
        SGMLParser.__init__(self)
        self._table_attr = table_attr  # table定位参数 id name class 之类的
        self._tr_attr = tr_attr  # tr定位参数 id name class 之类的
        self._td_attr = td_attr  # td定位参数 id name class 之类的
        self._array = []  # 用以存储td属性,值与unknown属性,值
        self._rows = []  # 用以存储td属性,值
        self._cols = []  # 临时存储每列数据
        self._unknown_d = []
        self._unknown = []  # 用以存储unknown属性,值
        self._temp_unknown = {}  # 临时存储unknown
        self._temp_td = {}  # 临时存储td
        self._unclose_tag = ['img', 'br', 'wbr', '']

        self._limit = limit  # 暂时无用  后期想用作行数截取
        self._t_flag = False  # table开关
        self._tr_flag = False  # tr开关
        self._td_flag = False  # td开关
        self._unknown_flag = False  # unknown开关

    def set_table_attrs(self, **attrs):
        """
        设置table的参数
        """
        for t_k in self._table_attr.keys():
            for v in attrs.values():
                if v and v != '':
                    self._table_attr[t_k] = v

    def set_tr_attrs(self, **attrs):
        """
        设置tr的参数
        """
        for t_k in self._tr_attr.keys():
            for v in attrs.values():
                if v and v != '':
                    self._tr_attr[t_k] = v

    def set_td_attrs(self, **attrs):
        """
        设置td的参数
        """
        for t_k in self._td_attr.keys():
            for v in attrs.values():
                if v and v != '':
                    self._td_attr[t_k] = v

    def start_table(self, attrs):
        """
        如果参数符合要求则开启table
        """
        self._t_flag = TableGridParse.__isEmpty(**self._table_attr)
        if self._t_flag:
            for k, v in self._table_attr.items():
                if v and v != '':
                    if TableGridParse.__getByName(attrs, name=k) != v:
                        self._t_flag = False

    def start_tr(self, attrs):
        """
        如果参数符合要求则开始tr
        """
        if self._t_flag:
            if self._tr_attr and TableGridParse.__isEmpty(**self._tr_attr):
                for k, v in self._tr_attr.items():
                    if v and v != '':
                        if TableGridParse.__getByName(attrs, name=k) != v:
                            self._tr_flag = False
            else:
                self._tr_flag = True
        if self._tr_flag:
            self._cols = []  # 每开启一行就将上一行的数据制空

    def start_td(self, attrs):
        if self._tr_flag:
            if self._td_attr and TableGridParse.__isEmpty(**self._td_attr):
                for k, v in self._tr_attr.items():
                    if v and v != '':
                        if TableGridParse.__getByName(attrs, name=k) != v:
                            self._td_flag = False
            else:
                self._td_flag = True
            if self._td_flag:
                self._temp_td['attrs'] = attrs
                self._temp_td['values'] = ''

    def unknown_starttag(self, tag, attrs):
        if self._td_flag:
            self._unknown_flag = True
            self._temp_unknown['tag'] = tag
            self._temp_unknown['attrs'] = attrs
            self._temp_unknown['values'] = ''
            if tag in self._unclose_tag:
                self._unknown_flag = False
                self._unknown.append(self._temp_unknown)
                self._temp_unknown = {}

    def unknown_endtag(self, tag):
        if self._unknown_flag:
            self._unknown_flag = False
            self._unknown.append(self._temp_unknown)
            self._temp_unknown = {}

    def end_td(self):
        if self._td_flag:
            self._td_flag = False
            self._cols.append(self._temp_td)
            self._temp_td = {}
            self._unknown_d.append(self._unknown)
            self._unknown = []

    def end_tr(self):
        if self._tr_flag and self._cols:
            self._rows.append(self._cols)
            self._array.append((self._cols, self._unknown_d))
            self._unknown_d = []
            self._tr_flag = False

    def end_table(self):
        if self._td_flag:
            self._td_flag = False

    def handle_data(self, text):
        if self._td_flag:
            if self._unknown_flag:
                self._temp_unknown['values'] = re.sub(ur'\s', '', text, re.M)
                self._temp_td['values'] = ''
            else:
                self._temp_td['values'] = re.sub(ur'\s', '', text, re.M)
                self._temp_unknown['values'] = ''

    def print_text(self):
        """
        测试用
        """
        for cols in self._rows:
            print cols

    def get_values(self):
        """
        返回数据
        """
        return self._rows

    def get_unknown_values(self):
        """
        返回其他数据
        """
        return self._unknown

    def get_array(self):
        """
        返回所有数据
        """
        return self._array

    @staticmethod
    def __isEmpty(**d):
        """
        判断dict中的value是否为空
        """
        if d:
            for i in d.values():
                if i and i != '':
                    return True
        return False

    @staticmethod
    def __getByName(lt, name=None):
        """
        从一个list(tuple(k,v))中获取到k的值
        """
        if lt:
            for k, v in lt:
                if k == name:
                    return v
        return None


if __name__ == '__main__':
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    # }
    # t_parse = TableGridParse(table_attr={'id': 'ip_list'})
    # req = urllib2.Request('http://www.xicidaili.com/nn/', headers=headers)
    # res = urllib2.urlopen(req)
    # print res.headers
    # page = res.read()
    # # print page
    # unicodePage = page.decode('Utf-8')
    #
    # t_parse.feed(unicodePage)
    # start = time.time()
    # array = t_parse.get_array()
    # values = t_parse.get_values()
    # end = time.time()
    # print end - start, 's'
    #
    # for a1, a2 in array:
    #     print a1
    #     print a2
    #     for i in range(len(a1)):
    #         print a1[i]
    #         print a2[i]

    rs = RecordSet()
    rs.execute_sql(ur'select id from proxyip where ip =%s and prot=%s', ('121.204.165.187', '8118'))
    print rs.getvalue('id')
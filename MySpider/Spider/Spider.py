# -*- coding: utf-8 -*-
import random
import requests
import time
import MySpider.Util as Util
import BeautifulSoup

__author__ = '奎'
"""
一个简单的单线爬虫模块
"""
import logging


class ContentFetch(object):
    """
    内容获取的接口类,集成后重新实现fetch方法
    """

    def __init__(self, timeout=3, sleep_time=3):
        """

        """
        self._timeout = timeout
        self._sleep_time = sleep_time

    def do(self, url):
        logging.debug('%s start: url=%s', self.__class__.__name__, url)
        time.sleep(random.randint(0, self.sleep_time))
        try:
            content = self.fetch(url)
        except Exception, e:
            logging.error('%s error: %s url=%s', self.__class__.__name__, e, url)
        logging.debug('%s end: url=%s', self.__class__.__name__, url)
        return content

    def fetch(self, url):
        """
        具体怎么实现请自己看情况来
        """
        headers = {"User-Agent": Util.make_random_useragent(), "Accept-Encoding": "gzip"}
        # logging.debug('%s url:%s', self.__class__.__name__, url)
        response = requests.get(url, headers=headers, cookies=None, timeout=self._timeout)
        return response.status_code, response.url, response.text


class ContentParse(object):
    """
    内容解析的接口类, 继承后重新实现parse方法
    """

    def __init__(self):
        pass

    def do(self, content):
        logging.debug('%s startParse', self.__class__.__name__)
        pass

    def parse(self, content):
        pass


class Saver(object):
    """
    信息存储的接口类,自定义时请重新实现save方法
    """

    def __init__(self):
        pass

    def do(self):
        pass

    def save(self):
        pass

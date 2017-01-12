# -*- coding: utf-8 -*-
import random
import time
import requests

__author__ = '奎'
import logging


class Fetch(object):
    def __init__(self, url, max_repeat=3, encoding='utf-8', timeout=3, sleep_time=3):
        self._url = url  # define  url
        self._max_repeat = max_repeat  # max repeat times;default :3
        # self._encoding = encoding  # page encoding; default utf-8
        self._timeout = timeout  # time out; default: 3
        self._sleep_time = sleep_time  # sleep time after fetching. default:3

    def do(self, url, keys, repeat):
        """

        """
        logging.debug("%s start: keys=%s, repeat=%s, url=%s", self.__class__.__name__, keys, repeat, url)
        time.sleep(random.randint(0, self._sleep_time))
        try:
            fetch_result, content = self.url_fetch(url, keys, repeat)
        except Exception, e:
            if repeat >= self._max_repeat:
                fetch_result, content = -1, None
                logging.error("%s error: %s, keys=%s, repeat=%s, url=%s", self.__class__.__name__, e, keys, repeat,
                              url)
            else:
                fetch_result, content = 0, None
                logging.debug("%s repeat: %s, keys=%s, repeat=%s, url=%s", self.__class__.__name__, e, keys, repeat,
                              url)

        logging.debug("%s end: fetch_result=%s, url=%s", self.__class__.__name__, fetch_result, url)
        return fetch_result, content

    def url_fetch(self, url, keys, repeat):
        """

        """
        headers = {}
        response = requests.get(url, params=None, data=None, headers=headers, cookies=None, timeout=(3.05, 10))
        if response.history:
            logging.debug("%s redirect: keys=%s, repeat=%s, url=%s", self.__class__.__name__, keys, repeat, url)
        content = (response.status_code, response.url, response.text)
        return 1, content

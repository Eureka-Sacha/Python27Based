# -*- coding: utf-8 -*-
import logging
import re

__author__ = '奎'


class Parse(object):
    def __init__(self, max_deep=0):
        self._max_deep = max_deep  # default: 0, if -1, spider will not stop until all urls are fetched

    def do(self, priority, url, keys, deep, content):
        logging.debug("%s start: priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, priority, keys, deep,
                      url)

        try:
            parse_result, url_list, save_list = self.htm_parse(priority, url, keys, deep, content)
        except Exception, e:
            parse_result, url_list, save_list = -1, [], []
            logging.error("%s error: %s, priority=%s, keys=%s, deep=%s, url=%s", self.__class__.__name__, e,
                          priority, keys, deep, url)

        logging.debug("%s end: parse_result=%s, len(url_list)=%s, len(save_list)=%s, url=%s", self.__class__.__name__,
                      parse_result, len(url_list), len(save_list), url)
        return parse_result, url_list, save_list

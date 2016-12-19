# -*- coding: utf-8 -*-
# python 2.7.9
__author__ = '奎'


class SpiderError(IOError):
    """
    错误信息
    """

    def __init__(self, reason):
        self.args = reason
        self.reason = reason

    def __str__(self):
        return '#SpiderError%s#' % self.reason


class SpiderBasis():
    def __init__(self):
        pass
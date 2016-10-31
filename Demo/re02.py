# -*- coding: utf-8 -*-
import re

__author__ = '奎'

reg_str = r'(\s{1}f+\w*\s{1})'  # 正则表达式字符串

pattern = re.compile(reg_str)  # 正则解析对象

something = ''' Shall I compare thee to a summer's day?
Thou art more lovely and more temperate:
Rough winds do shake the darling buds of May,
And summer's lease hath all too short a date:
Sometime too hot the eye of heaven shines,
And often is his gold complexion dimm'd;
And every fair from fair sometime declines,
By chance or nature's changing course untrimm'd;
But thy eternal summer shall not fade
Nor lose possession of that fair thou owest;
Nor shall Death brag thou wander'st in his shade,
When in eternal lines to time thou growest:
So long as men can breathe or eyes can see,
So long lives this and this gives life to thee.'''  # 被解析的字符串对象

math = pattern.findall(something)  # 开始解析并返回对象
for word in math:
    print(word.replace(u'\n', ''))

print '总共查到单词:', math.__len__(), '个'
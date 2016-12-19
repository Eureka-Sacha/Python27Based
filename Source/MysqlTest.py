# -*- coding: utf-8 -*-
import ConfigParser
from Demo.RecordSet import RecordSet

__author__ = '奎'
import MySQLdb


# conf = ConfigParser.ConfigParser()
# conf.readfp(open('../conf/conf.conf', 'r+'))
#
# option = conf.options('db')
# # print option
# options = []
# for o in option:
#     something = conf.get('db', o)
#     options.append(something)
#
# # print options
#
# db = MySQLdb.Connect(options[1], options[3], options[4], options[5])
# cursor = db.cursor()
# t = (("1.1.1.1", "233", "0", "0", "address", "2016-01-01", "0", ""),
#      ("1.1.1.1", "233", "0", "0", "address", "2016-01-01", "0", ""))
# sql = 'select * from proxyIP'
# sql2 = 'insert into proxyIP(ip,prot,incognito,type,address,verificationtime,flag,others) values(%s,%s,%s,%s,%s,%s,%s,%s)'
# print cursor.execute(sql)
# print cursor.description_flags
# if cursor._result:
#     print cursor.fetchall()
# else:
#     print 'false'
# # print cursor._do_get_result()
#
# db.rollback()
# cursor.close()
# db.close()
#
# if not None:
#     print '2'

if __name__ == '__main__':
    rs = RecordSet()
    sql = 'select * from proxyIP'
    rs.execute_sql(sql)
    while rs.next():
        print rs.getvalue('ip')

# -*- coding: utf-8 -*-
import ConfigParser

__author__ = '奎'
import MySQLdb


class DB_Pool:
    def __init__(self):
        conf=ConfigParser.ConfigParser()


conf = ConfigParser.ConfigParser()
conf.readfp(open('../conf/conf.conf', 'r+'))

option = conf.options('db')
options = []
for o in option:
    something = conf.get('db', o)
    options.append(something)

db = MySQLdb.Connect(options[0], options[2], options[3], options[4])
cursor = db.cursor()
sql = u'select * from proxyIP '
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print row[0]
        print row[1]
except Exception, e:
    print e
db.close()

print MySQLdb.threadsafety

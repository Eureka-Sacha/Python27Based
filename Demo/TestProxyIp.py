# -*- coding: utf-8 -*-
import urllib2
from datetime import datetime
import time
from Demo.RecordSet import RecordSet

__author__ = '奎'


class proxyIp():
    """
    """

    def time(self):
        tim = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return tim

    def __init__(self, id='-1', ip='0.0.0.0'):
        self.id = id
        self.ip = ip

    def test_proxy_ip(self):
        rs = RecordSet()
        rs.execute_sql('select * from proxyip where flag in (2,3) and type="HTTP"')
        while rs.next():
            proxy = urllib2.ProxyHandler({'http': rs.getvalue('ip') + ':' + str(rs.getvalue('prot'))})
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)
            try:
                start = time.time()
                response = urllib2.urlopen('http://httpbin.org/ip', timeout=2)
                end = time.time()
                diff = end - start
                response.status
                print response.status, diff
            except:
                print 'IP:', rs.getvalue('ip') + ':' + str(rs.getvalue('prot')), '已失效'
                rs2 = RecordSet()
                t = (datetime.now(), '0', rs.getvalue('id'))
                rs2.execute_sql(ur'update proxyIP set verificationtime=%s,flag=%s where id =%s', t)

    @staticmethod
    def test_http_proxyip(proxyip, testurl='http://httpbin.org/ip'):
        proxy = urllib2.ProxyHandler({'http': proxyip.ip})
        opener = urllib2.build_opener(proxy)
        diff = -1
        status = -1
        try:
            start = time.time()
            res = opener.open(testurl, timeout=2)
            end = time.time()
            diff = end - start
            status = res.code
            print 'IP:', proxyip.ip, 'testURL:', testurl, ' status:', status, ' time:', diff
            rs = RecordSet()
            t = (datetime.now(), '1', proxyip.id)
            rs.execute_sql(ur'update proxyIP set verificationtime=%s,flag=%s where id =%s', t)
            return True
        except urllib2.HTTPError, e:
            status = e.code
            print 'IP:', proxyip.ip, 'testURL:', testurl, ' status:', status, ' time:', diff, 'erro:', e
            rs = RecordSet()
            t = (datetime.now(), '0', proxyip.id)
            rs.execute_sql(ur'update proxyIP set verificationtime=%s,flag=%s where id =%s', t)
            return False
        except Exception, e:
            print 'IP:', proxyip.ip, 'testURL:', testurl, ' status:', status, ' time:', diff, 'erro:', e
            rs = RecordSet()
            t = (datetime.now(), '0', proxyip.id)
            rs.execute_sql(ur'update proxyIP set verificationtime=%s,flag=%s where id =%s', t)
            return False




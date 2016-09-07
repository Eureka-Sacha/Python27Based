import urllib2
import urllib

url = 'http://localhost:8081/ririshun/user/login'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
values = {'userId': '111111',
          'password': '11111'}
headers = {'User-Agent': user_agent}
data = urllib.urlencode(values)
req = urllib2.Request(url, data, headers)
try:
    response = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print 'The server could not fulfill the request.'
    print 'Error code: ', e.code
except urllib2.URLError, e:
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason
else:
    the_page = response.read()
    print the_page
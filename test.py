from urllib2 import Request, urlopen, URLError
from cookielib import CookieJar as cj

someurl = 'http://actus.clicanoo.re/rubrique/actu/sant%C3%A9'
det = {'User-Agent': 'azot-extractor-0.1',
        'cookies': cj(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
req = Request(someurl, headers = det)
urlopen(req)
#try:
#    print("Ok on teste")
#    response = urlopen(req)
#    print(response.info())
#    print(response.geturl())
#except URLError as e:
#    if hasattr(e, 'reason'):
#        print 'We failed to reach a server.'
#        print 'Reason: ', e.reason
#    elif hasattr(e, 'code'):
#        print 'The server couldn\'t fulfill the request.'
#        print 'Error code: ', e.code
#else:
#    print('OK')

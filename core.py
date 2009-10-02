import re, cgi, bz2
from google.appengine.api import urlfetch
import models, tools

ADDRESS = 'http://www.peeep.us/'
ADDRESS2 = 'http://peeep.us/'

class NotFound(Exception):
	pass
class Forbidden(Exception):
	pass
class DownloadFail(Exception):
	pass

def decodeContent(content):
	if content[0:2] == 'BZ':
		return bz2.decompress(content)
	return content
		
def fetch(url):
	try:
		req, a_url = tools.smartFetch(tools.asciify_url(url), allow_truncated=True, deadline=10)
	except urlfetch.Error, e:
		raise DownloadFail(url, e)
	if req.status_code != 200: raise DownloadFail(url, req.status_code)
	content = req.content
	contentType = req.headers['Content-type']
	return content, contentType, a_url
	
#def invalidateCache(page):
#	caches = models.Cache.all().filter('page =', page).fetch(2000)
#	for cache in caches:
#		cache.delete()
		
def getCache(page):
	return models.Cache.all().filter('page =', page).filter('url =', tools.md5(unicode(page.url))).get()
		
#def updateCache(page, content=None, contentType=None, invalidate=False):
#	if invalidate:
#		invalidateCache(page)
#	
#	if content is None:
#		content, contentType = fetch(page)
#		
#	content = bz2.compress(content)
#	cache = models.Cache(page=page, url=tools.md5(unicode(page.url)), content=content, contentType=contentType)
#	cache.put()
#	return cache
	
def preprocessHtml(html, url):
	safe_url = cgi.escape(url, True).encode('utf-8')
	html, n = re.subn(r'(?iL)(<head\b[^>]*>)', r'\1<!--PEEEP--><base href="%s"/><!--/PEEEP-->'%safe_url, html, count=1)
	if n == 0:
		html, n = re.subn(r'(?iL)(<html\b[^>]*>)', r'\1<!--PEEEP--><head><base href="%s"/><!--/PEEEP-->'%safe_url, html, count=1)
		
		if n == 0:
			html, n = re.subn(r'(?iL)(<!DOCTYPE\b[^>]*>)', r'\1<!--PEEEP--><head><base href="%s"/><!--/PEEEP-->'%safe_url, html, count=1)
		
			if n == 0:
				html = '<!--PEEEP--><base href="%s"/><!--/PEEEP-->'%safe_url + html
		
	return html
	
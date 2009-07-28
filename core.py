import re, cgi
from google.appengine.api import urlfetch
import models, tools

ADDRESS = 'http://localhost:8080/'

class NotFound(Exception):
	pass
class Forbidden(Exception):
	pass
class DownloadFail(Exception):
	pass


def fetch(page):
	headers = {}
	if page.cookie:
		headers['Cookie'] = page.cookie
		
	req, a_url = tools.smartFetch(tools.asciify_url(page.url), headers=headers, allow_truncated=True, deadline=10)
	if req.status_code != 200: raise DownloadFail(page.url, req.status_code)
	content = req.content
	contentType = req.headers['Content-type'][:500]
	
	if tools.isHtml(contentType):
		content = preprocessHtml(content, a_url)
		
	return content, contentType
	
def invalidateCache(page):
	caches = models.Cache.all().filter('page =', page).fetch(2000)
	for cache in caches:
		cache.delete()
		
def getCache(page):
	return models.Cache.all().filter('page =', page).filter('url =', tools.md5(unicode(page.url))).get()
		
def updateCache(page, content=None, contentType=None, invalidate=False):
	if invalidate:
		invalidateCache(page)
	
	if content is None:
		content, contentType = fetch(page)
		
	cache = models.Cache(page=page, url=tools.md5(unicode(page.url)), content=content, contentType=contentType)
	cache.put()
	return cache
	
def preprocessHtml(html, url):
	safe_url = cgi.escape(url, True).encode('utf-8')
	html, n = re.subn('(?iL)(<head\\b[^>]*>)', '\\1<!--PEEEP--><base href="%s"/><!--/PEEEP-->'%safe_url, html, count=1)
	if n == 0:
		html, n = re.subn('(?iL)(<html\\b[^>]*>)', '\\1<!--PEEEP--><head><base href="%s"/><!--/PEEEP-->'%safe_url, html, count=1)
		
		if n == 0:
			html = '<!--PEEEP--><base href="%s"/><!--/PEEEP-->'%safe_url + html
		
	return html
	
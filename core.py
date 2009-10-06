import re, cgi, bz2
from google.appengine.api import urlfetch
import models, tools
import os

ADDRESS = 'http://www.peeep.us/'
ADDRESS2 = 'http://peeep.us/'

def getEffectiveAddress():
	address = ADDRESS
	if 'HTTP_HOST' in os.environ:
		address = 'http://%s/' % os.environ['HTTP_HOST']
	return address
	
def getBookmarklet(html=False):
	code = (u"javascript: void(function(){var s=document.createElement('script'),sa='setAttribute';s[sa]('type','text/javascript');"+
		u"s[sa]('src','%sassets/send.js');document.body.appendChild(s); })();" % getEffectiveAddress())
	if html:
		code = u'''<a href="%s" onclick="window.alert('Drag this link to your bookmark bar'); return false">Get peeep link</a>''' % code
	return code

class NotFound(Exception):
	pass
class Forbidden(Exception):
	pass
class DownloadFail(Exception):
	pass

def decodeContent(content):
	if content[0:2] == 'BZ':
		try:
			return bz2.decompress(content)
		except IOError, e:
			return content
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
		
def getCache(page):
	return models.Cache.all().filter('page =', page).filter('url =', tools.md5(unicode(page.url))).get()
		
def preprocessHtml(html, url):
	safe_url = cgi.escape(url, True).encode('utf-8')
	offs = 0
	
	m = re.match(r'(?iL)((?:\s+|<!DOCTYPE\b[^>]*>|<html\b[^>]*>|<head\b[^>]*>)*)', html)
	if m: # skip any heading tags
		offs = m.end(0)
	
	html = html[:offs] + r'<!--PEEEP--><base href="%s"/><!--/PEEEP-->'%safe_url + html[offs:]
		
	return html
	
#def invalidateCache(page):
#	caches = models.Cache.all().filter('page =', page).fetch(2000)
#	for cache in caches:
#		cache.delete()
	
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
	
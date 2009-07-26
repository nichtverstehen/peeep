import re, cgi
from google.appengine.api import urlfetch
import tools

ADDRESS = 'http://ppeeepp.appspot.com/'

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
		
	req, a_url = tools.smartFetch(page.url, headers=headers, allow_truncated=True, deadline=10)
	if req.status_code != 200: raise DownloadFail(req.status_code)
	content = req.content
	contentType = req.headers['Content-type']
	
	if tools.isHtml(contentType):
		content = preprocessHtml(content, a_url)
		
	return content, contentType
	
def preprocessHtml(html, url):
	safe_url = cgi.escape(url, True).encode('utf-8')
	html, n = re.subn('(?iL)(<head\\b[^>]*>)', '\\1<!--PPEEPP--><base href="%s"/><!--/PPEEPP-->'%safe_url, html, count=1)
	if n == 0:
		html, n = re.subn('(?iL)(<html\\b[^>]*>)', '\\1<!--PPEEPP--><head><base href="%s"/><!--/PPEPP-->'%safe_url, html, count=1)
		
		if n == 0:
			html = '<!--PPEEPP--><base href="%s"/><!--/PPEPP-->'%safe_url + html
		
	return html
	
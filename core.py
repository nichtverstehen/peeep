import urllib2, re, cgi
import tools

ADDRESS = 'http://localhost:8080/'

class NotFound(Exception):
	pass

def fetch(page):
	req = urllib2.Request(page.url)
	if page.cookie:
		req.add_header('Cookie', page.cookie)
		
	resp = urllib2.urlopen(req)
	content = resp.read()
	contentType = resp.info()['Content-type']
	
	if tools.isHtml(contentType):
		content = preprocessHtml(content, resp.geturl())
		
	return content, contentType
	
def preprocessHtml(html, url):
	safe_url = cgi.escape(url, True)
	html, n = re.subn('(?i)(<head\s*>)', '\\1<!--PPEEPP--><base href="%s"/><!--/PPEEPP-->'%safe_url, html, count=1)
	if n == 0:
		html, n = re.subn('(?i)(<html\s*>)', '\\1<!--PPEEPP--><head><base href="%s"/><!--/PPEPP-->'%safe_url, html, count=1)
		
		if n == 0:
			html = '<!--PPEEPP--><base href="%s"/><!--/PPEPP-->'%safe_url + html
		
	return html
	
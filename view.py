import re, os, cgi
import models, tools
from core import *
from google.appengine.api import users

def main():
	try:
		path = os.environ['PATH_INFO']
		match = re.match("^/([0-9a-f]{8})(/actual)?/?$", path)
		id = match.group(1)
		act = match.group(2) == '/actual'
		
		page = models.Page.get_by_key_name('K'+id)
		if page is None or page.public < 1: raise NotFound
		
		if act:
			content, contentType = fetch(page)
		else:
			cache = models.Cache.all().filter('page =', page).filter('url =', page.url).get()
			if cache is None: raise NotFound
			content, contentType = cache.content, cache.contentType
		
		if tools.isHtml(contentType):
			content = createControls(content, page)
			
		print 'Content-type: ', contentType
		print
		print content
		
	except NotFound:
		tools.logException()
		tools.redirect('/')
	
def createControls(html, page):
	controls = '<!--PPEEPP--><style type="text/css">html{padding-top:17px!important;}</style>'+\
		'<div style="position:fixed;left:0;top:0;padding: 2px 10px;width:100%%;'+\
		'font:normal 12px Arial,sans-serif;background:#ffc;border-bottom:1px solid #cb5;">'+\
		'<a href="%(ppeepp)s%(id)s">Cached</a> | <a href="%(ppeepp)s%(id)s/actual">Actual</a> | <a href="%(url)s">Original</a></div>'+\
		'<!--/PPEEPP-->'
	controls = controls % {
		'ppeepp': ADDRESS,
		'id': page.key().name().encode('utf-8')[1:],
		'url': cgi.escape(page.url.encode('utf-8'))
	}
	
	html, n = re.subn('(?iL)(<body\\s*>)', '\\1%s'%controls, html, count=1)
	if n == 0:
		html, n = re.subn('(?iL)(<html\\s*>)', '\\1%s'%controls, html, count=1)
		if n == 0:
			html = controls + html
			
	return html
	
if __name__ == "__main__":
	main()
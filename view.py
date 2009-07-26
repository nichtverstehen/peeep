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
		
		cache = models.Cache.all().filter('page =', page).filter('url =', page.url).get()
		if act:
			content, contentType = fetch(page)
		else:
			if cache is None: raise NotFound
			content, contentType = cache.content, cache.contentType
		
		if tools.isHtml(contentType):
			content = createControls(content, page, cache, act)
			
		print 'Content-type: ', contentType
		print
		print content
		
	except NotFound:
		tools.logException()
		tools.redirect('/')
	
def createControls(html, page, cache, act):
	date = ' title="%s"'%cache.date.strftime('%a, %d %b %Y %H:%M:%S %Z') if cache else ''
	cached = '<a href="%(ppeepp)s%(id)s"'+date+'>Cached</a>' if act else '<a'+date+' class="act">Cached</a>'
	actual = '<a href="%(ppeepp)s%(id)s/actual">Actual</a>' if not act else '<a class="act">Actual</a>'
	
	controls = '''<!--PPEEPP--><style type="text/css"> 
	html { margin-top: 23px!important; } body { _margin-top: 23px!important; }
	#ppeepp_toolbar, #ppeepp_toolbar div { display: block; outline: 0; border: 0; overflow: hidden; visibility: visible;
		color: #999; vertical-align: baseline; text-transform: none; white-space: normal; background: none; margin: 0; padding: 0;
		font: normal 12px Arial, sans-serif; text-align: left; line-height: 16px; zoom: 1; }
	#ppeepp_toolbar a:link, #ppeepp_toolbar a:hover, #ppeepp_toolbar a:visited, #ppeepp_toolbar a:active, #ppeepp_toolbar a:focus { color: #00f; }
	#ppeepp_toolbar { position:absolute; z-index: 1025; left:0; top:0; width:100%%; height: 23px;
		 background: #ffc; }
	#ppeepp_toolbar .original_link { font-size: .9em; color: #999; float: left; margin-left: 2em; }
	#ppeepp_toolbar .original_link a { color: #999; }
	#ppeepp_toolbar .original_link a:visited { color: #bbb; }
	#ppeepp_toolbar .mode_switch { float: left; margin: 0 1em; }
	#ppeepp_toolbar .mode_switch a.act { text-decoration: none; font-weight: bold; color: #333; }
	</style>
	<div id="ppeepp_toolbar"><div style="padding: 3px 10px; border-bottom: 1px solid #cb5; overflow: hidden; _zoom: 1;">
		<a href="%(ppeepp)s"><img src="%(ppeepp)sassets/ppeepp.png" alt="ppeepp" title="ppeepp url shortener" 
			style="float: left; border: 0;" width="16" height="16" /></a>
		<div style="float: right;">
			<form method="post" action="%(ppeepp)supdate.php">
				<input type="hidden" name="id" value="%(id)s"/><input type="hidden" name="token" value="%(token)s"/>
				<input type="hidden" name="action" value="del"/>
				<input type="image" src="%(ppeepp)sassets/del.png" alt="delete" title="remove page from ppeepp"
					onclick="return confirm('Are you sure to remove the page from ppeepp?');"/>
			</form>
		</div>
		<div class="mode_switch">%(cached)s | %(actual)s</div>
		<div class="original_link"><a href="%(url)s">%(url)s</a></div>
	</div></div><!--/PPEEPP-->'''
	ctx = {
		'ppeepp': ADDRESS,
		'id': page.key().name().encode('utf-8')[1:],
		'url': cgi.escape(page.url.encode('utf-8')),
		'token': tools.token(page),
	}
	ctx['cached'] = cached % ctx
	ctx['actual'] = actual % ctx
	controls = controls % ctx
	
	html, n = re.subn('(?iL)(<body\\s*>)', '\\1%s'%controls, html, count=1)
	if n == 0:
		html, n = re.subn('(?iL)(<html\\s*>)', '\\1%s'%controls, html, count=1)
		if n == 0:
			html = controls + html
			
	return html
	
if __name__ == "__main__":
	main()
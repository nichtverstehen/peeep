import re, os, cgi, urllib
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
	id = page.key().name().encode('utf-8')[1:]
	url = ADDRESS+id
	date = ' title="%s"'%cache.date.strftime('%a, %d %b %Y %H:%M:%S %Z') if cache else ''
	cached = '<a href="%(ppeepp)s%(id)s"'+date+'>Cached</a>' if act else '<a'+date+' class="act">Cached</a>'
	actual = '<a href="%(ppeepp)s%(id)s/actual">Actual</a>' if not act else '<a class="act">Actual</a>'
	mailshare = 'mailto:?subject=%5Bppeepp%5D%20Get%20a%20link&body=Hi!%0A%0AYour%20friend%20shared%20this%20link%20with%20you:%0A'+url+'%0A%0A%0A--%0APPEEPP%2C%20more%20than%20a%20url%20shortener%0Ahttp://www.ppeepp.net/'
	twittershare = "http://twitter.com/home?status="+urllib.quote(url);
	gmailshare = "https://mail.google.com/mail/?view=cm&fs=1&tf=1&to=&su=" + "%5Bppeepp%5D%20Get%20a%20link" + "&body=" + 'Hi!%0A%0AYour%20friend%20shared%20this%20link%20with%20you:%0A'+urllib.quote(url)+'%0A%0A%0A--%0APPEEPP%2C%20more%20than%20a%20url%20shortener%0Ahttp://www.ppeepp.net/' + "&zx=BITLY&shva=1&disablechatbrowsercheck=1&ui=1"
	fbshare = 'http://www.facebook.com/sharer.php?u='+urllib.quote(url)+"&t="+'%5Bppeepp%5D'
	
	controls = '''<!--PPEEPP--><style type="text/css"> 
	html { margin-top: 23px!important; } body { _margin-top: 23px!important; }
	#ppeepp_toolbar, #ppeepp_toolbar div, #ppeepp_toolbar input, #ppeepp_toolbar form { display: block; overflow: hidden;
		margin: 0; padding: 0; text-align: left; zoom: 1; visibility: visible; line-height: 16px; }
	#ppeepp_toolbar, #ppeepp_toolbar div, #ppeepp_toolbar input, #ppeepp_toolbar a, #ppeepp_toolbar span {
		outline: 0; border: 0; color: #999; vertical-align: baseline;
		text-transform: none; white-space: normal; background: none; font: normal 12px Arial, sans-serif; }
	#ppeepp_toolbar img { border: 0; }
	#ppeepp_toolbar a:link, #ppeepp_toolbar a:hover, #ppeepp_toolbar a:visited, #ppeepp_toolbar a:active, #ppeepp_toolbar a:focus { color: #00f; }
	#ppeepp_toolbar { position:absolute; z-index: 1025; left:0; top:0; width:100%%; height: 23px;
		 background: #ffc; }
	#ppeepp_toolbar .original_link { font-size: .9em; color: #999; float: left; margin-left: 2em; }
	#ppeepp_toolbar .original_link a { color: #999; }
	#ppeepp_toolbar .original_link a:visited { color: #bbb; }
	#ppeepp_toolbar .mode_switch { float: left; margin: 0 1em; }
	#ppeepp_toolbar .mode_switch a.act { text-decoration: none; font-weight: bold; color: #333; }
	#ppeepp_toolbar .shares { float: right; line-height: 10px;/*?see Chrome*/ margin: -3px 20px -6px 0; padding: 3px 3px; }
	#ppeepp_toolbar .shares img { margin: 0; padding: 0; }
	#ppeepp_toolbar .shares .share { display: none; margin: 0 0 0 3px; }
	#ppeepp_toolbar .shares:hover, #ppeepp_toolbar .shares.hover { background: #eec; }
	#ppeepp_toolbar .shares:hover .grip, #ppeepp_toolbar .shares.hover .grip { display: none; }
	#ppeepp_toolbar .shares:hover .share, #ppeepp_toolbar .shares.hover .share { display: inline; }
	</style>
	<div id="ppeepp_toolbar"><div style="padding: 3px 10px; border-bottom: 1px solid #cb5; overflow: hidden; zoom: 1;">
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
		<div class="shares" onmouseover="this.className='shares hover'" onmouseout="this.className='shares'">
			<a class="share" href="%(mailshare)s"><img src="%(ppeepp)sassets/mail.png" alt="mail" title="Email this link"/></a>
			<a class="share" href="%(gmailshare)s" target="_blank"><img src="%(ppeepp)sassets/gmail.png" alt="gmail" title="Send this link with GMail"/></a>
			<a class="share" href="%(fbshare)s" target="_blank"><img src="%(ppeepp)sassets/facebook.png" alt="facebook" title="Share on Facebook"/></a>
			<a class="share" href="%(twittershare)s" target="_blank"><img src="%(ppeepp)sassets/twitter.png" alt="twitter" title="Share on Twitter"/></a>
			<span class="grip"><img src="%(ppeepp)sassets/share.png" alt="Share..." /></span>
		</div>
		<div class="mode_switch">%(cached)s | %(actual)s</div>
		<div class="original_link"><a href="%(url)s">%(url)s</a></div>
	</div></div>
	
<script type="text/javascript">var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));</script>
<script type="text/javascript">
try { var pageTracker = _gat._getTracker("UA-836471-6"); pageTracker._trackPageview(); }
catch(err) {}</script>

	<!--/PPEEPP-->'''
	ctx = {
		'ppeepp': ADDRESS,
		'id': id,
		'mailshare': mailshare,
		'twittershare': twittershare,
		'gmailshare': gmailshare,
		'fbshare': fbshare,
		'url': cgi.escape(page.url.encode('utf-8'), True),
		'token': tools.token(page),
	}
	ctx['cached'] = cached % ctx
	ctx['actual'] = actual % ctx
	controls = controls % ctx
	
	html, n = re.subn('(?iL)(<body\\b[^>]*>)', '\\1%s'%controls, html, count=1)
	if n == 0:
		html, n = re.subn('(?iL)(<html\\b[^>]*>)', '\\1%s'%controls, html, count=1)
		if n == 0:
			html = controls + html
			
	return html
	
if __name__ == "__main__":
	main()
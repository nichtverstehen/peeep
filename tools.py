import traceback, logging
import sys, hashlib
import template
from google.appengine.api import urlfetch, users

def md5(s):
	if type(s) is unicode:
		s = s.encode('utf-8')
	
	md5 = hashlib.md5()	
	md5.update(s.encode('utf-8'))
	sig = md5.hexdigest()
	return sig
	
def token(page):
	SALT = "I DO NOT WANT TO WORK"
	user = users.get_current_user()
	
	s = page.key().name()
	if user:
		s += user.user_id()
	s+=SALT
	
	return md5(s)
	
def smartFetch(url, **kwargs):
	"""UrlFetch following redirects and returning actual URL"""
	a_url = url
	c = 0
	while True or c > 5:
		req = urlfetch.fetch(a_url, follow_redirects=False, **kwargs)
		if req.status_code in range(301, 303) or req.status_code == 307:
			a_url = req.headers['location']
		else:
			break
		c += 1
			
	return req, a_url
	
def isHtml(contentType):
	return contentType.startswith('text/html') or contentType.startswith('application/xhtml+xml')
	
def set_trace():
    import pdb, sys
    debugger = pdb.Pdb(stdin=sys.__stdin__, 
        stdout=sys.__stdout__)
    debugger.set_trace(sys._getframe().f_back)
	
def redirect(url):
	print "Status: 302"
	print "Location: ", url
	print
	print "Redirecting to ", url

def logException():
	tp, exc, tb = sys.exc_info()
	text = traceback.format_exc()
	log = logging.getLogger()
	log.error("%s %s\n%s", str(tp), unicode(exc), text)
	
def printError(title, text = ""):
	print template.render("Error", '<h3 class="first">%s</h3><p>%s</p>' % (title, text), tagline='<a href="/">ppeepp</a>')
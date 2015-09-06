import traceback, logging
import sys, hashlib, urlparse, urllib
import template, core
from google.appengine.api import urlfetch, users

def md5(s):
	if type(s) is unicode:
		s = s.encode('utf-8')
	
	md5 = hashlib.md5()	
	md5.update(s)
	sig = md5.hexdigest()
	return sig
	
def token(page, user):
	SALT = "I DO NOT WANT TO WORK"
	
	s = SALT
	s += page.key().name()
	if user and core.isAnonymous(user):
		s += user.email()
	elif user and user.user_id():
		s += user.user_id()

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
	print template.ErrorTemplate(title="Error", text=text).utf8()
	
def asciify_url(url, force_quote=False):  
    r"""Attempts to make a unicode url usuable with ``urllib/urllib2``. 
 
    More specifically, it attempts to convert the unicode object ``url``, 
    which is meant to represent a IRI, to an unicode object that, 
    containing only ASCII characters, is a valid URI. This involves: 
 
        * IDNA/Puny-encoding the domain name. 
        * UTF8-quoting the path and querystring parts. 
 
    See also RFC 3987. 
	Author http://elsdoerfer.name/
	http://blog.elsdoerfer.name/2008/12/12/opening-iris-in-python/
    """  
    # if type(url) is unicode:
	#	 url = url.encode('utf-8')
  
    parts = urlparse.urlsplit(url)  
    # if not parts.scheme or not parts.netloc:  
    #    apparently not an url  
    #    return url  
  
    # idna-encode domain  
    hostname = parts.hostname.encode('idna')  
  
    # UTF8-quote the other parts. We check each part individually if  
    # if needs to be quoted - that should catch some additional user  
    # errors, say for example an umlaut in the username even though  
    # the path *is* already quoted.  
    def quote(s, safe):  
        s = s or ''  
        # Triggers on non-ascii characters - another option would be:  
        #     urllib.quote(s.replace('%', '')) != s.replace('%', '')  
        # which would trigger on all %-characters, e.g. "&".  
        if s.encode('ascii', 'replace') != s or force_quote:  
            return urllib.quote(s.encode('utf8'), safe=safe)  
        return s  
    username = quote(parts.username, '')  
    password = quote(parts.password, safe='')  
    path = quote(parts.path, safe='/')  
    query = quote(parts.query, safe='&=')  
  
    # put everything back together  
    netloc = hostname  
    if username or password:  
        netloc = '@' + netloc  
        if password:  
            netloc = ':' + password + netloc  
        netloc = username + netloc  
    if parts.port:  
        netloc += ':' + str(parts.port)  
    return urlparse.urlunsplit([  
        parts.scheme, netloc, path, query, parts.fragment])  
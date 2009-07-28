import cgi, time, os
import models, tools
from core import *
from google.appengine.api import users, urlfetch

ID_SALT = u"Don't you want to get a job?"

def main():
	if os.environ['REQUEST_METHOD'] != 'POST': # Forbidden
		tools.redirect('/')
		exit()
		
	form = cgi.FieldStorage()
	r_url = form.getfirst("r_url")
	r_cookie = form.getfirst("r_cookie")
	r_url = unicode(r_url, 'utf-8') if r_url else None
	r_cookie = unicode(r_cookie, 'utf-8') if r_cookie else None
	
	if not r_url or r_url == 'http://': # url not passed
		tools.redirect('/')
		exit()
	
	id = tools.md5(ID_SALT+r_url+unicode(time.time()))[:8]
	page = models.Page(key_name='K'+id, url=r_url, cookie=r_cookie)
	
	try:
		content, contentType = fetch(page)
	except (urlfetch.Error,DownloadFail):
		tools.printError('Download error', 'Sorry, we couldn\'t access to address you provided. Please try again in a few seconds.')
		tools.logException()
		exit()
	
	page.put()
	updateCache(page, content, contentType)
	
	tools.redirect('/'+id)
	
if __name__ == "__main__":
	main()
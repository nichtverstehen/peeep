import cgi, time
import models, tools
from core import *
from google.appengine.api import users

ID_SALT = "Don't you want to get a job?"

def main():
	form = cgi.FieldStorage()
	r_url = form.getfirst("r_url")
	r_cookie = form.getfirst("r_cookie")
	
	if not r_url or r_url == 'http://': # url not passed
		tools.redirect('/')
		exit()
	
	id = tools.md5(ID_SALT+r_url+str(time.time()))[:8]
	page = models.Page(key_name='K'+id, url=r_url, cookie=r_cookie)
	
	try:
		content, contentType = fetch(page)
	except urllib2.URLError:
		tools.redirect('/?error=1')
		exit()
	
	page.put()
	cache = models.Cache(page=page, url=page.url, content=content, contentType=contentType)
	cache.put()
	
	tools.redirect('/'+id)
	
if __name__ == "__main__":
	main()
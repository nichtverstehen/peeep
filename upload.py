import cgi, time, os
from google.appengine.api import users
import models, tools
from core import *

ID_SALT = u"Don't you want to get a job?"

def main():
	if os.environ['REQUEST_METHOD'] != 'POST': # Forbidden
		tools.redirect('/')
		exit()
		
	form = cgi.FieldStorage()
	r_url = form.getfirst("r_url")
	r_content = form.getfirst("r_content")
	r_type = form.getfirst("r_type")
	r_url = unicode(r_url, 'utf-8') if r_url else None
	r_content = r_content if r_content else None
	r_type = unicode(r_type, 'utf-8') if r_type else None
	verified = False
	
	if not r_url or r_url == 'http://': # url not passed
		tools.redirect('/')
		exit()
		
	if not r_url.startswith('http://') and not r_url.startswith('https://'):
		r_url = 'http://'+r_url

	user = users.get_current_user()
	public = 1 if user is not None else 0
	if user:
		owner = user
	else:
		owner = generateAnonymous()
		
	try:
		if not r_content or not r_type:
			r_content, r_type, r_url = fetch(r_url)
			verified = True
	except DownloadFail, e:
		tools.printError('Download error', 'Sorry, we couldn\'t access to address you provided. Please try again in a few seconds.')
		tools.logException()
		exit()
	
	id = tools.md5(ID_SALT+r_url+unicode(time.time()))[:8]
	page = models.Page(key_name='K'+id, url=r_url, owner=owner, public=public)
	page.put()
	
	if tools.isHtml(r_type):
		r_content = preprocessHtml(r_content, r_url)
		
	content = bz2.compress(r_content)
	cache = models.Cache(page=page, url=tools.md5(unicode(page.url)), content=content, contentType=r_type, verified=verified)
	cache.put()
	
	if user:
		tools.redirect('/'+id)
	else:
		cookies = {'anonymous_token': tools.token(page, owner)}
		headers = [
			tools.formatCookie(cookies, 60*60*24)
		]
		tools.redirect(users.create_login_url('/confirm.php?id=%s' % id), headers)
	
if __name__ == "__main__":
	main()
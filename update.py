import re, os, cgi
import models, tools
import template
from core import *
from google.appengine.api import users

def main():
	try:
		if os.environ['REQUEST_METHOD'] != 'POST': # Forbidden
			raise Forbidden
		user = users.get_current_user()
		if user == None:
			raise Forbidden
			
		form = cgi.FieldStorage()
		r_id = form.getfirst("id")
		r_token = form.getfirst("token")
		r_action = form.getfirst("action")
		
		if r_action != 'del':
			raise Forbidden
		page = models.Page.get_by_key_name('K'+r_id)
		if page is None or page.public < 0: raise NotFound
		
		if not users.is_current_user_admin() and page.owner != user:
			raise Forbidden
		if r_token != tools.token(page, user):
			raise Forbidden
			
		page.public = -1
		page.put()
		
		tools.redirect('/my')
	except Forbidden:
		tools.printError("Forbidden", "You've just tried to do some evil thing. We didn't expect that of you.")
	except NotFound:
		tools.printError("Not found", "We think you are playing unfair.")
	
if __name__ == "__main__":
	main()

import Cookie
from google.appengine.api import users
import tools
from core import *

def main():
	try:
		args = cgi.FieldStorage()
		r_id = args.getfirst("id")
		cookies = Cookie.SimpleCookie(os.environ['HTTP_COOKIE'])
		r_token = cookies['anonymous_token'].value

		user = users.get_current_user()
		if not user: raise Forbidden

		page = models.Page.get_by_key_name('K'+r_id)
		if page is None: raise NotFound(id)

		if page.public != 0: raise Forbidden
		if not isAnonymous(page.owner): raise Forbidden
		if r_token != tools.token(page, page.owner): raise Forbidden

		page.public = 1
		page.owner = user
		page.put()

		tools.redirect('/'+page.key().name()[1:])
	except Forbidden:
		tools.printError("Forbidden", "You've just tried to do some evil thing. We didn't expect that of you.")
	except NotFound:
		tools.printError("Not found", "We think you are playing unfair.")

if __name__ == "__main__":
	main()

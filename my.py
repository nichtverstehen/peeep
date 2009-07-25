import re, os, cgi
import models, tools
import template
from core import *
from google.appengine.api import users

def main():
	user = users.get_current_user()
	pages = models.Page.all().filter('owner =', user).filter('public >', 0).order('-public').order('-date').fetch(2000)
	
	line = '''<tr>
		<td><a href="/%(id)s">%(url)s</a></td>
		<td><form method="post" action="/update.php">
			<input type="hidden" name="id" value="%(id)s/><input type="hidden" name="token" value="%(token)s"/>
			<input type="image" src="/assets/del.png" alt="Remove"/>
		</form></td>
	</tr>'''
	html = '''<table>
		<colgroup><col/><col width="16"/></cols>\n'''
	html += '\n'.join([line%{'id':p.key().name()[1:], 'url':cgi.escape(p.url), 'token': tools.token(p)} for p in pages])
	html += '\n</table>'
	
	print template.render('Your pages', html, tagline='<a href="/">ppeepp</a>')
	
if __name__ == "__main__":
	main()
import re, os, cgi
import models, tools
import template
from core import *
from google.appengine.api import users

def main():
	user = users.get_current_user()
	if user is None: # do not show anonymous uploads with unworking del button
		tools.redirect('/')
		
	pages = models.Page.all().filter('owner =', user).filter('public >', 0).order('-public').order('-date').fetch(2000)
	
	line = '''<tr>
		<td><a href="/%(id)s">%(url)s</a></td>
		<td><form method="post" action="/update.php">
			<input type="hidden" name="id" value="%(id)s"/><input type="hidden" name="token" value="%(token)s"/>
			<input type="hidden" name="action" value="del"/>
			<input type="image" src="/assets/del.png" alt="Remove" onclick="return confirm('Are you sure to remove the page from ppeepp?');"/>
		</form></td>
	</tr>'''
	html = '''<table>
		<colgroup><col/><col width="16"/></cols>\n'''
	if pages:
		html += '\n'.join([line%{'id':p.key().name()[1:], 'url':cgi.escape(p.url, True), 'token': tools.token(p)} for p in pages])
	else:
		html += "You haven't created any links using ppeepp."
	html += '\n</table>'
	
	print template.render('Your pages', html, tagline='<a href="/">ppeepp</a>')
	
if __name__ == "__main__":
	main()
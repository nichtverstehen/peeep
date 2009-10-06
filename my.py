import re, os, cgi
import models, tools
import template
import xml.sax.saxutils
from core import *
from google.appengine.api import users

def main():
	user = users.get_current_user()
	if user is None: # do not show anonymous uploads with unworking del button
		tools.redirect('/')
		return
		
	pages = models.Page.all().filter('owner =', user).filter('public >', 0).order('-public').order('-date').fetch(2000)
	print MyTemplate(user=user, pages=pages).utf8()
	
class MyTemplate(template.PeeepTemplate): 
	title_template = u'Your pages'
	logininfo_template = u'''<h2>Your pages</h2>
	${user.email()} (<a href=${xml.sax.saxutils.quoteattr(users.create_logout_url('/'))}>logout</a>)\n'''
	content_template = u'''<div class="my_head login">
	$<logininfo_template>
</div>
$<list_pages>\n\n '''
	line_template = u'''	<tr>
		<td class="link"><div><a href="/$id">$url</a></div></td>
		<td>$date</td>
		<td><form method="post" action="/update.php"><div>
			<input type="hidden" name="id" value="$id"/><input type="hidden" name="token" value="$token"/>
			<input type="hidden" name="action" value="del"/>
			<input type="image" src="/assets/del.png" alt="Remove" onclick="return confirm('Are you sure to remove the page from peeep?');"/>
		</div></form></td>
	</tr>\n '''
	
	def list_pages(self, args, **kwargs):
		args.update(kwargs)
		user, pages = args.get('user'), args.get('pages')
		if pages:
			self.write(u'<table>\n<colgroup><col class="link"/><col class="date"/><col class="del"/></colgroup>\n')
			for p in pages:
				self.line_template(
					id=p.key().name()[1:], 
					url=cgi.escape(p.url, True),
					token=tools.token(p),
					date=p.date.strftime('%d %b %Y %H:%M'), 
					**kwargs)
			self.write('</table>');
		else:
			self.write(u"<p>You have no saved pages on peeep.</p>");
	
if __name__ == "__main__":
	main()
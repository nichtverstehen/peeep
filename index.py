import cgi
import template
from core import ADDRESS
from google.appengine.api import users

def main():
	form = cgi.FieldStorage()
	r_url = form.getfirst("r_url")
	
	print render(r_url);
	
	
def render(url = None):
	if url is None: url = 'http://'
	
	user = users.get_current_user()
	if user is None:
		login_info = '<a href="'+users.create_login_url('/')+'">Login</a> \n'+\
			'using <a href="https://www.google.com/accounts/NewAccount">Google Account</a> to manage your saved pages.'
	else:
		login_info = user.email()+u' (<a href="'+users.create_logout_url('/')+'">logout</a>). \n'+\
			'<a href="/my">Manage your links...</a>'
			
	js = "javascript: void(function(){var s=document.createElement('script'),sa='setAttribute';s[sa]('type','text/javascript');s[sa]('src','%sassets/send.js');document.body.appendChild(s); })();" % ADDRESS
	html = u'''\n\t<form method="post" id="upload" action="/upload.php" enctype=""application/x-www-form-urlencoded" accept-charset="utf-8">
		<div id="url_line">
			<input type="text" name="r_url" value="'''+cgi.escape(url, True)+'''" /><button type="submit">Submit</button>
		</div>
	</form>
	
	<div class="login">'''+login_info+'''</div>
	
	<div class="info">
		<p><strong>peeep</strong> is a next generation URL shortener.</p>
		<h3>Why use it?</h3>
		<ul class="features">
		<li>
			<p class="first">To save a snapshot of current state of a webpage.</p>
			<p class="descr">Peeep takes a snapshot of your page. So even if the author has altered content 
			on the page, peeep will always remember, what it looked like at the moment you took its peep-url.</p>
		</li>
		<li>
			<p class="first">To give links to protected pages normally viewable only by you.
			<p class="descr">You can ask peeep to store a snapshot of page, retrieved using your authentication information.
				For example you can send your friend a link to a protected 
				Facebook profile or forum topic without sharing your password with them.</p>
		</li>
		</ul>
	</div>
	
	<h3>Bookmarklet</h3>
	
	<p>
	To make links to protected pages drag this bookmarklet to your bookmarks toolbar:
	<a href="'''+cgi.escape(js)+'''" class="pseudobutton">Get peeep link</a>.</p>
	<p>Or you can just paste the bookmarklet url code to address field of the desired page and hit Enter.</p>'''
	
	return template.render("peeep.us", html, tagline="persistent url shortener")

if __name__ == "__main__":
	main()
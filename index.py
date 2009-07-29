import cgi
import template
from core import ADDRESS
from google.appengine.api import users

def main():
	form = cgi.FieldStorage()
	r_url = form.getfirst("r_url")
	r_cookie = form.getfirst("r_cookie")
	
	print render(r_url, r_cookie);
	
	
def render(url = None, cookie = None):
	if url is None: url = 'http://'
	if cookie is None: cookie = ''
	
	user = users.get_current_user()
	if user is None:
		login_info = '<a href="'+users.create_login_url('/')+'">Login</a> \n'+\
			'using <a href="https://www.google.com/accounts/NewAccount">Google Account</a> to manage your saved pages.'
	else:
		login_info = user.email()+u' (<a href="'+users.create_logout_url('/')+'">logout</a>). \n'+\
			'<a href="/my">Manage your links...</a>'
			
	js = "javascript:(function(){var enc=encodeURIComponent, a='%s?r_url='+enc(location.href)+'&r_cookie='+enc(document.cookie), m=function(){ if(!window.open(a)) location.href=a;}; m();})(); void 0" % ADDRESS
	html = u'''\n\t<form method="post" id="upload" action="/upload.php" enctype=""application/x-www-form-urlencoded" accept-charset="utf-8">
		<div id="url_line">
			<input type="text" name="r_url" value="'''+cgi.escape(url, True)+'''" /><button type="submit">Submit</button>
		</div>
		<div id="cookie">
			<label for="r_cookie">Cookie: </label>
			<input type="text" name="r_cookie" id="r_cookie" size="40" value="'''+cgi.escape(cookie, True)+'''" />
			<a href="#" title="Include authorization info..."
				onclick="var e=document.getElementById('cookie');e.className=e.className=='hide'?'':'hide';return false"
				class="js">Use cookie?</a>
			<script type="text/javascript">if (document.getElementById('r_cookie').value == '') document.getElementById('cookie').className = 'hide';</script>
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
			<p class="descr">You can ask peeep to store your cookie information securely, so that it can show
				desired page from your point of view. For example you can send your friend a link to a protected 
				Facebook profile or forum topic without sharing your password with them.</p>
		</li>
		</ul>
	</div>
	
	<h3>Bookmarklet</h3>
	
	<p>
	To make a link quickly drag this button to your bookmarks:
	<a href="'''+cgi.escape(js)+'''" class="pseudobutton">Get peeep link</a>.</p>
	<p>Or just paste this code to address field:</p>
	<div class="jscode">'''+js+'''</div>
	'''
	
	return template.render("peeep.us", html, tagline="persistent url shortener")

if __name__ == "__main__":
	main()
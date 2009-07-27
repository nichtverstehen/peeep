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
		<p><strong>peeep</strong> is a URL shortener that can:</p>
		<ul class="features">
		<li>
			<h3>cache.</h3>
			<p class="first">It stores a snapshot of current page state.</p>
			<p class="descr">Your correspondents will be able to see what the page looked like exactly at the exact moment you took its short URL.</p>
		</li>
		<li>
			<h3>use cookies.</h3>
			<p class="first">You can share a page, protected from public access.</p>
			<p class="descr">It securely stores cookies with your authentication information and you won't need to share your password with anyone just to
			show some private page.</p>
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
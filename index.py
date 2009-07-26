import template
from google.appengine.api import users

def main():
	print render();
	
	
def render():
	user = users.get_current_user()
	if user is None:
		login_info = '<a href="'+users.create_login_url('/')+'">Login</a> \n'+\
			'using <a href="https://www.google.com/accounts/NewAccount">Google Account</a> to manage your saved pages.'
	else:
		login_info = user.email()+u' (<a href="'+users.create_logout_url('/')+'">logout</a>). \n'+\
			'<a href="/my">Manage your documents</a>'
	html = u'''\n\t<form method="post" id="upload" action="/upload.php" enctype=""application/x-www-form-urlencoded" accept-charset="utf-8">
		<div id="url_line">
			<input type="text" name="r_url" value="http://" /><button type="submit">Submit</button>
		</div>
		<div id="cookie">
			<label for="r_cookie">Cookie: </label> <input type="text" name="r_cookie" id="r_cookie" size="40" />
			<a href="#" title="Include authorization info..."
				onclick="var e=document.getElementById('cookie');e.className=e.className=='hide'?'':'hide';return false"
				class="js">Use cookie?</a>
			<script type="text/javascript">document.getElementById('cookie').className = 'hide';</script>
		</div>
	</form>
	
	<div class="login">'''+login_info+'''</div>
	
	<div class="info">
		<p><strong>ppeepp</strong> is a URL shortener that can:</p>
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
	
	<p>To create a public</p>
	'''
	
	return template.render("ppeepp", html, tagline="persistent url shortener")

if __name__ == "__main__":
	main()
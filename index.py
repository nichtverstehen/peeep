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
		login_info = ('<b><a href="'+users.create_login_url('/')+'">Login</a></b> \n'+
			'using your <a href="https://www.google.com/accounts/NewAccount">Google account</a>')
	else:
		login_info = ('<b><a href="/my">Your links</a></b> \n'+
			user.email()+u' (<a href="'+users.create_logout_url('/')+'">logout</a>)\n')
			
	js = "javascript: void(function(){var s=document.createElement('script'),sa='setAttribute';s[sa]('type','text/javascript');s[sa]('src','%sassets/send.js');document.body.appendChild(s); })();" % ADDRESS
	html = u'''\n\t
<div class="section">

<h2>Save snapshot of a web page forever!</h2>

<div class="figure">
	<a href="http://www.peeep.us/3b953848"><img src="/assets/untitled.png" alt="nytimes"/></a>
</div>

<p>Peeep.us is more than a URL shortener. 
	It stores current contents of a web page 
	and gives you a link to it.</p>
<p>So even if the author alters or deletes 
	the page or even the whole site is shut down
	you will have a proof that it existed. </p>
<p>Peeep.us will always remember 
	what the page looked like at the moment 
	you gave it to peeep.us</p>
	
</div> <!-- .section -->

<form method="post" id="upload" action="/upload.php" enctype="application/x-www-form-urlencoded" accept-charset="utf-8">
<div class="fieldset">
	<input type="text" style="display: block; width: 84%; float: left;" name="r_url" value="'''+cgi.escape(url, True)+'''" />
	<button type="submit"><img src="assets/peeep.png" style=""/>submit</button>
</div>
</form>

<div class="section">

<h2>Create links to protected pages</h2>

<div class="bookmarklet">
	<a href="'''+cgi.escape(js)+'''" class="pseudobutton"><div>Get peeep link</div></a>

	<div>Drag this button to your
		Bookmarks toolbar.
		<!--Detailed instructions--></div>
</div> <!-- .bookmarklet -->

<p>Peeep can help if you want to share a link that is 
normally viewable only by you (it may be a resource r
equiring sign-up a private profile on a social network or 
just any private page publicly inaccessible). Just use a 
bookmarklet to send a page to Peeep and share the 
resulting link.</p>

</div> <!-- .section -->
	
	<!--div class="info">
		<div class="buttons">
			<a href="http://delicious.com/save" onclick="window.open('http://delicious.com/save?v=5&amp;noui&amp;jump=close&amp;url='+encodeURIComponent(location.href)+'&amp;title='+encodeURIComponent(document.title), 'delicious','toolbar=no,width=550,height=550'); return false;"><img src="http://static.delicious.com/img/delicious.gif" height="16" width="16" alt="Delicious" /></a>
			<a href="http://www.reddit.com/submit" onclick="window.location = 'http://www.reddit.com/submit?url=' + encodeURIComponent(window.location); return false"> <img src="http://www.reddit.com/static/spreddit1.gif" alt="submit to reddit" border="0" /> </a>
			<a href="http://digg.com/submit?phase=2&url=http://www.peeep.us/&title=New-generation%20URL%20shortener"><img src="http://digg.com/img/badges/16x16-digg-guy.gif" width="16" height="16" alt="Digg this" title="Digg this"/></a>
			<a href="http://www.stumbleupon.com/submit?url=http://www.peeep.us/"> <img border="0" src="http://cdn.stumble-upon.com/images/16x16_su_solid.gif" alt=""></a>
		</div>
	</div-->
	
<div id="personal" class="pers bl">
<div class="pers br"><div class="pers tl"><div class="pers tr">

	<div class="login">'''+login_info+'''</div>

</div></div></div></div> <!-- #personal -->

	'''
	
	return template.render("Peeep.us", html, tagline="persistent url shortener")

if __name__ == "__main__":
	main()
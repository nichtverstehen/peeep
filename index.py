import cgi
import template, core
import xml.sax.saxutils
from core import getEffectiveAddress
from google.appengine.api import users

def main():
	form = cgi.FieldStorage()
	r_url = form.getfirst("r_url")
	user = users.get_current_user()
	print IndexTemplate(url=r_url, user=user).utf8()
	
class IndexTemplate(template.PeeepTemplate): 
	index = True
	bookmarklet = core.getBookmarklet()
	head_template = u'<script type="text/javascript" src="/assets/prompt.js"></script>'
	content_template = u'''\n\t
<div class="section">

	<h2>Save snapshot of a web page forever!</h2>

	<a href="http://www.peeep.us/3b953848" title="nytimes.com at Sep 30, 2009">
		<img src="/assets/screenshot.jpg" width="256" height="196" alt="nytimes.com at Sep 30, 2009" class="figure"/>
	</a>

	<p>Peeep.us is more than a URL shortener. It stores current contents of a web page 
		and gives you a link to the stored copy.</p>
	<p>So even if the author alters or deletes the page or even the whole site is shut down
		you will have a proof that it existed. </p>
	<p>Peeep.us will always remember what the page looked like at the moment 
		you gave it to peeep.us</p>
		
	</div> <!-- .section -->

	<form method="post" id="upload" action="/upload.php" enctype="application/x-www-form-urlencoded" accept-charset="utf-8">
	<div class="fieldset">
		<input type="text" class="text" name="r_url" id="r_url" value="${cgi.escape(url, True) if url is not None else ''}" />
		<button type="submit"><span>submit</span></button>
	</div>
	<script type="text/javascript">//<![CDATA[
		var input = document.getElementById('r_url');
		if (input && Prompt) { input.value = ''; new Prompt(input, 'Paste URL here', ''); }
	//]]></script>
	</form>

<div class="section">

	<h2>Create links to protected pages</h2>

	<div class="bookmarklet">
		<a href="${cgi.escape(self.bookmarklet)}" class="pseudobutton" title="Get peeep link" 
			onclick="window.alert('Drag this link to your bookmark bar'); return false">
			<img src="/assets/bookmarklet.png" width="139" height="39" alt="Get peeep link"/>
		</a>

		<div>Drag this button to your
			Bookmarks toolbar.
			<a href="/pages/howto">Detailed instructions</a></div>
	</div> <!-- .bookmarklet -->

	<p>Peeep can help if you want to share a link that is 
	normally viewable only by you (it may be a resource requiring 
	sign-up, a private profile on a social network or 
	just any publicly inaccessible page). Just use the 
	bookmarklet to send the page to Peeep and share the 
	resulting link.</p>

</div> <!-- .section -->
	
<div id="personal" class="pers pbl">
<div class="pers pbr"><div class="pers ptl"><div class="pers ptr">

	<div class="login">
		${{ 
			if user is None: self.anonymous_template(vars())
			else: self.loggedin_template(vars())
		}}\n
	</div>

</div></div></div></div> <!-- #personal -->
'''
	loggedin_template = u'''<b><a href="/my">Your pages</a></b>
		${user.email()} (<a href=${xml.sax.saxutils.quoteattr(users.create_logout_url('/'))}>logout</a>)'''
	anonymous_template = u'''<b><a href=${xml.sax.saxutils.quoteattr(users.create_login_url('/'))}>Login</a></b>
		using your <a href="https://www.google.com/accounts/NewAccount">Google account</a>'''

if __name__ == "__main__":
	main()
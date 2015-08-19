import template

html = '''<p>This statement applies to the following data collected through the <a href="http://www.peeep.us">peeep.us</a> website.</p>
<h2 class="first">Scope</h2>
<ul>
<li>Peeep.us collects the addresses and cookies you entered and/or sent to peeep.us website.</li>
<li>Peeep.us uses Google Authentication mechanism to allow you to login at peeep.us. It stores your user identifier. It doesn't store any other personal information like email or password.</li>
</ul>

<h2>Uses</h2>
<ul>
<li>Peeep.us uses Google services to store collected data and offer you the service. Thus your data is shared with Google. <a href="http://www.google.com/privacy.html">Google rules</a> apply.</li>
<li>The user authentication is provided by Google. See <a href="http://www.google.com/privacy.html">Google privacy policy</a> to see the rules applied by them.</li>
<li>Peeep.us uses cookies you provided solely to authentificate requests to the URL you entered.</li>
<li>The cookie data you provided, your email, user id is not shared with any other third parties.</li>
<li>Peeep.us doen't provide a way to get a list of addresses it stores (with one exception. You can view a list of addresses you entered yourself).</li>
<li>Peeep.us doen't provide a way to view a stored page without knowing its exact identifier (http://www.peeep.us/XXXXXX).</li>
</ul>'''

def main():
	print template.render("Privacy rules", html, tagline='<a href="/">peeep</a>')

if __name__ == "__main__":
	main()
import template
from google.appengine.api import users

def main():
	print render();
	
	
def render():
	html = u'''\n\t<form method="post" id="upload" action="/upload.php" enctype=""application/x-www-form-urlencoded" accept-charset="utf-8">
		<div id="url_line">
			<input type="text" name="r_url" value="http://" />
			<button type="submit">Submit</button>
		</div>
		<div id="cookie">
			<label for="r_cookie">Cookie: </label> <input type="text" name="r_cookie" id="r_cookie" size="40" />
			<a href="#" title="Include authorization info..."
				onclick="var e=document.getElementById('cookie');e.className=e.className=='hide'?'':'hide';return false"
				class="js">Add cookie</a>
			<script type="text/javascript">document.getElementById('cookie').className = 'hide';</script>
		</div>
	</form>
	
	<div class="info">
	</div>\n\n'''
	
	return template.render("ppeepp", html, tagline="smart url shortener")

if __name__ == "__main__":
	main()
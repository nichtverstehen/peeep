# -*- coding utf8 -*-

from string import Template

def render(title, content, head = None, tagline = None):
	t = Template(u'Content-type: text/html;charset=utf-8\r\n\r\n'+
	
u'''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>$title</title>
	<link rel="Shortcut Icon" href="/favicon.ico" type="image/x-icon" /> 
	<link rel="stylesheet" type="text/css" href="/assets/style.css?3" />
	<!--[if lt IE 8]><link rel="stylesheet" type="text/css" href="/assets/ie.css?1" /><![endif]-->
	$head
</head>
<body>

<div class="header">
	<h1>$title</h1>
	
	<ul class="menu">
		<li><a>About</a></li>
	</ul>
</div>

<div id="doc" class="sh bl">
<div class="sh br"><div class="sh tl"><div class="sh tr">

$content

</div></div></div></div> <!-- #doc -->

<div class="footer">
© 2009, <a href="mailto:cyril7@gmail.com">Cyril Nikolaev</a>.
Icons by <a href="http://pinvoke.com">pinvoke</a>.
<div> <!-- .footer -->

<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-836471-6");
pageTracker._trackPageview();
} catch(err) {}</script>

</body>
</html>''')

	html = t.safe_substitute({
		'title': title, 
		'head': head if head is not None else '',
		'content': content
	})
	
	return html.encode('utf-8')
	
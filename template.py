# -*- coding utf8 -*-

from string import Template

def render(title, content, head = None, tagline = None):
	t = Template(u'Content-type: text/html;charset=utf-8\r\n\r\n'+
	
u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>$title</title>
	<link rel="Shortcut Icon" href="/favicon.ico" type="image/x-icon" /> 
	<link rel="stylesheet" type="text/css" href="/assets/style.css" />
	$head
</head>
<body>

<div id="doc">
<div class="box"><div class="box2">

<div class="tagline">$tagline</div>
<h1>$title</h1>

$content

</div> <!-- .box2 -->
</div> <!-- .box -->

</div> <!-- #doc -->

<div class="footer">
© 2009, <a href="http://nichtverstehen.de">Cyril Nikolaev</a>.
Favicon by <a href="http://pinvoke.com">pinvoke</a>.
</div> <!-- .footer -->

</body>
</html>''')

	html = t.safe_substitute({
		'title': title, 
		'head': head if head is not None else '', 
		'tagline': tagline if tagline is not None else '',
		'content': content
	})
	
	return html.encode('utf-8')
	
# -*- coding utf8 -*-

import templet
import statics_core

class PeeepTemplate(templet.UnicodeTemplate, statics_core.StaticsMixin): 
	h1 = 'Peeep.us'
	title_template = 'Peeep.us'
	index = False
	head_template = u''
	http_headers = u''
	content_template = 'Not found'
	template = (u'Content-type: text/html;charset=utf-8\r\n${self.http_headers}\r\n'+
	
u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>$<title_template></title>
	<link rel="Shortcut Icon" href="/favicon.ico" type="image/x-icon" /> 
	<link rel="stylesheet" type="text/css" href="/assets/style.css?7" />
	<!--[if lt IE 8]><link rel="stylesheet" type="text/css" href="/assets/ie.css?1" /><![endif]-->
	$<head_template>
	
</head>
<body>

<div class="header">
	<h1>${ self.h1 if self.index else '<a href="/">'+self.h1+'</a>' }</h1>
	
	<ul class="menu">
		${{ self.statics_template(vars(), category='main') }}
	</ul>
</div>

<div id="doc" class="sh sbl">
<div class="sh sbr"><div class="sh stl"><div class="sh str">

$<content_template>

</div></div></div></div> <!-- #doc -->

<div class="footer">
	© 2009, Cyril Nikolaev.
	Icons by <a href="http://pinvoke.com">pinvoke</a>.
</div> <!-- .footer -->

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

	def utf8(self):
		return unicode(self).encode('utf-8')

class ErrorTemplate(PeeepTemplate): 
	title_template = '$title'
	content_template = u'''<h2>$title</h2>\n<p>$text</p>'''
	
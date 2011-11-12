# -*- coding utf8 -*-
import core

STATICS = {
	'faq': {
		'title': 'Frequently Asked Questions',
		'short': 'FAQ',
		'category': 'main',
		'body': '''
<dl>
	<dt>What is Peeep and why should I use it?</dt>
	<dd><p>When you see a page that can soon change and you want to make a copy of current content,
		Peeep is here to help you to easily store web page.</p>
		<p>Another use case of Peeep is to share pages, unavailable for public views.
		For example you can store a private page on a social network,
		a view of some administrative web application, page from a resource requiring sign-up 
		or subscription. You can publish a link to that page on Peeep securely. Peeep stores only one 
		page and blocks all active components that could be used to disclose more personal information
		than it is presented on the particular page.
		</p></dd>
		
	<dt>How do I store current page content on Peeep?</dt>
	<dd><p>Given the page is publicly available just enter its URL and hit submit. 
		You will be automatically redirected to the copy of your page.</p>
		<p>Note that it is highly recommended that you log in. Only data submitted by
		authenticated users can be removed form Peeep.</p></dd>
	
	<dt>How do I share a private page?</dt>
	<dd><p>Install the bookmarklet (<a href="/pages/howto">Instructions here</a>). Navigate to the
		page you are going to share and click Get peeep link bookmarklet on your browser toolbar.
		You will be automatically redirected to the copy of your page.</p>
		<p>Note that it is highly recommended that you log in. Only data submitted by
		authenticated users can be removed from Peeep.</p></dd>
		
	<dt>How do I remove my data from Peeep?</dt>
	<dd><p>You can remove pages that you have saved to Peeep. Just log in using the account
		you used to submit pages and navigate to <a href="/my">Your pages</a>. Use red cross
		near a link to remove it.</p>
		<p>Note that you will not be able to remove a page you sent to Peeep anonymously.</p></dd>
		
	<dt>Why would I want to log in?</dt>
	<dd><p>Only pages stored by authenticated users can be removed from Peeep.</p></dd>
		
	<dt>How long will Peeep keep my data?</dt>
		<dd><p>Virtually forever. Nevertheless, we retain a right to remove content which 
		has not been accessed for a month.</p></dd>
		
	<dt>How can I contact you?</dt>
		<dd><p>If you have questions, offers or bug reports send email to
		<a href="mailto:support@peeep.us">support@peeep.us</a>.</p></dd>
</dl>
''',
	},
	'howto': {
		'title': 'How to install bookmarklet',
		'short': 'Install bookmarklet',
		'body': u'''
<div class="section">
<h3>Mozilla Firefox</h3>
<ol>
	<li>Make sure the <strong>Bookmarks toolbar</strong> is visible (use <strong>View ⇢ Toolbars ⇢ Bookmarks Toolbar</strong> to show it)</li>
	<li>Drag this link: <strong>%(bm)s</strong> to the toolbar</li>
</ol>
<div class="bigfigure">
	<img src="/assets/figures/ff_bm.png" alt="Install bookmarklet in Firefox" />
</div>
</div>

<div class="section">
<h3>Internet Explorer</h3>
<ol>
	<li>Make sure the <strong>Links</strong> (Favorites in IE 8) toolbar is visible (right click any part of menu bar and check <strong>Links</strong> to show it)</li>
	<li>Right-click this link: <strong>%(bm)s</strong> and click <strong>Add to Favorites</strong>.</li>
	<li>Internet Explorer will warn you, that you are installing an active (javascript) bookmark. Ignore this warning.</li>
	<li>Choose <strong>Links</strong> (Favorites) folder to save your bookmark so that it appears in the toolbar</li>
</ol>
<div class="bigfigure">
	<img src="/assets/figures/ie_bm.png" alt="Install bookmarklet in IE" />
</div>
</div>

<div class="section">
<h3>Safari</h3>
<ol>
	<li>Make sure the <strong>Bookmarks bar</strong> is visible (use <strong>View ⇢ Show Bookmarks Bar</strong> to show it)</li>
	<li>Drag this link: <strong>%(bm)s</strong> to the toolbar</li>
</ol>
<div class="bigfigure">
	<img src="/assets/figures/saf_bm.png" alt="Install bookmarklet in Safari" />
</div>
</div>

<div class="section">
<h3>Opera</h3>
<ol>
	<li>Make sure the <strong>Personal bar</strong> is visible (use <strong>View ⇢ Toolbars ⇢ Personal Bar</strong> to show it).</li>
	<li>Drag this link: <strong>%(bm)s</strong> to the toolbar. You may need to hold <strong>Ctrl</strong> key to drop the button.</li>
</ol>
<div class="bigfigure">
	<img src="/assets/figures/opera_bm.png" alt="Install bookmarklet in Opera" />
</div>
</div>

<div class="section">
<h3>Google Chrome</h3>
<ol>
	<li>Make sure the <strong>Bookmarks bar</strong> is visible (use <strong>Ctrl+B</strong> to show it).</li>
	<li>Drag this link: <strong>%(bm)s</strong> to the toolbar.</li>
</ol>
<div class="bigfigure">
	<img src="/assets/figures/chrome_bm.png" alt="Install bookmarklet in Opera" />
</div>
</div>
<p></p>
		''' % {'bm': core.getBookmarklet(html=True) },
	},
}

		
class StaticsMixin(object):
	def staticlink_template(self, args={}, *a, **kw):
		for i, v in args.iteritems():
			if i not in kw: kw[i] = v
		slug, page, current_slug = kw.get('slug'), kw.get('page'), kw.get('static_slug') # or None
		
		href = ''
		if slug != current_slug:
			 href = ' href="/pages/%s"'%slug
		self.write('\t\t<li><a%s>%s</a></li>\n' % (href, page['short']))
	
	def statics_template(self, args, *a, **kw):
		for i, v in args.iteritems():
			if i not in kw: kw[i] = v
		category = kw.get('category')
		
		for slug, page in STATICS.iteritems():
			if not category is None and page.get('category') != category:
				continue
			self.staticlink_template(kw, slug=slug, page=page)
			

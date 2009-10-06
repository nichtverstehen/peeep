import os, re

import template, e404
from statics_core import *
from core import NotFound

def main():
	try:
		path = os.environ['PATH_INFO']
		match = re.match("^/pages/(\w+)/?$", path)
		if match is None: raise NotFound
		
		slug = match.group(1)
		if slug not in STATICS: raise NotFound
			
		page = STATICS[slug]
		
		print StaticTemplate(page=page, static_slug=slug)
		
	except NotFound:
		e404.main()
			
	
class StaticTemplate(template.PeeepTemplate):
	title_template = "${page['title']}"
	content_template = "<h2>${page['title']}</h2>\n\n${page['body']}"
			
if __name__ == "__main__":
	main()
			
		
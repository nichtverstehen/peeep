import template

def main():
	print NotFoundTemplate().utf8()
	
class NotFoundTemplate(template.ErrorTemplate):
	http_headers = 'Status: 404 Not Found'
	def template(self, *args, **kwargs):
		if 'title' not in kwargs:
			kwargs['title'] = "Not found"
		if 'text' not in kwargs:
			kwargs['text'] = "The requested page was not found."
		super(NotFoundTemplate, self).template(*args, **kwargs)
	
if __name__ == "__main__":
	main()
from google.appengine.ext import db

class Page(db.Model):
	url = db.TextProperty(required=True)
	date = db.DateTimeProperty(auto_now_add=True, required=True)
	public = db.IntegerProperty(required=True, default=1)
	owner = db.UserProperty(auto_current_user_add=True)
	
class Cache(db.Model):
	page = db.ReferenceProperty(Page, required=True)
	url = db.StringProperty(required=True) # hash
	content = db.BlobProperty(required=True)
	contentType = db.StringProperty()
	date = db.DateTimeProperty(auto_now_add=True, required=True)
	
class Counter(db.Model):
	page = db.ReferenceProperty(Page, required=True)
	count = db.IntegerProperty(default=0, required=True)
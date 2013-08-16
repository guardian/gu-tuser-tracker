from google.appengine.ext import ndb

class Configuration(ndb.Model):
	key = ndb.StringProperty()
	value = ndb.StringProperty()

class TrackedUser(ndb.Model):
	username= ndb.StringProperty(required=True)

class TrackedUserSnapshot(ndb.Model):
	username=ndb.StringProperty(required=True)
	profile=ndb.TextProperty(required=True)
	when=ndb.DateTimeProperty(auto_now_add=True)

class Followers(ndb.Model):
	username=ndb.StringProperty(required=True)
	followers=ndb.IntegerProperty(required=True)
	when=ndb.DateTimeProperty(auto_now_add=True)

import webapp2
import jinja2
import os
import json
import logging
from urllib import quote, urlencode
from google.appengine.api import urlfetch

from models import TrackedUser, Followers

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('index.html')
		
		template_values = {}

		self.response.out.write(template.render(template_values))

class TrackedUserList(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('user-listing.html')

		template_values = {'tracked_users' : TrackedUser.query().order(TrackedUser.username)}

		self.response.out.write(template.render(template_values))

class UserDetails(webapp2.RequestHandler):
	def get(self, username):
		template = jinja_environment.get_template('user-data.html')

		template_values = {'follower_data' : Followers.query(Followers.username == username).order(-Followers.when)}

		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage),
	('/tracked-users', TrackedUserList),
	('/user/(.*)', UserDetails)],
                              debug=True)
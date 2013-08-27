import webapp2
import jinja2
import os
import json
import logging
import datetime
import csv
from StringIO import StringIO
from urllib import quote, urlencode
from google.appengine.api import urlfetch

from models import TrackedUser, Followers

import headers

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

		now = datetime.datetime.now()
		two_days_ago = now - datetime.timedelta(days=2)

		follower_data = [f for f in Followers.query(Followers.username == username, Followers.when >= two_days_ago).order(-Followers.when)]

		followers = [f.followers for f in follower_data]

		follower_change = max_followers = min_followers = 0
		if len(follower_data) > 1:
			follower_change = followers[0] - followers[-1]
			max_followers = max(followers)
			min_followers = min(followers)


		template_values = {'username' : username,
			'follower_data' : follower_data,
			'follower_change' : follower_change,
			'max_followers' : max_followers,
			'min_followers' : min_followers,}

		self.response.out.write(template.render(template_values))

class CsvDump(webapp2.RequestHandler):
	def get(self, username):
		follower_data = [f for f in Followers.query(Followers.username == username).order(-Followers.when)]

		headers.csv(self.response)
		buffer = StringIO()
		csv_writer = csv.writer(buffer)
		for f in follower_data:
			csv_writer.writerow([f.when.strftime("%Y-%m-%d %H:%M:%S"), f.followers])

		self.response.out.write(buffer.getvalue())

app = webapp2.WSGIApplication([('/', MainPage),
	('/tracked-users', TrackedUserList),
	('/user/(.*)/csv', CsvDump),
	('/user/(.*)', UserDetails)],
                              debug=True)
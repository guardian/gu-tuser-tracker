import webapp2
import jinja2
import os
import json
import logging
from urllib import quote, urlencode
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

from models import Configuration, TrackedUser, TrackedUserSnapshot, Followers
from configuration import lookup

import tweepy

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class ScraperTask(webapp2.RequestHandler):
	def get(self):
		consumer_key = lookup("t_consumer_key")
		consumer_secret = lookup("t_consumer_secret")
		access_token = lookup("t_access_token")
		access_token_secret =  lookup("t_access_token_secret")
		auth = tweepy.OAuthHandler( consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

		for tracked_user in TrackedUser.query():
			username=tracked_user.username

			try:
				user = api.get_user(screen_name=username)

				TrackedUserSnapshot(username=username, profile=json.dumps(user)).put()
				Followers(username=username, followers=user['followers_count']).put()
			except Exception, e:
				logging.fatal("Could not retreive data for %s" % username)
				logging.fatal(e)

	
		response = {"result" : "ok"}
		
		self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([('/tasks/scrape', ScraperTask)],
                              debug=True)
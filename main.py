# -*- coding: utf-8 -*-
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template

import os

from images.views import Thumbnailer

from games.views import SearchGames, AddGame
from movies.views import SearchMovies, AddMovie

from collection.views import NewCollection, ShowCollection
from collection.models import Collection

from users.models import User
from users.views import get_or_create_user

import logging

class MainPage(webapp.RequestHandler):
    def get(self):
        collections = None
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            user = get_or_create_user(users.get_current_user())
            collections = [db.get(key) for key in user.collections]
            collections = [[collection.name, collection.key().id()] for collection in collections]
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'logged': bool(users.get_current_user()),
            'collections': collections
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/collection/new', NewCollection),
                                      (r'/collection/(\d+)', ShowCollection),
                                      (r'/games/search/(.+)', SearchGames),
                                      (r'/movies/search/(.+)', SearchMovies),
                                      (r'/collection/(\d+)/games/new', AddGame),
                                      (r'/collection/(\d+)/movies/new', AddMovie),
                                      (r'/img/(\d+)', Thumbnailer)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
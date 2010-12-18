from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.db import Key

import os

import models
from users.views import get_or_create_user

class NewCollection(webapp.RequestHandler):
    def get(self):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))

        template_values = {}

        path = os.path.join(os.path.dirname(__file__), 'new_collection.html')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        collection = models.Collection()
        collection.name = self.request.get('nome')
        collection.users = [users.get_current_user()]
        collection.put()

        user = get_or_create_user(users.get_current_user())
        user.collections.append(collection.key())
        user.put()

        self.redirect('/')

class ShowCollection(webapp.RequestHandler):
    def get(self, idx):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))

        collection = db.get(Key.from_path('Collection', int(idx)))

        template_values = {'nome': collection.name}

        path = os.path.join(os.path.dirname(__file__), 'collection.html')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):
        collection = models.Collection()
        collection.name = self.request.get('nome')
        collection.users = [users.get_current_user()]
        collection.put()

        user = get_or_create_user(users.get_current_user())
        user.collections.append(collection.key())
        user.put()

        self.redirect('/')
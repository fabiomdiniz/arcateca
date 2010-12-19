# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template

import os

import models

def get_or_create_user(user):
    query = models.User.all()
    query.filter('user =', user)
    if query.count():
        return query.fetch(1)[0]
    else:
        output = models.User(user=user)
        output.put()
        return output
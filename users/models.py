# -*- coding: utf-8 -*-
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.db import Key
from collection.models import Collection

class User(db.Model):
    user = db.UserProperty()
    collections = db.ListProperty(Key)
from google.appengine.ext import db
from google.appengine.api import users

from images.models import Img

class Collection(db.Model):
    name = db.StringProperty(verbose_name='Nome')
    users = db.ListProperty(users.User)
    date = db.DateTimeProperty(auto_now_add=True)
from google.appengine.ext import db
from google.appengine.api import users

class Collection(db.Model):
    name = db.StringProperty(verbose_name='Nome')
    users = db.ListProperty(users.User)
    date = db.DateTimeProperty(auto_now_add=True)

class GameReg(db.Model):
    collection = db.ReferenceProperty(Collection)
    beated = db.BooleanProperty()

class Game(db.Model):
    name = db.StringProperty(verbose_name='Nome')
    platform = db.StringProperty(verbose_name='Plataforma')
    cover = db.BlobProperty()
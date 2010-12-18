from google.appengine.ext import db
from collection.models import Collection
from images.models import Img

class Game(db.Model):
    name = db.StringProperty(verbose_name='Nome')
    platform = db.StringProperty(verbose_name='Plataforma')
    cover = db.ReferenceProperty(Img)

class GameReg(db.Model):
    collection = db.ReferenceProperty(Collection)
    beated = db.BooleanProperty()
    game = db.ReferenceProperty(Game)
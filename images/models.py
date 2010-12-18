from google.appengine.ext import db

class Img(db.Model):
    url = db.StringProperty()
    data = db.BlobProperty()
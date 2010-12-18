from google.appengine.ext import db
from google.appengine.ext import webapp

class Thumbnailer(webapp.RequestHandler):
    def get(self, idx):
        img = db.get(db.Key.from_path('Img', int(idx)))
        self.response.headers['Content-Type'] = 'image/jpeg'
        self.response.out.write(img.data)

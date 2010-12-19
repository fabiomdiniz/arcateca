from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template

import os

import logging
import time

class bulkdelete(webapp.RequestHandler):
    def get(self, model):
        self.response.headers['Content-Type'] = 'text/plain'
        try:
            while True:
                q = db.GqlQuery('SELECT __key__ FROM ' + str(model))
                assert q.count()
                db.delete(q.fetch(200))
                time.sleep(0.5)
        except Exception, e:
            self.response.out.write(repr(e)+'\n')
            pass

application = webapp.WSGIApplication(
                                     [(r'/admin/bulkdelete/(.+)', bulkdelete)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
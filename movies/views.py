# -*- coding: utf-8 -*-
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.db import Key

import os

from users.views import get_or_create_user

from BeautifulSoup import BeautifulSoup
import urllib

import logging

from images.models import Img

from google.appengine.api import urlfetch

from models import Movie, MovieReg

from search.views import search_metacritic

class SearchMovies(webapp.RequestHandler):
    def get(self, name):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))

        results = search_metacritic(name, 'movie')

        output = []

        for result in results:
            query = Img.all()
            query.filter('url =', result[1])
            img = query.fetch(1)[0]
            query = Movie.all()
            query.filter('cover =', img)
            if not query.count():
                movie = Movie(name=str(result[0]),cover=img,score=str(result[2]))
                movie.put()
            else:
                movie = query.fetch(1)[0]
            output.append([img.key().id(), result[0], movie.key().id()])

        template_values = {'results': output}

        path = os.path.join(os.path.dirname(__file__), 'search.html')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):

        self.redirect('/')

class AddMovie(webapp.RequestHandler):
    def get(self, collection_id):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))

        template_values = {'collection':collection_id}

        path = os.path.join(os.path.dirname(__file__), 'new.html')
        self.response.out.write(template.render(path, template_values))
    
    def post(self, collection_id):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))

        collection = db.get(db.Key.from_path('Collection', int(collection_id)))
        
        logging.info(str(self.request.arguments()))

        checks = [arg for arg in self.request.arguments() if arg.find('watched') == -1 and arg.find('type') == -1]

        for check in checks:
            movie_id = int(check)
            watched = 'watched_'+str(check) in self.request.arguments()
            media_type = db.Category(self.request.get('type_'+str(check)))
            movie = db.get(db.Key.from_path('Movie', movie_id))
            movie_reg = MovieReg(movie=movie,collection=collection,watched=watched,media_type=media_type)
            movie_reg.put()

        template_values = {'collection':collection_id, 'msg':'Filmes adicionados com sucesso!'}

        path = os.path.join(os.path.dirname(__file__), 'new.html')
        self.response.out.write(template.render(path, template_values))
    
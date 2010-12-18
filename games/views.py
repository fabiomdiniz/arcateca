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

from models import Game, GameReg

from search.views import search_metacritic

class SearchGames(webapp.RequestHandler):
    def get(self, name):
        if not users.get_current_user():
            self.redirect(users.create_login_url(self.request.uri))

        results = search_metacritic(name, 'game')

        output = []

        for result in results:
            query = Img.all()
            query.filter('url =', result[1])
            img = query.fetch(1)[0]
            query = Game.all()
            query.filter('cover =', img)
            if not query.count():
                platform = str(result[1])[:str(result[1]).rfind('/')].replace('/game/','')
                game = Game(name=str(result[0]),cover=img,platform=platform)
                game.put()
            else:
                game = query.fetch(1)[0]
            output.append([img.key().id(), result[0], game.key().id()])

        template_values = {'results': output}

        path = os.path.join(os.path.dirname(__file__), 'search.html')
        self.response.out.write(template.render(path, template_values))
    
    def post(self):

        self.redirect('/')

class AddGame(webapp.RequestHandler):
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

        checks = [arg for arg in self.request.arguments() if arg.find('beated') == -1]

        for check in checks:
            game_id = int(check)
            beated = 'beated_'+str(check) in self.request.arguments()
            game = db.get(db.Key.from_path('Game', game_id))
            game_reg = GameReg(game=game,collection=collection,beated=beated)
            game_reg.put()

        template_values = {'collection':collection_id, 'msg':'Jogos adicionados com sucesso!'}

        path = os.path.join(os.path.dirname(__file__), 'new.html')
        self.response.out.write(template.render(path, template_values))
    
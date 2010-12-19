# -*- coding: utf-8 -*-
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.db import Key

import os
from BeautifulSoup import BeautifulSoup
import urllib

import logging

from images.models import Img

from google.appengine.api import urlfetch

def extract_img(url):
    try:
        soup = BeautifulSoup(urllib.urlopen('http://www.metacritic.com'+str(url)))
        logging.info('fetching '+str(url))
        return urlfetch.Fetch(soup('img', 'product_image large_image')[0].get('src')).content
    except:
        logging.info('http://www.metacritic.com'+str(url))
        if os.environ.get('HTTP_HOST'):
            url = os.environ['HTTP_HOST']
        else:
            url = os.environ['SERVER_NAME']
        logging.info('drawback: ' + 'http://' +  url + '/static/img/image_not_found.jpg')
        return urlfetch.Fetch('http://' + url + '/static/img/image_not_found.jpg').content
    

def extract_score(div):
    if len(div) == 5:
        return div.div.div('span')[1].string
    else:
        return 'XX'

def search_metacritic(name, tag):
    try:
        name = name.replace('%20','+')
        logging.info('iniciando fecth de ' + str(name))
        soup = BeautifulSoup(urlfetch.fetch('http://www.metacritic.com/search/' + str(tag) + '/' +str(name)+ '/results').content)

        divs = soup.findAll('div', attrs={'class':'main_stats'})

        results = [[divs[i].h3.a.string,divs[i].h3.a.get('href'),extract_score(divs[i])] for i in range(len(divs))]
        logging.info('coletando imagens')
        for result in results:
            query = Img.all()
            query.filter('url =', result[1])
            if not query.count():
                img = Img(data=db.Blob(extract_img(result[1])),
                          url=result[1])
                img.put()
        return results
    except Exception, e:
        logging.info('ERRO :' + str(e))
        return search_metacritic(name,tag)
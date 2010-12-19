# -*- coding: utf-8 -*-
from google.appengine.ext import db
from collection.models import Collection
from images.models import Img

class Movie(db.Model):
    name = db.StringProperty(verbose_name='Nome')
    cover = db.ReferenceProperty(Img)
    score = db.StringProperty()

class MovieReg(db.Model):
    collection = db.ReferenceProperty(Collection)
    media_type = db.CategoryProperty(verbose_name='Tipo de Mídia') #1 -DVD, 2-BD, 3-VHS
    movie = db.ReferenceProperty(Movie)
    watched = db.BooleanProperty()
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from apps.cocktails.models import Cocktail
from apps.tastes.models import Taste
from apps.ingredients.models import Spirit, Mixer, Ingredient

from scrapy_djangoitem import DjangoItem


class CocktailItem(DjangoItem):
    django_model = Cocktail

    description = scrapy.Field(default='No description')

class TasteItem(DjangoItem):
    django_model = Taste

class SpiritItem(DjangoItem):
    django_model = Spirit

class MixerItem(DjangoItem):
    django_model = Mixer

class IngredientItem(DjangoItem):
    django_model = Ingredient

    cocktail = scrapy.Field()
    liquid = scrapy.Field()
    kind = scrapy.Field()

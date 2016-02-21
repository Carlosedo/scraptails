# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from apps.cocktails.models import Cocktail

from scrapy_djangoitem import DjangoItem


class CocktailItem(DjangoItem):
    django_model = Cocktail
# class CocktailItem(scrapy.Item):

    # title = scrapy.Field()
    # mixing_instructions = scrapy.Field()
    description = scrapy.Field(default='No description')

    ingredients = scrapy.Field()
    scraped_tastes = scrapy.Field()
    # glass_type = scrapy.Field()
    # skill_level = scrapy.Field()

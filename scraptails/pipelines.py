# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from slugify import slugify

from apps.tastes.models import Taste
from apps.ingredients.models import Spirit, Mixer
from apps.cocktails.models import Cocktail

from .items import CocktailItem, TasteItem, SpiritItem, MixerItem, IngredientItem


class ScraptailsPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CocktailItem):
            return self.process_cocktail(item, spider)
        elif isinstance(item, TasteItem):
            return self.process_taste(item, spider)
        elif isinstance(item, SpiritItem):
            return self.process_spirit(item, spider)
        elif isinstance(item, MixerItem):
            return self.process_mixer(item, spider)
        elif isinstance(item, IngredientItem):
            return self.process_ingredient(item, spider)
        else:
            return item

    def process_cocktail(self, item, spider):
        item['title'] = item['title'].replace('Absolut ', '')
        item['description'] = item['description'].replace('Absolut Vodka', 'Vodka')
        item['taste_list'] = ','.join(item['taste_list'])

        item.save()

    def process_taste(self, item, spider):
        item.save()

    def process_spirit(self, item, spider):
        if 'Absolut' in item['name']:
            item['name'] = 'Vodka'

        item.save()

    def process_mixer(self, item, spider):
        item.save()

    def process_ingredient(self, item, spider):
        cocktail = Cocktail.objects.get(slug=slugify(item['cocktail'].replace('Absolut ', '')))
        item['cocktail'] = cocktail

        if item['kind'] == 'spirit':
            if 'Absolut' in item['liquid']:
                item['liquid'] = 'Vodka'
            try:
                spirit = Spirit.objects.get(slug=slugify(item['liquid']))
            except:
                import ipdb; ipdb.set_trace()
            item['spirit'] = spirit
        else:
            mixer = Mixer.objects.get(slug=slugify(item['liquid']))
            item['mixer'] = mixer

        item.save()

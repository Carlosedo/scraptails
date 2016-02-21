# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScraptailsPipeline(object):
    def process_item(self, item, spider):
        return item

class CocktailPipeline(object):
    def process_item(self, item, spider):
        item['title'] = item['title'].replace('Absolut ', '')

        for ingredient in item['ingredients']:
            if 'Absolut' in ingredient['ingredient']:
                ingredient['ingredient'] = 'Vodka'

        item['description'] = item['description'].replace('Absolut Vodka', 'Vodka')

        item.save()
        return item

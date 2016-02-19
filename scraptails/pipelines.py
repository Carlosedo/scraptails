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
#         tastes = item['tastes']
#         item['tastes'] = []

#         for taste in tastes:

#         item['tastes'] = Category.objects.get(id=2)
        # item.save()
        return item

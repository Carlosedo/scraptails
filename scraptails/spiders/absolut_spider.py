# -*- coding: utf-8 -*-

import scrapy

from scraptails.items import CocktailItem, SpiritItem, MixerItem, TasteItem, IngredientItem

class AbsolutSpider(scrapy.Spider):
    name = "absolut"
    allowed_domains = ["absolutdrinks.com"]
    start_urls = ["http://www.absolutdrinks.com/en/drinks/"]
    # start_urls = ["http://www.absolutdrinks.com/en/drinks/anejo-highball/"]

    def parse(self, response):
        for page in range(1):
            url = 'http://www.absolutdrinks.com/en/drinks/?pageNumber={page}'.format(
                page=page
            )
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        for href in response.css("div.grid.drink-list > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        cocktail = CocktailItem()

        cocktail_name = response.xpath('//h1[@class="heading"]/text()').extract_first()

        cocktail['title'] = cocktail_name
        cocktail['mixing_instructions'] = response.xpath('//div[@itemprop="recipeInstructions"]/p/text()').extract_first(default='')
        cocktail['description'] = response.xpath('//div[@class="text-content"]/p/text()').extract_first(default='')

        extra_contents = response.xpath('//div[@class="hide-mobile"]/h4')
        cocktail['glass_type'] = extra_contents[0].xpath('span/a/text()').extract_first(default='')
        cocktail['skill_level'] = extra_contents[2].xpath('span/a/text()').extract_first(default='')
        cocktail['taste_list'] = extra_contents[1].xpath('span/a/text()').extract()

        for scraped_taste in cocktail['taste_list']:
            taste = TasteItem()
            taste['title'] = scraped_taste
            yield taste

        yield cocktail

        ingredients = response.xpath('//ul[@class="ingredient"]/li')

        for ingredient in ingredients:
            ingredient_kind = None
            ingredient_name = ingredient.xpath('a/text()').extract_first()
            measure = ingredient.xpath('text()').extract_first()

            # Some ingredients don't have measures (eg. Champagne)
            if not measure:
                ingredient_kind = 'mixer'
                mixer = MixerItem()
                mixer['name'] = ingredient_name
                yield mixer

            else:
                measure = measure.split(' ')

                if measure[1] in ['Part', 'Parts']:
                    ingredient_kind = 'spirit'
                    spirit = SpiritItem()
                    spirit['name'] = ingredient_name
                    yield spirit
                else:
                    ingredient_kind = 'mixer'
                    mixer = MixerItem()
                    mixer['name'] = ingredient_name
                    yield mixer

            ingredient = IngredientItem()
            ingredient['cocktail'] = cocktail_name

            if measure:
                ingredient['amount'] = measure[0]
                ingredient['measurement'] = measure[1]

            ingredient['liquid'] = ingredient_name
            ingredient['kind'] = ingredient_kind

            yield ingredient

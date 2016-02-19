import scrapy

from scraptails.items import CocktailItem

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
        item = CocktailItem()

        item['title'] = response.xpath('//h1[@class="heading"]/text()').extract_first()
        item['mixing_instructions'] = response.xpath('//div[@itemprop="recipeInstructions"]/p/text()').extract_first(default='')
        item['description'] = response.xpath('//div[@class="text-content"]/p/text()').extract_first(default='')

        ingredients = response.xpath('//ul[@class="ingredient"]/li')
        item['ingredients'] = []

        for ingredient in ingredients:
            measure = ingredient.xpath('text()').extract_first().split(' ')
            item['ingredients'].append({
                'ingredient': ingredient.xpath('a/text()').extract_first(),
                'amount': measure[0],
                'measurement': measure[1]
            })

        extra_contents = response.xpath('//div[@class="hide-mobile"]/h4')
        item['glass_type'] = extra_contents[0].xpath('span/a/text()').extract_first(default='')
        item['scraped_tastes'] = extra_contents[1].xpath('span/a/text()').extract()
        item['skill_level'] = extra_contents[2].xpath('span/a/text()').extract_first(default='')

        yield item

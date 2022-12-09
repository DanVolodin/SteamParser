# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderSteamItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    reviews_number = scrapy.Field()
    reviews_summary = scrapy.Field()
    rating_value = scrapy.Field()
    release_date = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    genres = scrapy.Field()
    initial_price = scrapy.Field()
    discounted_price = scrapy.Field()
    discount = scrapy.Field()
    available_platforms = scrapy.Field()



# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyNbaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsItem(scrapy.Item):
    title = scrapy.Field()
    introduction = scrapy.Field()
    news_id = scrapy.Field()
    url = scrapy.Field() 

class ContentItem(scrapy.Item):
    title = scrapy.Field()
    news_id = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class postItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    create_time = scrapy.Field()
    source = scrapy.Field()
    source_link = scrapy.Field()
    desc = scrapy.Field()
    tag = scrapy.Field()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExtractjokeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class QiuShiItem(scrapy.Item):
    content = scrapy.Field()
    pic_url = scrapy.Field()
    rank_number = scrapy.Field()

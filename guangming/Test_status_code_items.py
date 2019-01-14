# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Items(scrapy.Item):
    type = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    status_code = scrapy.Field()
    # if_url_xpath = scrapy.Field()


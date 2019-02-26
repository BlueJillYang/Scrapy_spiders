# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DateItemApp(scrapy.Item):
    # medianame是发布人，type是类型，比如news、forum、blog、newspaper，viewcount浏览数，replys回复数，area地区，abstract概要，channel填 app
    title = scrapy.Field()
    url = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pubtime = scrapy.Field()
    type = scrapy.Field()
    keywords = scrapy.Field()
    medianame=scrapy.Field()
    viewcount =scrapy.Field()
    replys = scrapy.Field()
    collecttime = scrapy.Field()
    area = scrapy.Field()
    abstract = scrapy.Field()
    favicon = scrapy.Field()
    channel = scrapy.Field()


class DataItem(scrapy.Item):
    title = scrapy.Field()  #标题
    url = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    pubtime = scrapy.Field()
    type = scrapy.Field()
    keywords = scrapy.Field()
    medianame=scrapy.Field()
    viewcount =scrapy.Field()
    replys = scrapy.Field()
    collecttime = scrapy.Field()
    area = scrapy.Field()
    abstract = scrapy.Field()
    favicon = scrapy.Field()
    channel = scrapy.Field()
    spidername = scrapy.Field()
    author=scrapy.Field()
    file_urls = scrapy.Field()
    passed = scrapy.Field()


class JobItem(scrapy.Item):
    job_name = scrapy.Field()
    url = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    desc = scrapy.Field()
    pubtime = scrapy.Field()
    education = scrapy.Field()



#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'cwq'
import re
import time
import sys
import scrapy
import json
import redis
import urllib
import requests
import urlparse
from scrapy.http import Request
import datetime
from scrapy import Selector
from scrapy.http import FormRequest
from scrapy.utils.response import get_base_url
from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime,create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class jsyzglzfcgw(scrapy.Spider):
    name = "jsyzglzfcgw"
    start_urls = [
        "http://www.glcgw.gov.cn/news.asp?bigclassname=%B2%C9%B9%BA%B9%AB%B8%E6&mykeys=&smallclassname=&page=1 PN",
        "http://www.glcgw.gov.cn/news.asp?bigclassname=%D6%D0%B1%EA(%B3%C9%BD%BB)%B9%AB%B8%E6&mykeys=&smallclassname=&page=1 RN"
    ]
    Debug = True
    doredis = True
    source = u"广陵区政府招标采购网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"DOWNLOAD_TIMEOUT": 15.0, "DOWNLOAD_DELAY": 0.25}

    def __init__(self, start_url=None,history=False):
        super(jsyzglzfcgw, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True,"page_index":"1"},headers=self.headers,callback=self.parse_link)

    def parse_link(self, response):
        items = response.xpath("//td[@valign='center']/a/../..")

        for index,item in enumerate(items):
            url = item.xpath("./td/a/@href").extract()[0]
            final = urlparse.urljoin(response.url, url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            pubtime = item.xpath("./td/font/text()").extract()[0].strip()
            yield Request(url=final,method='get',headers=self.headers,
                          meta={"ba_type": response.meta["ba_type"], "page_index": response.meta["page_index"],"pubtime":pubtime}, callback=self.parse_item)

        if response.meta["page_parse"]:
            lastPage = response.xpath("//div[@align='right']/strong/text()").extract()[0].strip()
            page = lastPage.replace("/","")
            if self.history and int(page)>1:
                for i in range(2,int(page)+1):
                    url = response.url.replace("page=1","page="+str(i))
                    yield Request(url=url,method='get',headers=self.headers,
                                  meta={"ba_type": response.meta["ba_type"], "page_parse": False, "page_index": str(i)}, callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item['pubtime'] = datetime.datetime.strptime(response.meta["pubtime"], "%Y-%m-%d").strftime("%Y-%m-%d %H:%M")
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省扬州市广陵区'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath("//div[@id='article']/table[1]//td/text()").extract()[0].strip()
        item['content']= response.xpath("//div[@id='article']/table[2]").extract()[0]
        if u'更正' in item["title"] or u'补充' in item['title']:
            item["type"] = "CN"
        if item['pubtime'] and item['title'] and item['content']:
            yield item


#!/usr/bin/python
# -*- coding: utf-8 -*-
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


class jsnjnydx(scrapy.Spider):
    name = "jsnjnydx"
    start_urls = [
        "http://zbb.njau.edu.cn/pservices/index.jhtml PN",
        "http://zbb.njau.edu.cn/pgoods/index.jhtml PN",
        "http://zbb.njau.edu.cn/pprojects/index.jhtml PN",
        "http://zbb.njau.edu.cn/rservices/index.jhtml RN",
        "http://zbb.njau.edu.cn/rprojects/index.jhtml RN",
        "http://zbb.njau.edu.cn/rgoods/index.jhtml RN"
    ]
    Debug = True
    doredis = True
    source = u"南京农业大学招标网"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self,start_url=None,history=True):
        super(jsnjnydx, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

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
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        urls = response.xpath("//a[@title]/@href").extract()

        for index,url in enumerate(urls):
            final = urlparse.urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            yield Request(url=final,method='get',dont_filter=True,meta={"ba_type":response.meta["ba_type"]},callback=self.parse_item)

        lastPage = response.xpath("//div[@class='lpage']/div/text()").extract()[0]
        page = re.search("/(\d+)",lastPage)
        if page:
            page = page.group(1)
            if self.history and int(page)>1 and response.meta["page_parse"]:
                # for i in range(2,int(page)+1):
                for i in range(2,4):
                    url = response.url.replace("index","index_"+str(i))
                    yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()

        pubtime = response.xpath("//div[@class='info']/i[1]/text()").extract()[0]
        item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",pubtime).group(0) + " 00:00"
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省南京市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath("//h1/text()").extract()[0]
        item['content']= response.xpath("//div[@class='ccontent']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item


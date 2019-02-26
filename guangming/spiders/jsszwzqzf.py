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


class jsszwzqzf(scrapy.Spider):
    name = "jsszwzqzf"
    start_urls = [
        "http://www.szwz.gov.cn/zwgk/003018/003018003/1.html RN",
        "http://www.szwz.gov.cn/zwgk/003018/003018002/1.html PN"
    ]
    Debug = True
    doredis = True
    source = u"苏州市吴中区政府"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"DOWNLOAD_DELAY": 0.25}

    def __init__(self, start_url=None,history=True):
        super(jsszwzqzf, self).__init__()
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
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True,"page_index":"1"},callback=self.parse_link)

    def parse_link(self, response):
        urls = response.xpath("//ul[@class='ewb-info-items']/li/a/@href").extract()

        for index,url in enumerate(urls):
            final = urlparse.urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            yield Request(url=final,method='get',meta={"ba_type": response.meta["ba_type"], "page_index": response.meta["page_index"]}, callback=self.parse_item)

        if response.meta["page_parse"]:
            lastPage = response.xpath("//li[@id='pagetotal']/text()").extract()[0].strip()
            page = re.search(r"/(\d+)",lastPage).group(1)
            if self.history and int(page)>1:
                    for i in range(2,int(page)+1):
                        url = response.url.replace("/1.html","/"+str(i)+".html")
                        yield Request(url=url,method='get',meta={"ba_type": response.meta["ba_type"], "page_parse": False, "page_index": str(i)}, callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath("//div[@class='detailmessage']/text()[1]").extract()[0]
        pubtime = pubtime.replace("/","-")
        pubtime = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",pubtime).group(0)
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M")
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省苏州市吴中区'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath("//h1[@id='title']/text()").extract()[0].strip()
        item['content']= response.xpath("//div[@class='infoContent_info']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            # print response.meta["page_index"],item['title'],item["type"]
            yield item


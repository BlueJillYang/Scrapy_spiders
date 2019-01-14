#!/usr/bin/python
#-*- coding: utf-8 -*-import sys
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
# from scrapy import Selector
from scrapy.http import FormRequest
# from scrapy.utils.response import get_base_url
# from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler.configs.special_config import SpecialConfig
# from bc_crawler.sources.data_clean import create_pubtime,create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')

class chinanews(scrapy.Spider):
    name = "zgxw"
    start_urls = [

    ]
    Debug = True
    doredis = True
    source = u"中国新闻网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"DOWNLOAD_DELAY":1.0}
    totalCount = 0

    def __init__(self, start_url = None,history = True):
        super(chinanews, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
        # self.post_params.append({"url":self.start_urls[0].split()[0],"ba_type":self.start_urls[0].split()[1]})
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
            # formdata={"findInfo":"","typeId": "news34","auditingStatus":"1","isIndexFlg": "1","isPortal": "1","removedNewsId": "0","siteId": "-1","extType": "0","currentPage": "1"}
            # yield FormRequest(url=url,meta={"ba_type":"PN","page_index":"1"},method='post',formdata=formdata,callback=self.parse_link)
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"]},callback=self.parse_link)

    def parse_link(self, response):
        items = response.xpath("//a")
        # for index,item in enumerate(items):
        #     title = item.xpath("./text()").extract()[0]
            # final = urlparse.urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            # title = titles[index]
            # if self.check_title(title):
            #     yield Request(url=final,method='get',
            #                   meta={"ba_type":self.check_title(title),"page_index":response.meta["page_index"],"title":title},
            #                   callback=self.parse_item)

        # if self.history and response.meta["page_index"] == "1":
        #         lastPage = response.xpath("//tr[@class='listheadtd']/td/text()[1]").extract()[0]
              #  page = re.search(ur"共(\d+)页",lastPage).group(1)
                #if int(page) > 1:
                #    for i in range(2,int(page)+1):
                #        formdata={"findInfo":"","typeId": "news34","auditingStatus":"1","isIndexFlg": "1","isPortal": "1","removedNewsId": "0","siteId": "-1","extType": "0","currentPage": str(i)}
                 #       yield FormRequest(url=response.url,meta={"ba_type":"PN","page_index":str(i)},method='post',formdata=formdata,callback=self.parse_link)


    def parse_item(self, response):
        item=DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["medianame"] = response.meta["medianame"]
        item["type"] = response.meta["ba_type"]
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta["title"]
        item['content'] = response.xpath("//div[@class='content']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
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


class jsnjhwzbb(scrapy.Spider):
    name = "jsnjhwzbb"
    start_urls = [
        "http://www.njhwzbb.com/app/index/column/indexColumnBidAnnounce.html?currentCode=4100000&parentCode=102300&childCode=102320 PN",
        "http://www.njhwzbb.com/app/index/column/indexColumnBidAnnounce.html?currentCode=4100000&parentCode=102300&childCode=102340 PN",
        "http://www.njhwzbb.com/app/index/column/indexColumnBidAnnounce.html?currentCode=4100000&parentCode=102300&childCode=102431 RN"
    ]
    Debug = True
    doredis = True
    source = u"南京货物招标投标监督平台"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self,start_url=None,history=True):
        super(jsnjhwzbb, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            childCode = re.search(r"childCode=(.*)",channel["url"]).group(1)
            parentCode = re.search(r"parentCode=(.*?)&",channel["url"]).group(1)
            currentCode = re.search(r"currentCode=(.*?)&",channel["url"]).group(1)
            url = "http://www.njhwzbb.com/BidNewSupervisionAPI/api/Commtent/Announcements?currentCode="+str(childCode)+"&currentPage=1&operateType=all"

            yield Request(url=url,method='get',
                          meta={"ba_type":channel["ba_type"],"page_parse":True,"parentCode":parentCode,"childCode":childCode,"currentCode":currentCode},
                          callback=self.parse_link)

    def parse_link(self, response):
        body = json.loads(response.body)
        items = body["Data"]
        for index,item in enumerate(items):
            final = "http://www.njhwzbb.com/app/index/column/detail.html?"
            final += "currentCode="+response.meta["currentCode"]+"&parentCode="+response.meta["parentCode"]+"&childCode="+response.meta["childCode"]
            final += "&contentID="+item["DataKey"]
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            if "0001-01-01" in item["PublishDate"]:
                pass
            else:
                if "." in item["PublishDate"]:
                    pubtime = datetime.datetime.strptime(item["PublishDate"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M")
                else:
                    pubtime = datetime.datetime.strptime(item["PublishDate"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M")
                yield Request(url=final,method='get',
                          meta={"ba_type":response.meta["ba_type"],"title":item["TitleName"],"ContentText":item["ContentText"],"pubtime":pubtime},
                          callback=self.parse_item)

        page = int(body["TotalPage"])
        if self.history and int(page) > 1 and response.meta["page_parse"]:
            # for i in range(2,int(page)+1):
            for i in range(2,4):
                url = response.url.replace("currentPage=1","currentPage="+str(i))
                yield Request(url=url,method='get',
                              meta={"ba_type":response.meta["ba_type"],"page_parse":False,
                                    "parentCode":response.meta["parentCode"],"childCode":response.meta["childCode"],"currentCode":response.meta["currentCode"]},
                              callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()

        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省南京市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta["title"]
        item['content']= response.meta["ContentText"]

        if item['pubtime'] and item['title'] and item['content']:
            yield item


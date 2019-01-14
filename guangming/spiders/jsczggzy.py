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


class jsczggzy(scrapy.Spider):
    name = "jsczggzy"
    start_urls = [
        "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a 001001001 PN",
        "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a 001001005 RN",
        "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a 001001006 RN",
        "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a 001004002 PN",
        "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a 001004003 CN",
        "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a 001004006 RN",
        "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a 001005001 PN",
        "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a 001005003 RN",
        "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a 001006001 PN",
        "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a 001006003 RN",
    ]
    Debug = True
    doredis = True
    source = u"常州市公共资源网"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self, start_url = None,history = True):  #默认全采，非None非False只采第一页
        super(jsczggzy, self).__init__()
        jobs = self.start_urls
        # jobs = start_url.split('|')
        for job in jobs:
            self.post_params.append({"siteGuid":job.split()[0],"categorynum":job.split()[1],"ba_type":job.split()[2]})
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
            url = "http://58.216.50.99:8089/czggzyweb/jyxxAction.action?cmd=initPageCount"
            formdata={
                    "siteGuid": channel["siteGuid"],
                    "cityCode":"",
                    "type": "",
                    "categorynum": channel["categorynum"],
                    "title":""
                }
            yield FormRequest(url=url,meta={"ba_type":channel["ba_type"],"siteGuid":channel["siteGuid"],"categorynum":channel["categorynum"]},method='post',formdata=formdata,callback=self.parse_link)

    def parse_link(self, response):
        totalcounts = int(json.loads(response.body)["custom"])
        if totalcounts % 15 == 0:
            page = totalcounts / 15
        else:
            page = totalcounts / 15 + 1

        if page >= 1:
            for i in range(1,int(page)+1):
                if i >1 and not self.history:
                    break
                url = "http://58.216.50.99:8089/czggzyweb/jyxxAction.action?cmd=initPageList"
                formdata={
                    "pageIndex": str(i),
                    "pageSize": "15",
                    "siteGuid": response.meta["siteGuid"],
                    "cityCode": "" ,
                    "type": "",
                    "categorynum": response.meta["categorynum"],
                    "title": ""
                }
                yield FormRequest(url=url,meta={"ba_type":response.meta["ba_type"],"siteGuid":response.meta["siteGuid"]},method='post',formdata=formdata,callback=self.parse_get_json)

    def parse_get_json(self,response):
            urls = json.loads(json.loads(response.body)["custom"])["Table"]
            for index,url in enumerate(urls):
                pubtime = url["infodate"] + " 00:00"
                title = url["title"]
                infoid = url["infoid"]
                categorynum = url["categorynum"]
                url = "http://58.216.50.99:8089/czggzyweb/frontPageRedirctAction.action?cmd=pageRedirect"
                formdata={
                    "infoid": infoid,
                    "siteGuid": response.meta["siteGuid"],
                    "categorynum": categorynum
                }
                yield FormRequest(url=url,
                                  meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},
                                  method='post',formdata=formdata,callback=self.parse_redirect)

    def parse_redirect(self,response):
        url = json.loads(response.body)["custom"]
        final = urlparse.urljoin(response.url,url)
        # if self.doredis and self.expire_redis.exists(final):
        #     pass
        # else:
        yield Request(url=final,method='get',dont_filter=True,
                  meta={"ba_type":response.meta["ba_type"],"pubtime":response.meta["pubtime"],"title":response.meta["title"]},
                  callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()

        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省常州市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta["title"]
        item['content']= response.xpath("//div[@class='article']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item


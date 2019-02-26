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


class jsszgdjt(scrapy.Spider):
    name = "jsszgdjt"
    start_urls = [
        "http://www.sz-mtr.com/tender/notice/group/index.html PN",#招标-集团公司
        "http://www.sz-mtr.com/tender/notice/operation/index.html PN",#招标-分公司
        "http://www.sz-mtr.com/tender/notice/resource/index.html PN",#招标-资源开发分
        "http://www.sz-mtr.com/tender/notice/pm/index.html PN",#招标-物业公司
        "http://www.sz-mtr.com/tender/notice/S1/index.html PN",#招标-s1
        "http://www.sz-mtr.com/tender/result/group/index.html RN",#中标-集团公司
        "http://www.sz-mtr.com/tender/result/operation/index.html RN",#中标-分公司
        "http://www.sz-mtr.com/tender/result/resource/index.html RN",#中标-资源开发分
        "http://www.sz-mtr.com/tender/result/pm/index.html RN",#中标-物业公司
        "http://www.sz-mtr.com/tender/result/S1/index.html RN",#中标-s1
    ]
    Debug = True
    doredis = True
    source = u"苏州轨道交通"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def __init__(self, start_url=None, history=True):
        super(jsszgdjt, self).__init__()
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
        data_list = response.xpath('//ul[@class="mn-box-ul row"]/li[contains(@class, "-sm")]/a')
        if len(data_list) > 0:
            for index, data in enumerate(data_list):
                url = data.xpath('./@href').extract()[0]
                pubtime = data.xpath('./../div/text()').re('\d{4}-\d{2}-\d{2}')[0]
                title = data.xpath('./@title').extract()[0]
                final = urlparse.urljoin(response.url,url)
                # if self.doredis and self.expire_redis.exists(final):
                #     continue
                yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"],
                                                           "page_index":response.meta["page_index"],
                                                           "pubtime": pubtime, "title": title},callback=self.parse_item)

        if response.meta["page_parse"] and self.history:
            lastPage = re.search(r"createPageHTML\((\d+?),",response.body).group(1)
            page = int(lastPage)
            if self.history and int(page) > 1:
                for i in range(2,int(page)+1):
                    url = response.url.replace("index","index_"+str(i-1))
                    yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"page_parse":False,"page_index":str(i)},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省苏州市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath("//div[@class='txt_title1']/text()").extract() or \
                        response.xpath('//*[@id="tdTitle"]/h2/text()').extract()
        if len(item['title']) > 0:
            item['title'] = item['title'][0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        pubtime = response.meta['pubtime']
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M")
        content = response.xpath("//div[@class='txt1']").extract() or \
                         response.xpath('//*[@id="TDContent"]').extract()
        if len(content) > 0:
            item['content'] = content[0]
        else:
            raise Exception('{} content字段错误'.format(response.url))
        if u'变更' in item['title']:
            item["type"] = "CN"
        if item['pubtime'] and item['title'] and item['content']:
            print '页数:', response.meta["page_index"],item['title'],item["type"]
            yield item


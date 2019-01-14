#!/usr/bin/python
#-*- coding: utf-8 -*-import sys
import re
import time
import sys
import scrapy
import json
import redis
import random
import urllib
import requests
import urlparse
from scrapy import Selector
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import FormRequest
from scrapy.utils.response import get_base_url
from scrapy import signals
from urlparse import urljoin
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime,create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Zgbh(scrapy.Spider):
    name = "zgbh"
    start_urls = [
        'http://www.binhai.gov.cn/Article/ShowClass.asp?ClassID=202&page=1 PN',
        'http://www.binhai.gov.cn/Article/ShowClass.asp?ClassID=201&page=1 RN',
        'http://www.binhai.gov.cn/Article/ShowClass.asp?ClassID=200&page=1 PN',
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=False):
        super(Zgbh, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//td[@class="cl3"]/table[2]/tr[not(@style)]').extract()
        print len(data_list)
        # print data_listmeta
        for each in data_list[1:]:
            sel1 = Selector(text=each)
            url = sel1.xpath('//td[@class="news1424"]/a/@href').extract()[0]
            pubtime = sel1.xpath('//td[last()]/text()').re('\d+/\d+/\d+')[0].replace('/','-')
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            print url,  '  pubtime: ', pubtime
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            if response.xpath('//div[@class="show_page"]/b/text()').re('\d+'):
                count = int(response.xpath('//div[@class="show_page"]/b/text()').re('\d+')[0])
                page = count/20 if count/20 == 0 else count/20 + 1
                for i in range(2,int(page)+1):
                    page_url = response.url.replace('page=1','page='+str(i))
                    yield FormRequest(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市'
        item['source'] = u'中国滨海'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath('//td[@style="HEIGHT: 60px; TEXT-ALIGN: center"]/span/strong/text()').extract()[0]
        item['content'] = ''.join(response.xpath('/html/body/table[3]/tr/td[1]/table[1]/tr/td/table/tr[2]/td/table').extract())
        # print item
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

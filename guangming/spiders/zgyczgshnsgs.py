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


class Zgyczgshnsgs(scrapy.Spider):
    name = "zgyczgshnsgs"  # 中国烟草总公司湖南省公司
    start_urls = [
        'http://www.hntobacco.gov.cn/export/sites/mysite/zhewugongkai/jingyingguanli/zhaobiaocaigou/ PN',  # 招标公告
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=True):
        super(Zgyczgshnsgs, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        self.count = 0
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
        data_list = response.xpath('//div[@id="newsList31"]//td[@class="newsCalendar"]/a')
        # data_list = response.xpath('//td[@class="cl3"]/table[2]/tr[not(@style)]').extract()
        print len(data_list)
        # print data_listmeta
        for each in data_list:
            url = each.xpath('./@href').extract()[0]
            pubtime = each.xpath('./text()').re('\d+-\d+-\d+')[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            print url,  '  pubtime: ', pubtime
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            print '处理翻页'
            page_rule = response.xpath(u'//span[text()="下一页"]/ancestor::a/@href').extract()
            print page_rule
            if len(page_rule) > 0:
                page_url = urljoin(response.url, page_rule[0].strip())
                print page_url
                yield Request(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        self.count += 1
        print '处理了%d条'%self.count
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.xpath('//div[@class="title"]/text()').extract()[0]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'中国湖南省'
        item['source'] = u'中国烟草总公司湖南省公司'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = '//div[@class="richContent  richContent3"]'
        item['content'] = response.xpath(content).extract()[0]
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

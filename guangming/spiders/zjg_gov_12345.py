#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import re
import sys
import time
import traceback
import urllib
import urlparse
import codecs
import redis
import requests
import scrapy
# from SpeciSpiders.items import DataItem
# from bc_crawler.configs.special_config import SpecialConfig
from scrapy import Selector
from scrapy import signals
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.utils.response import get_base_url
# from scrapy.xlib.pydispatch import dispatcher
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Zjg_gov_12345(scrapy.Spider):
    name = "zjg_gov_12345"  # 张家港市便民服务网
    start_urls = [
        'http://www.zjg12345.com/zjgbmweb/ywxxtemplate/slgs.aspx news',
    ]
    Debug = True
    doredis = True
    source = u"张家港市便民服务网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Zjg_gov_12345, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)

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
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"]},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//a[contains(@onclick, "window.open")]')
        print len(data_list)
        if len(data_list) > 0:
            for data in data_list:
                url = data.xpath('./@onclick').extract()[0]
                title = data.xpath('./text()').extract()[0]
                url = re.search(r'window.open\("(.+?)"', url).group(1).strip()
                url = urlparse.urljoin(response.url, url)
                yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'title':title},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.xpath('//*[@id="CaseDetail_lbl_requestDate"]/text()').extract()[0].strip()
        item['pubtime'] = datetime.datetime.strptime(item['pubtime'].replace('/', '-'), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        title = response.xpath('//*[@id="CaseDetail_lbl_title"]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省苏州市张家港市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['medianame'] = u'张家港市便民服务网'
        item['url'] = response.url
        content = response.xpath('//*[@id="Table2"]').extract()
        item['content'] = content[0]
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



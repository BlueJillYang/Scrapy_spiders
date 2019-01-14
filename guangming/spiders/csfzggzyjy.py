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


class Csfzggzyjy(scrapy.Spider):
    name = "csfzggzyjy"
    start_urls = [
        'http://ggzy.csfzc.gov.cn/news?newsclass=50 RN',  # 10
        'http://ggzy.csfzc.gov.cn/news?newsclass=49 PN',  # 13
        'http://ggzy.csfzc.gov.cn/news?newsclass=45 RN',  # 73
        'http://ggzy.csfzc.gov.cn/news?newsclass=44 RN',  # 38
        'http://ggzy.csfzc.gov.cn/news?newsclass=43 RN',  # 216
        'http://ggzy.csfzc.gov.cn/news?newsclass=42 PN',  # 207
        'http://ggzy.csfzc.gov.cn/news?newsclass=41 PN',  # 50
        'http://ggzy.csfzc.gov.cn/news?newsclass=40 PN',  # 311
        # 理论918 实际918
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.5,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url=None,history=True):
        super(Csfzggzyjy, self).__init__()
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
        data_list = response.xpath('//div[@class="listnr"]/ul/li')
        for each in data_list:
            url = each.xpath('.//a/@href').extract()[0]
            pubtime = each.xpath('.//div[@class="date"]/text()').re('\d+-\d+-\d+')[0]
            title = ''.join(each.xpath('.//a//text()').extract())
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            if response.xpath('//div[@class="pageinfo"]/span[2]//text()'):
                page = response.xpath('//div[@class="pageinfo"]/span[2]//text()').extract()[0]
                for i in range(2,int(page)+1):
                    page_url = response.url+'&p='+str(i)
                    print '正在处理翻页{}'.format(page_url)
                    yield Request(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省常熟市'
        item['source'] = u'常熟服装城公共资源交易中心'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        item['content'] = ''.join(response.xpath('//div[@class="article"]').extract())
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

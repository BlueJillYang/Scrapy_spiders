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


class Hasggzy(scrapy.Spider):
    name = "hasggzy"  # 无更新
    start_urls = [
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003001/003001001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003001/003001002/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003001/003001003/ CN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003001/003001004/ CN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003001/003001005/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003001/003001006/ CN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003001/003001007/ CN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003001/003001008/ PF',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003002/003002001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003002/003002007/ PF',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003002/003002003/ CN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003002/003002006/ CN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003002/003002004/ CN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003002/003002005/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003004/003004001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003004/003004002/ CN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003004/003004004/ PF',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003004/003004005/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003004/003004003/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003010/003010001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003010/003010003/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003005/003005001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003005/003005002/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003006/003006001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003006/003006003/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003006/003006004/ PF',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003007/003007001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003007/003007002/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009001/003009001001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009001/003009001002/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009003/003009003001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009003/003009003002/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009004/003009004001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009004/003009004002/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009005/003009005001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009005/003009005002/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009006/003009006001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009006/003009006002/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009007/003009007001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009007/003009007002/ RN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009008/003009008001/ PN',
        'http://www.haztb.gov.cn/EpointWeb/jyxx/003009/003009008/003009008002/ RN',
    ]
    allow_domains = ["haztb.gov.cn"]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history = True):
        super(Hasggzy, self).__init__()
        jobs = self.start_urls
        # jobs = start_url.split('|')
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
        data_list = response.xpath('//ul[@class="menu-right-items"]/li').extract()
        for each in data_list:
            sel1 = Selector(text=each)
            url = sel1.xpath('//a/@href').extract()[0]
            pubtime = sel1.xpath('//span[@class="menu-date"]//text()').re('\d+-\d+-\d+')[0]
            title = ''.join(sel1.xpath('//a/text()').extract())
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            if response.xpath('//a[@class="wb-page-default wb-page-number wb-page-family"]/text()'):
                page = response.xpath('//a[@class="wb-page-default wb-page-number wb-page-family"]/text()').re('\d+/(\d+)')[0]
                for i in range(2,3):
                    page_url = response.url+'?Paging='+str(i)
                    yield FormRequest(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省淮安市'
        item['source'] = u'淮安市公共资源交易网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        item['content'] = ''.join(response.xpath('//div[@id="mainContent"]').extract())
        print item
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

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


class Gzzfcg(scrapy.Spider):
    name = "gzzfcg"  # 无更新
    start_urls = [
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=wsxjzb CN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=wsxj CN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=wsjjzb PN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=wsjj PN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=qtxjzb CN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=qtxj PN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=qtdwgg CN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=jzxzb CN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=jzxcsjggg RN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=jzxcs CN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=jzx PN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=jjgg RN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=gkzbzb PN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=gkzb PN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=dylyzb RN',
        'http://222.184.252.155:90/net/cgxx.jsp?page=1&opstatus=dyly PN',

    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url=None,history=True):
        super(Gzzfcg, self).__init__()
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
        data_list = response.xpath('//table/tr[@class="table_tr"]').extract()
        print len(data_list)
        for each in data_list:
            sel1 = Selector(text=each)
            url = sel1.xpath('//td[@class="cutText"]/a/@href').extract()[0]
            title = sel1.xpath('//td[@class="cutText"]/a/@title').extract()[0]
            pubtime = sel1.xpath('//td[last()]/text()').re('\d+-\d+-\d+')[0]
            url = urljoin(response.url,url)
            print url
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            print ''.join(response.xpath('//table[@id="__01"]/tr[2]/td/table/tr[last()]/td/text()').re(u'\d+页\/共(\d+)')[0])
            print '*'*20
            if response.xpath('//table[@id="__01"]/tr[2]/td/table/tr[last()]/td/text()').re(u'\d+页\/共(\d+)'):
                page = response.xpath('//table[@id="__01"]/tr[2]/td/table/tr[last()]/td/text()').re(u'\d+页\/共(\d+)')[0]
                for i in range(2,int(page)+1):
                    print response.url
                    page_url = response.url.replace('page=1','page='+str(i))
                    print page_url
                    yield FormRequest(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省南通市港闸区'
        item['source'] = u'港闸政府采购'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        item['content'] = ''.join(response.xpath('//table[@width="894"]').extract())
        print item
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

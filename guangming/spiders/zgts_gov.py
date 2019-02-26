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


class Zgts_gov(scrapy.Spider):
    name = "zgts_gov"  # 铜山网络发言人平台
    start_urls = [
        'http://fyr.zgts.gov.cn/services/common_new/news.aspx?type=3 news',
    ]
    Debug = True
    doredis = True
    source = u"铜山网络发言人平台"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}
    final = []

    def __init__(self,start_url=None):
        super(Zgts_gov, self).__init__()
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
        data_list = response.xpath('//*[@id="newlist"]//p/a')
        print 'len: ', len(data_list), response.url
        if len(data_list) > 0:
            for data in data_list:
                url = data.xpath('./@href').extract()[0]
                title = data.xpath('./text()').extract()[0]
                pubtime = data.xpath('./../../following-sibling::li[3]/font/text()').extract()[0].strip()
                url = urlparse.urljoin(response.url, url)
                self.final.append(url)
                print url, title,' list:',len(self.final), ' set:', len(set(self.final))
                yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'title':title,"pubtime":pubtime},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta['pubtime']
        item['pubtime'] = datetime.datetime.strptime(item['pubtime'].replace('/', '-'), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        title = response.xpath('//*[@id="CaseDetail_lbl_title"]/text()').extract() or \
                response.xpath('//div[@id="contitle"]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省徐州市铜山区'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['medianame'] = u'铜山网络发言人平台'
        item['url'] = response.url
        content = ''.join(response.xpath('//*[@class="w1003"]').extract())  # content分内容及回复内容
        quelist = ''.join(response.xpath('//ul[@class="quelist"]').extract())
        item['content'] = content + quelist
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



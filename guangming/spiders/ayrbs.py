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
from scrapy import Selector
from scrapy import signals
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.utils.response import get_base_url
# from SpeciSpiders.items import DataItem
# from bc_crawler.configs.special_config import SpecialConfig
# from scrapy.xlib.pydispatch import dispatcher
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Ayrbs(scrapy.Spider):
    name = "ayrbs"  # 安阳日报电子版 和 安阳少年报电子版
    start_urls = [
        'http://www.ayrbs.com/epaper/paperindex.htm newspaper',
        'http://www.ayrbs.com/aywb/paperindex.htm newspaper',
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None,history=True):
        super(Ayrbs, self).__init__()
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
            yield Request(url=url,method='get',meta={'ba_type':channel['ba_type'],'page_parse':True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//ul[@class="main-ed-articlenav-list"]/li[@id]/a')
        for data in data_list:
            url = data.xpath('./@href').extract()[0]
            title = data.xpath('./text()').extract()[0]
            url = urlparse.urljoin(response.url, url)
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'title':title},callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = response.xpath('//a[@id="pageLink"]/@href').extract()
            for page in page_rule:
                url = urlparse.urljoin(response.url, page)
                if url != response.url:
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'河南省安阳市'
        if 'aywb' in response.url:
            item['source'] = u'安阳少年报电子版'
            item['medianame'] = u'安阳少年报电子版'
        else:
            item['source'] = u"安阳日报电子版"
            item['medianame'] = u'安阳日报电子版'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        pubtime = response.xpath('/html/body/table//tr/td[4]/table[3]//tr/td/table//tr/td[2]/span[1]/span/text()').extract()[0].strip()
        item['pubtime'] = datetime.datetime.strptime(pubtime.replace(u'年', '-').replace(u'月', '-').replace(u'日', ''), "%Y-%m-%d").strftime('%Y-%m-%d %H:%M')
        title = response.xpath('//span[@class="biaoti_heiti"]/..//strong[1]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        content = response.xpath('//table[@class="detail_table"]').extract()
        item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



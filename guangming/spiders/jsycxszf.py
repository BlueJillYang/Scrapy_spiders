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


class jsycxszf(scrapy.Spider):
    name = "jsycxszf"
    start_urls = [
        'http://218.92.246.62:8090/zbtb/Class_44.html PN',  # 工程建设-招标公告
        'http://218.92.246.62:8090/zbtb/Class_45.html PN',  # 工程建设-最高限价
        'http://218.92.246.62:8090/zbtb/Class_46.html PN',  # 工程建设-中标公示
        'http://218.92.246.62:8090/zbtb/Class_48.html PN',  # 工程建设-招标答疑
        'http://218.92.246.62:8090/zbtb/Class_50.html PN',  # 政府采购-招标公告
        'http://218.92.246.62:8090/zbtb/Class_51.html CN',  # 政府采购-招标答疑
        'http://218.92.246.62:8090/zbtb/Class_52.html RN',  # 政府采购-中标公示
        'http://218.92.246.62:8090/zbtb/Class_55.html PN',  # 产权交易-招标公告
        'http://218.92.246.62:8090/zbtb/Class_56.html CN',  # 产权交易-招标答疑
        'http://218.92.246.62:8090/zbtb/Class_57.html RN',  # 产权交易-中标公示
    ]
    Debug = True
    doredis = True
    source = u"响水县政府"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False}

    def __init__(self,start_url=None,history=True):
        super(jsycxszf, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        self.history = history
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"], "page_parse": True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//ul[@class="yw-nr-ul"]/li/a')
        for index, data in enumerate(data_list):
            url = data.xpath('./@href').extract()[0]
            title = data.xpath('./@title').extract()[0]
            pubtime = data.xpath('./../span/text()').re('\d{4}-\d{2}-\d{2}')[0]
            final = urlparse.urljoin(response.url, url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            yield Request(url=final,method='get',meta={"ba_type": response.meta["ba_type"],
                          "pubtime": pubtime, "title": title},callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = re.search(r'totalPages: (\d+),', response.body)
            print page_rule
            if page_rule:
                page = page_rule.group(1)
                print page
                for i in range(2, int(page)+1):
                    final = response.url.replace('.html', '_{}.html'.format(i))
                    print final
                    yield Request(url=final, method='get', meta={"ba_type": response.meta["ba_type"],
                                                                 "page_parse": False}, callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()

        item["pubtime"] = response.meta["pubtime"] + ' 00:00'
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市响水县'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        item['content'] = response.xpath("//div[@class='main-txt']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item

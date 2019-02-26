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
import execjs
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


class Aygxq_gov(scrapy.Spider):
    name = "aygxq_gov"  # 安阳国家高新技术产业开发区
    start_urls = [
        'http://www.aygxq.gov.cn/channels/16.html news',
        'http://www.aygxq.gov.cn/channels/10.html news',
        'http://www.aygxq.gov.cn/channels/80.html news',
    ]
    Debug = True
    doredis = True
    source = u"安阳国家高新技术产业开发区"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Aygxq_gov, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.js_file = codecs.open('/home/python/Desktop/Test_spiders/guangming/guangming/spiders/aygxq_gov.js', 'r', encoding='utf-8')
        self.html_str = ''
        self.html_str = self.get_js()

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def get_js(self):
        line = self.js_file.readline()
        html_str = ''
        while line:
            html_str += line
            line = self.js_file.readline()
        return html_str

    def get_redirect_href(self, url):
        js_code = self.html_str
        ctx = execjs.compile(js_code)
        result = ctx.call('YunSuoAutoJump', url)
        return result

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            result = self.get_redirect_href(url)
            headers = {'Referer': 'http://www.aygxq.gov.cn/'}
            url = url + result['another_href'].replace('/', '')
            cookies = {'path': '/', 'srcurl': result['str_cookie']}
            yield Request(url=url,headers=headers,cookies=cookies,method='get',meta={'ba_type':channel['ba_type']},callback=self.re_direct)

    def re_direct(self, response):
        url = response.url
        # print url,'\n', response.body
        yield Request(url=url,method='get',dont_filter=True,meta={'ba_type':response.meta['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//ul[@class="main_other_list"]/li/a') or \
                    response.xpath('//div[@class="box_list"]//div/div/div/a')
        if len(data_list) == 0:
            yield Request(url=response.url,method='get',dont_filter=True,meta={'ba_type':response.meta['ba_type']},callback=self.parse_link)
        for data in data_list:
            url = data.xpath('./@href').extract()[0]
            pubtime = data.xpath('./../span/text()').extract() or data.xpath('./../following-sibling::div/text()').extract()
            pubtime = re.search(r'\d{4}-\d{1,2}-\d{1,2}', pubtime[0]).group()
            title = data.xpath('./text()').extract()[0].strip()
            url = urlparse.urljoin(response.url, url)
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime,'title':title},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'河南省安阳市高新区'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['medianame'] = u'安阳国家高新技术产业开发区'
        item['url'] = response.url
        pubtime = response.meta['pubtime']
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d").strftime('%Y-%m-%d %H:%M')
        title = response.xpath('//h2[@class="title"]/text()').extract() or \
                response.xpath('//*[@id="main_box"]/div[2]/div[2]/div[1]/div[1]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        content = response.xpath('//div[@class="content"]').extract() or \
                  response.xpath('//div[@id="main_box"]').extract()
        item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



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


class Ayxww(scrapy.Spider):
    name = "ayxww"  # 安阳新闻网
    start_urls = [
        'http://www.aynews.net.cn/vision/node_144.shtml news',
    ]
    source = u'安阳新闻网'
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.3,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Ayxww, self).__init__()
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
            yield Request(url=url,method='get',meta={'ba_type':channel['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//div[@class="Teletext_list"]/ul/li/a')
        for data in data_list:
            url = data.xpath('./@href').extract()[0]
            title = data.xpath('./h4/text()').extract()[0]
            url = urlparse.urljoin(response.url, url)
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'title':title},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'河南省安阳市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        pubtime = response.xpath('//div[@class="biaoti"]/div/text()').extract()[0].strip()
        medianame = re.search(ur'来源[:：]\s?(\S+)', pubtime)
        pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}', pubtime).group().strip()
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
        print 'medianame ', medianame, 'pubtime ', pubtime
        if medianame:
            item['medianame'] = medianame.group(1)
        else:
            item['medianame'] = u'安阳新闻网'
        title = ''.join(response.xpath('//div[@class="biaoti"]/h2/text()').extract())
        item['title'] = title.strip() or response.meta['title'].strip()
        content = response.xpath('//div[@class="page"]').extract()
        item['content'] = content[0]

        print response.status
        print item['url'], item['title'], item['pubtime']
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item['url']
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



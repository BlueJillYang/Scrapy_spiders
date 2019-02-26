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


class Tangyin_gov(scrapy.Spider):
    name = "tangyin_gov"  # 中国汤阴
    start_urls = [
        'http://www.tangyin.gov.cn/front/mailbox/tableData?category=0 news',
    ]
    source = u'中国汤阴'
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.3,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Tangyin_gov, self).__init__()
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
            formdata = {
                'order': 'asc',
                'limit': '20',
                'offset': '0',
                'title': '',
                'starttime': '',
                'endtime': '',
                'siteId': '8e1ea6fa17774eb7b7b3e54b723edc17',
            }
            yield FormRequest(url=url,formdata=formdata,meta={'ba_type':channel['ba_type'],'siteId':formdata['siteId']},callback=self.parse_link)

    def parse_link(self, response):
        result = json.loads(response.body)['rows']
        for info in result:
            url_id = info['id']
            title = info['title'].strip()
            pubtime = info['writeTime']
            url = 'http://www.tangyin.gov.cn/front/mailbox/mailbox?id={}&siteId={}'.format(url_id, response.meta['siteId'])
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime,'title':title},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'河南省安阳市汤阴县'
        item['source'] = self.source
        item['medianame'] = u'中国汤阴'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        pubtime = response.meta['pubtime']
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M')
        title = ''.join(response.xpath('//div[@class="biaoti"]/h2/text()').extract())
        item['title'] = title.strip() or response.meta['title'].strip()
        content = response.xpath('//div[@class="border_common"]/input/..').extract()
        item['content'] = content[0]

        print item['url'], item['title'], item['pubtime']
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item['url']
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



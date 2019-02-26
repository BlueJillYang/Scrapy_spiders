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


class Changzhou_gov_12345(scrapy.Spider):
    name = "changzhou_gov_12345"  # 常州市12345政府公共服务平台
    start_urls = [
        'http://58.216.242.45/gdsq/ news',  # 电话诉求
        'http://58.216.242.45/wssq/ news',  # 网上诉求
    ]
    Debug = True
    doredis = True
    source = u"常州市12345政府公共服务平台"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Changzhou_gov_12345, self).__init__()
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
        table_node = response.xpath('//table[@class="divtable"]').extract()[0]
        id_node = response.xpath('//table[@class="divtable"]//td[@id]/@id').extract()
        formdata = {'page': '1', 'len': '10'}
        if 'gdsq' in response.url:
            url = 'http://58.216.242.45/czweb/queryTelAllPage.do'
        else:
            url = 'http://58.216.242.45/czweb/queryWebAllPage.do'
        yield FormRequest(url=url,formdata=formdata,meta={'ba_type':response.meta['ba_type'],'table_node':table_node,
                                                          'id_node':id_node,'get_url':response.url},callback=self.parse_item)

    def parse_item(self, response):
        table_node = response.meta['table_node']
        id_node = response.meta['id_node']
        jsonDict = json.loads(response.body)['pc']['list']
        for info in jsonDict:
            item = DataItem()
            pubtime = info['return_time']
            title = info['title'].strip()

            # 拼接节点 content
            result = table_node
            for id_key in id_node:
                if id_key == u'readcount':
                    id_value = info['{}'.format('read_count')]
                elif id_key == u'form_status':
                    id_value = info['{}'.format('status')]
                else:
                    id_value = info['{}'.format(id_key)]
                if 'content' in id_key:
                    result = re.sub(r'(?P<text>id="{}".*?><div.*?>)'.format(id_key), r'\g<text>{}'.format(id_value), result)
                else:
                    result = re.sub(r'(?P<text>id="{}".*?>)'.format(id_key), r'\g<text>{}'.format(id_value), result)

            item['pubtime'] = datetime.datetime.strptime(pubtime.replace('/', '-'), "%Y-%m-%d").strftime("%Y-%m-%d %H:%M")
            item['title'] = title
            item["type"] = response.meta["ba_type"]
            item['area'] = u'江苏省常州市'
            item['source'] = self.source
            item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
            item['medianame'] = u'常州市12345政府公共服务平台'
            item['url'] = response.meta['get_url']
            item['content'] = result
            if item['pubtime'] and item['title'] and item['content']:
                yield item
            else:
                print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



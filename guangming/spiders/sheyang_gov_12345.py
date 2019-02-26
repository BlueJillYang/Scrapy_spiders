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


class Sheyang_gov_12345(scrapy.Spider):
    name = "sheyang_gov_12345"  # 射阳12345在线
    start_urls = [
        'http://sy12345.sheyang.gov.cn/list/index.html#0 news',
        'http://sy12345.sheyang.gov.cn/list/index.html#1 news',
        'http://sy12345.sheyang.gov.cn/list/index.html#2 news',
        'http://sy12345.sheyang.gov.cn/acceptance/show/ news',  # 诉求展示  2是post参数

    ]
    Debug = True
    doredis = True
    source = u"射阳12345在线"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Sheyang_gov_12345, self).__init__()
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
        post_param_dict = {'#0': u'新闻中心', '#1': u'通知公告', '#2': u'工作动态'}
        for channel in self.post_params:
            url = channel['url']
            if '#' in url:
                post_type = re.search(r'#\d', url).group()
                post_url = 'http://112.25.171.120:8044/api/webapi/news/getnewslist'
                formdata = {'newstypename': post_param_dict[post_type].encode('utf-8'), 'pageindex': '1', 'pagesize': '15'}
                get_url = 'http://sy12345.sheyang.gov.cn/news/index.html?id='
                real_url = 'http://112.25.171.120:8044/api/webapi/news/getnewsinfo'
            else:
                post_url = 'http://112.25.171.120:8044/api/webapi/appeal/insidelist'
                formdata = {'ordertype': '2', 'pageindex': '1', 'pagesize': '10'}
                get_url = 'http://sy12345.sheyang.gov.cn/acceptance/show/detail/index.html?id='
                real_url = 'http://112.25.171.120:8044/api/webapi/appeal/getappealdetail/'
            print formdata
            yield FormRequest(url=post_url,formdata=formdata,meta={"ba_type":channel["ba_type"],"get_url":get_url,"real_url":real_url},callback=self.parse_link)

    def parse_link(self, response):
        id_list = []
        result = re.findall(r'caseid=(\d+)', response.body)
        result1 = re.findall(r'newsid.(\d+)', response.body)
        if len(result) > 0:
            id_list = result
        elif len(result) == 0 and len(result1) > 0:
            id_list = result1
        if len(id_list) > 0:
            print id_list
            for id in id_list:
                real_url = response.meta['real_url']
                get_url = response.meta['get_url'] + id
                print 'real_url', real_url
                if 'news' in real_url:
                    formdata = {'newsid': id}
                    print formdata
                    yield FormRequest(url=real_url,dont_filter=True,formdata=formdata,meta={'ba_type':response.meta['ba_type'],"get_url":get_url},callback=self.parse_item)
                else:
                    url = real_url + id
                    print url
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],"get_url":get_url},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        pubtime = re.search(r'CreateTime>\s*?(20\d{2}-\d{2}-\d{2}\s\d{2}:\d{2}):?\d{2}?', response.body)
        pubtime1 = re.search(r'createtime>(20\d{2}-\d{2}-\d{2})</createtime', response.body)
        title = re.search(r'NewsTitle>(.+?)<', response.body)
        title1 = re.search(r'title>(.+)</title', response.body)
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市射阳市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['medianame'] = u'射阳12345在线'
        item['url'] = response.meta['get_url']
        content = re.search(r'NewsContent>(.*)</Json', response.body)
        content1 = re.search(r'OutPut">(.*)<', response.body)
        if title:
            item['title'] = title.group(1).strip()
        elif title1:
            item['title'] = title1.group(1).strip()
        if pubtime:
            item['pubtime'] = pubtime.group(1).strip()
        elif pubtime1:
            item['pubtime'] = pubtime1.group(1).strip()
        if content:
            item['content'] = content.group(1)
        elif content1:
            item['content'] = content1.group(1)
        else:
            print pubtime,pubtime1,title,title1,content,content1
            print '出错!!!!!!'
            print '出错!!!!!!'
            print '出错!!!!!!'
            print response.body
            print item
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



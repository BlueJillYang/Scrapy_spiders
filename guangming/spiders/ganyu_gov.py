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


class Ganyu_gov(scrapy.Spider):
    name = "ganyu_gov"  # 赣榆区政府
    start_urls = [
        'http://xx.ganyu.gov.cn/ news',  # 书记/区长信箱
        'http://www.ganyu.gov.cn/gyqzf/yjzj/yjzjall_gy.html news',  # 意见征集
    ]
    Debug = True
    doredis = True
    source = u"赣榆区政府"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Ganyu_gov, self).__init__()
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
            if 'yjzjall' in url:
                url = 'http://www.ganyu.gov.cn/TrueCMS/visitorController/getPetitionListByType.do?numPerPage=10&dept=gyqzf&pageNum=1&callback=truecmsData&_='
            yield Request(url=url,method='get',meta={'ba_type':channel['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        if 'TrueCMS' in response.url:
            print response.body
            jsonDict = json.loads(re.search(r'\{.+\}', response.body).group())['content']
            for data in jsonDict:
                title = data['theme']
                pubtime = data['starttime'].strip() + ' 00:00'
                url_id = data['id']
                url = 'http://www.ganyu.gov.cn/TrueCMS/visitorController/toViewTheme.do?model=gy&id=' + url_id
                yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime,'title':title},callback=self.parse_item)
        else:
            data_list = response.xpath('//tr[@class="mail_list_nr"]')
            if len(data_list) > 0:
                for data in data_list:
                    url = data.xpath('./@onclick').extract()[0]
                    pubtime = data.xpath('./td[last()-1]/span/text()').extract()[0].strip() + ' 00:00'
                    title = data.xpath('./td[2]/span/text()').extract()[0].strip()
                    url = 'http://xx.ganyu.gov.cn/MailBox/FinishedDetail/?owner=0&id=' + re.search(r'\d+', url).group()
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime,'title':title},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省连云港市赣榆区'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['medianame'] = u'赣榆区人民政府'
        item['url'] = response.url
        pubtime = response.meta['pubtime']
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
        title = response.xpath('//div[@class="art-title"]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title']
        content = response.xpath('//div[@class="mail_xq_main"]').extract() or \
                  response.xpath('//div[@class="art-main"]').extract()
        item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



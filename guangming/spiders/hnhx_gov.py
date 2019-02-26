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


class Hnhx_gov(scrapy.Spider):
    name = "hnhx_gov"  # 滑县人民政府
    start_urls = [
        'http://www.hnhx.gov.cn/xwzx/zwyw.htm news',
        'http://www.hnhx.gov.cn/xwzx/tzgg.htm news',
        'http://www.hnhx.gov.cn/xwzx/ztlm.htm news',
        'http://www.hnhx.gov.cn/xwzx/bmdt.htm news',
        'http://www.hnhx.gov.cn/xwzx/xzdt.htm news',
        'http://www.hnhx.gov.cn/xwzx/ayswcw_xwsjdlhhdbdj.htm news',
        'http://www.hnhx.gov.cn/xwzx/xwfsj_xzczhdbdj.htm news',
        'http://www.hnhx.gov.cn/xwzx/wbgz.htm news',
        'http://www.hnhx.gov.cn/xzxx.jsp?urltype=tree.TreeTempUrl&wbtreeid=1082 news',
        'http://www.hnhx.gov.cn/zmhd/hygq.htm news',
    ]
    Debug = True
    doredis = True
    source = u"滑县人民政府"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 4.5,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Hnhx_gov, self).__init__()
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
        data_list = response.xpath('//table[contains(@class, "winstyle")]//tr[@id]/td/a') or \
                    response.xpath('//form//table[contains(@class, "winstyle")]//tr/td/a')
        for data in data_list:
            url = data.xpath('./@href').extract()[0]
            pubtime = data.xpath('./../following-sibling::td[1]/span/text()').extract() or data.xpath('./../following-sibling::td[1]/text()').extract()
            pubtime = re.search(r'\d{4}-\d{1,2}-\d{1,2}', pubtime[0]).group()
            title = data.xpath('./@title').extract() or data.xpath('./span/text()').extract()
            title = title[0].strip()
            url = urlparse.urljoin(response.url, url)
            # print url,pubtime,title
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime,'title':title},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'河南省安阳市滑县'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['medianame'] = u'滑县人民政府'
        item['url'] = response.url
        pubtime = response.xpath('//span[contains(@class, "timestyle")]/text()').extract()
        if len(pubtime) > 0:
            pubtime = re.search(r'\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}', pubtime[0]).group()
        else:
            pubtime = response.meta['pubtime'].strip() + ' 00:00'
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
        title = response.xpath('//td[contains(@class, "titlestyle")]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
            if u'流水号' in item['title']:
                item['title'] = response.meta['title'].strip()
        else:
            item['title'] = response.meta['title'].strip()
        content = response.xpath('//div[contains(@class, "govitemcontentdetal")]').extract() or \
                  response.xpath('//td[contains(@class, "contentstyle")]').extract()
        item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



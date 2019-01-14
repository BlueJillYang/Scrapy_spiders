#!/usr/bin/python
#-*- coding: utf-8 -*-import sys
import re
import time
import sys
import scrapy
import json
import redis
import random
import urllib
import requests
import urlparse
from scrapy import Selector
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import FormRequest
from scrapy.utils.response import get_base_url
from scrapy import signals
from urlparse import urljoin
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime,create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Byxzfcg(scrapy.Spider):
    name = "byxzfcg"
    start_urls = [
        'http://baoying.yangzhou.gov.cn/xxgk_info/by_xxgk/by_xxgkml.jsp?channel_id=16e35ce11021437a805d589ff549d31e&xx=1&qzf=5&ml=1&mlname=%E9%87%87%E8%B4%AD%E5%85%AC%E5%91%8A PN', # 采购公告 827
        'http://baoying.yangzhou.gov.cn/xxgk_info/by_xxgk/by_xxgkml.jsp?channel_id=7c6ce7b05918435b88c930bc6171101a&xx=1&qzf=5&ml=1&mlname=%E6%8B%9B%E6%8A%95%E6%A0%87%E5%85%AC%E5%91%8A PN',  # 招投标公告 1050
        'http://baoying.yangzhou.gov.cn/xxgk_info/by_xxgk/by_xxgkml.jsp?channel_id=2c1c1d389f0048bf86269673ac751d7d&xx=1&qzf=5&ml=1&mlname=%E5%9C%9F%E5%9C%B0%E6%8B%8D%E5%8D%96 PN',  # 土地出让 80 该频道有PN 有RN
        # &cn_name=&currentPage=3&code_id=&bid=   # 翻页参数
        # 理论1957条 实际1950条 采集率99.64%
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=True):
        super(Byxzfcg, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//table[@class="table table-bordered"]//tr//td/a')
        for each in data_list:
            url = each.xpath('./@href').extract()[0]
            title = each.xpath('./text()').extract()[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],
                                                     'title': title},callback=self.parse_item)

        if self.history and response.meta["page_parse"]:
            page_rule = response.xpath(u'//span/a[contains(text(), "末页")]/@href').extract()
            if len(page_rule) > 0:
                totalpage = re.search(r'submitPage.(\d+).+', page_rule[0]).group(1)
                for i in range(2, int(totalpage)+1):
                    page_url = response.url + '&cn_name=&currentPage={}&code_id=&bid='.format(i)
                    print '处理翻页,', page_url
                    yield Request(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.xpath('//table[@class="xxgk_content_info1"]/tbody/tr[4]/td[2]/text()').extract()
        if len(item['pubtime']) > 0:
            item['pubtime'] = item['pubtime'][0] + ' 00:00'
        else:
            print '{} 没有时间'.format(response.url)
        item['title'] = response.xpath('//div[@class="contentShow"]/div[1]/text()').extract()
        if len(item['title']) > 0:
            item['title'] = item['title'][0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省扬州市宝应县'
        item['source'] = u'宝应县人民政府'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = '//div[@class="contentShow"]'
        item['content'] = response.xpath(content).extract()[0]
        # 处理一下混杂网站的type分类, 土地出让频道里有PN RN
        if u'成交' in item['title']:
            item['type'] = 'RN'
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass


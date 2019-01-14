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


class Lzhqrmzf(scrapy.Spider):
    name = "lzhqrmzf"
    start_urls = [
        'http://zwgk.bengbu.gov.cn/com_list.jsp?serialnum=CE&LmId=368809240&DwId=87430039&OfNature=400000 PN',  # 招标
        'http://zwgk.bengbu.gov.cn/com_list.jsp?serialnum=CE&LmId=368808766&DwId=87430039&OfNature=400000 PN',  # 采购
        'http://zwgk.bengbu.gov.cn/com_list.jsp?serialnum=CE&LmId=368808806&DwId=87430039&OfNature=400000 RN',  # 中标成交公告
        'http://zwgk.bengbu.gov.cn/com_list.jsp?serialnum=CE&LmId=368809266&DwId=87430039&OfNature=400000 RN',  # 中标公示
        # 理论180条 实际180条
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url=None,history=True):
        super(Lzhqrmzf, self).__init__()
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
        data_list = response.xpath('//div[contains(@class, "List")]/ul[@class="ul"]/li[not( @class="ed")][not(@id)]/a')
        print len(data_list)
        for each in data_list:
            url = each.xpath('./@href').extract()[0]
            pubtime = each.xpath('./following-sibling::span[2]/text()').re('\d+-\d+-\d+')[0]
            title = each.xpath('./text()').extract()[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            print url,  '  pubtime: ', pubtime
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime, 'title': title},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page_rule = response.xpath('//div[@class="page"]/a[last()]/@href').extract()
            print page_rule
            if len(page_rule) > 0:
                page_rule = page_rule[0]
                if re.search(r'&page=(\d+)', page_rule):
                    count = int(re.search(r'&page=(\d+)', page_rule).group(1))
                    for i in range(2,int(count)+1):
                        page_url = response.url + '&page={}'.format(i)
                        print page_url
                        yield Request(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.xpath('//div[@class="Titinfo"]/h2/text()').extract()
        if len(item['title']) > 0:
            item['title'] = item['title'][0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'安徽省蚌埠市龙子湖区'
        item['source'] = u'蚌埠市龙子湖区人民政府'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = '//div[@id="printArea"]'
        item['content'] = response.xpath(content).extract()[0]
        # print item
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

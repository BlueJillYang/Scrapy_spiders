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
    name = "byxzfcg_old"
    start_urls = [
        'http://baoying.yangzhou.gov.cn/xxgk_info/by_xxgk/by_xxgkml.jsp?channel_id=16e35ce11021437a805d589ff549d31e&code_id=&xx=1&bid=&mlname=%E9%87%87%E8%B4%AD%E5%85%AC%E5%91%8A&ml=1&qzf=5&cn_name=&currentPage=1 CN',
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 1, "RETRY_TIMES": 5, "DOWNLOAD_TIMEOUT": 15}

    def __init__(self, start_url=None, pages=1):
        super(Byxzfcg, self).__init__()
        # self.proxy_list = self.configure.get_proxy_from_api(domain="weibo.cn")
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            url = job.split()[0]
            ba_type = job.split()[1]
            for page in range(1, int(pages) + 1):
                if page > 1:
                    next_url = url[:url.rindex(".")] + '_' + str(page) + ".shtml"
                else:
                    next_url = url
                self.post_params.append({"url": next_url, "ba_type": ba_type})
                print self.post_params
        # dispatcher.connect(self.initial, signals.engine_started)

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            # proxy = random.choice(self.proxy_list)
            yield Request(url=url,
                          meta={"ba_type": channel["ba_type"]}, # "proxy": proxy},
                          callback=self.parse_link)

    def parse_link(self, response):
        lis = response.xpath('//ul[@class="item lh jt_dott f14"]/li')
        for li in lis:
            url = li.xpath('./a/@href').extract_first()
            title = li.xpath('./a/@title').extract_first().strip()
            pubtime = li.xpath('./span/text()').extract_first().strip()
            url = urljoin(response.url, url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            # proxy = random.choice(self.proxy_list)
            yield Request(url=url,
                          meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},# "proxy": proxy},
                          callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省扬州市宝应县'
        item['source'] = u'宝应县人民政府'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        item['content'] = ''.join(response.xpath('//div[@id="zoom"]').extract())
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print(item)

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

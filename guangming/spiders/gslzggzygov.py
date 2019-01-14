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


class Gslzggzygov(scrapy.Spider):
    name = "gslzggzygov"
    start_urls = [
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002001/002001001/1.html PN',
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002001/002001002/1.html CN',
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002001/002001003/1.html RN',
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002001/002001004/1.html RN',
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002001/002001005/1.html RN',
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002002/002002001/1.html PN',
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002002/002002002/1.html CN',
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002002/002002003/1.html RN',
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002002/002002004/1.html PN',
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002003/002003001/1.html PN',
        'http://lzggzyjy.lanzhou.gov.cn/jygk/002003/002003002/1.html RN',
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=True):
        super(Gslzggzygov, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        self.count = 0
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
        data_list = response.xpath('//ul[@class="ewb-news-items"]/li')
        # data_list = response.xpath('//td[@class="cl3"]/table[2]/tr[not(@style)]').extract()
        print len(data_list)
        # print data_listmeta
        for each in data_list:
            url = each.xpath('./div[@class="ewb-work-block l"]/a/@href').extract()[0]
            pubtime = each.xpath('./span/text()').re('\d+-\d+-\d+')[0]
            title = each.xpath('./div[@class="ewb-work-block l"]/a/@title').extract()[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            print url,  '  pubtime: ', pubtime
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime, 'title': title},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page_rule = response.xpath('//span[@id="index"]/text()').extract()
            print page_rule
            if len(page_rule) > 0:
                if re.search(ur'\d+/(\d+)', page_rule[0]):
                    count = int(re.search(ur'1/(\d+)', page_rule[0]).group(1))
                    page = count
                    print 'count', count
                    for i in range(2,int(page)+1):
                        page_url = response.url.replace('1.html', '%d.html'%i)
                        print page_url
                        print '处理翻页 %s'%page_url
                        yield Request(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        self.count += 1
        print '处理了%d条'%self.count
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.meta['title']
        item["type"] = response.meta["ba_type"]
        item['area'] = u'甘肃省兰州市'
        item['source'] = u'兰州市公共资源交易中心'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        if '002001001' in response.url:
            content = '//div[@id="b"]'
        elif '002001002' in response.url:
            content = '//div[@id="b"]'
        elif '002001003' in response.url:
            content = '//div[@id="i"]'
        elif '002001004' in response.url:
            content = '//div[@id="f"]'
        elif '002001005' in response.url:
            content = '//div[@id="k"]'
        elif '002002001' in response.url:
            content = '//div[@id="b"]'
        elif '002002002' in response.url:
            content = '//div[@id="b"]'
        elif '002002003' in response.url:
            content = '//div[@id="f"]'
        elif '002002004' in response.url:
            content = '//div[@class="contents" and @id="tab-1"]'
        elif '002003001' in response.url:
            content = '//div[@class="news-article"]'
        elif '002003002' in response.url:
            content = '//div[@class="news-article"]'
        else:
            content = '/html/body'
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

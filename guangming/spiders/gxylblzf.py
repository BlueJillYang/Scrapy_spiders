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


class Gxylblzf(scrapy.Spider):
    name = "gxylblzf"
    start_urls = [
        'http://www.beiliu.gov.cn/beiliushizhengfuwangz/xxgk/ggzypzlygk/gcjsxmzbtbly PN',
        'http://www.beiliu.gov.cn/beiliushizhengfuwangz/xxgk/ggzypzlygk/gycqjyly PN',
        'http://www.beiliu.gov.cn/beiliushizhengfuwangz/xxgk/ggzypzlygk/zfcgly PN',
        'http://www.beiliu.gov.cn/beiliushizhengfuwangz/xxgk/ggzypzlygk/gytdsyqykyqcrly PN',
        'http://www.beiliu.gov.cn/beiliushizhengfuwangz/xxgk/zdjsxmpzhsylygk/zbtb PN',
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=True):
        super(Gxylblzf, self).__init__()
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
        data_list = response.xpath('//div[@class="dczjlblist"]/ul/li')
        ajax_id = response.xpath('//input[@id="channelCode"]/@value').extract()
        for each in data_list:
            url = each.xpath('./div[1]/a/@href').extract()[0]
            pubtime = each.xpath('./div[2]/text()').re('\d+.\d+.\d+')[0]
            title = each.xpath('./div[1]/a/@title').extract()[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            print '  pubtime: ', pubtime, ' ', url
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],
                                                     "pubtime":pubtime, 'title': title,
                                                     'ajax_id': ajax_id}, callback=self.parse_item)
        print len(data_list)
        # print data_listmeta
        if self.history and response.meta["page_parse"]:
            ajax_url = 'http://www.beiliu.gov.cn/channel/'
            total_page = response.xpath('//ul[@id="pages"]/li[last()]/a/@onclick').re('\d+')[0]
            for i in range(2, int(total_page)+1):
                timestamp0 = time.strftime('%Y%m%d%H%M%S')
                final_url = ajax_url + '%d?pageNo=%d&$$time$$=%s'%(int(response.meta['ajax_id']), int(i), timestamp0)
                yield Request(url=final_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},
                              callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        self.count += 1
        print '处理了%d条'%self.count
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.xpath('//div[@class="tzggtitle"]/h1').extract()
        if len(item['title']) > 0:
            item['title'] = item['title'][0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        if u'成交公' in item['title'] or u'结果' in item['title'] or u'中标' in item['title'] or \
                u'未入围' in item['title'] or u'失败公' in item['title'] or u'合同公' in item['title'] or \
                u'结果有关事宜公告' in item['title']:
            item['type'] = 'RN'
        elif u'变更' in item['title'] or u'澄清' in item['title'] or u'答疑' in item['title'] or \
                u'更正' in item['title'] or u'更改' in item['title']:
            item['type'] = 'CN'
        elif u'招标公' in item['title'] or u'磋商' in item['title'] or u'采购公' in item['title'] or\
                u'出让公告' in item['title']:
            item['type'] = 'PN'
        elif u'预告' in item['title']:
            item['type'] = 'PF'
        item['area'] = u'广西壮族自治区玉林市北流市'
        item['source'] = u'北流市人民政府门户网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['content'] = response.xpath('//div[@class="tzgginfo"]').extract()
        if len(item['content']) > 0:
            item['content'] = item['content'][0]
        else:
            print 'content有问题:  %s'%response.url
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

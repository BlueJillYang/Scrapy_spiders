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


class Jhxzfmhw(scrapy.Spider):
    name = "jhxzfmhw"  # 无更新
    start_urls = [
        # 'http://www.jianhu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=1&endrecord=44&perpage=15 col=1&appid=1&webid=1&path=%2F&columnid=1369&sourceContentType=1&unitid=2633&webname=%E5%BB%BA%E6%B9%96%E5%8E%BF%E6%94%BF%E5%BA%9C%E9%97%A8%E6%88%B7%E7%BD%91%E7%AB%99%E7%BE%A4&permissiontype=0 CN',
        # 'http://www.jianhu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=1&endrecord=45&perpage=15 col=1&appid=1&webid=1&path=%2F&columnid=1370&sourceContentType=1&unitid=2633&webname=%E5%BB%BA%E6%B9%96%E5%8E%BF%E6%94%BF%E5%BA%9C%E9%97%A8%E6%88%B7%E7%BD%91%E7%AB%99%E7%BE%A4&permissiontype=0 CN',
        # 'http://www.jianhu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=1&endrecord=8&perpage=15 col=1&appid=1&webid=1&path=%2F&columnid=1371&sourceContentType=1&unitid=2633&webname=%E5%BB%BA%E6%B9%96%E5%8E%BF%E6%94%BF%E5%BA%9C%E9%97%A8%E6%88%B7%E7%BD%91%E7%AB%99%E7%BE%A4&permissiontype=0 CN',
        'http://www.jianhu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=1&endrecord=45&perpage=15 col=1&appid=1&webid=1&path=%2F&columnid=1372&sourceContentType=1&unitid=2633&webname=%E5%BB%BA%E6%B9%96%E5%8E%BF%E6%94%BF%E5%BA%9C%E9%97%A8%E6%88%B7%E7%BD%91%E7%AB%99%E7%BE%A4&permissiontype=0 PN',
        'http://www.jianhu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=1&endrecord=5&perpage=15 col=1&appid=1&webid=1&path=%2F&columnid=1386&sourceContentType=1&unitid=2633&webname=%E5%BB%BA%E6%B9%96%E5%8E%BF%E6%94%BF%E5%BA%9C%E9%97%A8%E6%88%B7%E7%BD%91%E7%AB%99%E7%BE%A4&permissiontype=0 CN',
        'http://www.jianhu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=1&endrecord=9&perpage=15 col=1&appid=1&webid=1&path=%2F&columnid=1387&sourceContentType=1&unitid=2633&webname=%E5%BB%BA%E6%B9%96%E5%8E%BF%E6%94%BF%E5%BA%9C%E9%97%A8%E6%88%B7%E7%BD%91%E7%AB%99%E7%BE%A4&permissiontype=0 CN',

    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.2,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url=None,history=True):
        super(Jhxzfmhw, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"data":job.split()[1],"ba_type":job.split()[2]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            post_data = {}
            for i in channel['data'].split('&'):
                post_data[i.split('=')[0]] = urllib.unquote(i.split('=')[1])
            yield FormRequest(url=url,method='post',formdata=post_data,meta={"ba_type":channel["ba_type"],'data':post_data,"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = Selector(text=response.body).xpath('//record').extract()
        for each in data_list:
            sel1 = Selector(text=each)
            url = ''.join(sel1.xpath('//a/@href').extract())
            pubtime = sel1.xpath('//td[@class="bt_time"]//text()').re('\d+-\d+-\d+')[0]
            title = ''.join(sel1.xpath('//a/@title').extract())
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            get_page = response.xpath('//totalpage//text()').re('(\d+)')[0]
            # print get_page
            # print type(get_page)
            page = int(get_page)/3 if int(get_page)%3 == 0 else int(get_page)/3 + 1
            for i in range(2,3):
                page_url = re.sub('startrecord=\d+','startrecord='+str((i-1)*45+1),response.url)
                print page_url
                yield FormRequest(url=page_url,method='post',formdata = response.meta['data'],meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市建湖县'
        item['source'] = u'建湖县政府门户网站'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        item['content'] = ''.join(response.xpath('//div[@id="zoom"]').extract())
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

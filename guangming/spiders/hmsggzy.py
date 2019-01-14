#!/usr/bin/python
#-*- coding: utf-8 -*-import sys
import re
import time
import sys
import scrapy
import json
import redis
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


class Hmsggzy(scrapy.Spider):
    name = "hmsggzy"
    start_urls = [

    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                        "DOWNLOAD_DELAY":0.1,
                        "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url=None,history=True):
        super(Hmsggzy, self).__init__()
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
        data_list = response.xpath("//table[@id='MoreInfoList1_DataGrid1']/tr").extract()
        for each in data_list:
            sel1 = Selector(text=each)
            url = ''.join(sel1.xpath('//td[2]/a/@href').extract())
            title = ''.join(sel1.xpath('//td[2]/a/@title').extract())
            pubtime = sel1.xpath('//td[3]//text()').re('\d+-\d+-\d+')[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page = response.xpath('//div[@id="MoreInfoList1_Pager"]/table/tr/td[1]/font[1]//text()').extract()[0]
#            print page
            for i in range(2,int(page)+1):
                data={
                    '__VIEWSTATE':response.xpath("//input[@id='__VIEWSTATE']/@value").extract()[0],
                    ' __VIEWSTATEGENERATOR':response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract()[0],
                    '__EVENTTARGET':'MoreInfoList1$Pager',
                    '__EVENTARGUMENT':str(i),
                    '__VIEWSTATEENCRYPTED':''}
                yield FormRequest(url=response.url,formdata=data,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省海门市'
        item['source'] = u'海门市公共资源交易网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        item['content'] = ''.join(response.xpath('//td[@id="TDContent"]').extract())
        print item
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

#!/usr/bin/python
# -*- coding: utf-8 -*-
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


class Dfggzy(scrapy.Spider):
    name = "dfggzy"  # 无更新
    start_urls = [
        'http://221.231.122.12/dfweb/jyxx/005006/005006001/MoreInfo.aspx?CategoryNum=005006001 PN',
        'http://221.231.122.12/dfweb/jyxx/005005/005005003/MoreInfo.aspx?CategoryNum=005005003 RN',
        'http://221.231.122.12/dfweb/jyxx/005005/005005001/MoreInfo.aspx?CategoryNum=005005001 RN',
        'http://221.231.122.12/dfweb/jyxx/005004/005004003/MoreInfo.aspx?CategoryNum=005004003 RN',
        'http://221.231.122.12/dfweb/jyxx/005004/005004001/MoreInfo.aspx?CategoryNum=005004001 RN',
        'http://221.231.122.12/dfweb/jyxx/005003/005003006/MoreInfo.aspx?CategoryNum=005003006 CN',
        'http://221.231.122.12/dfweb/jyxx/005003/005003003/MoreInfo.aspx?CategoryNum=005003003 RN',
        'http://221.231.122.12/dfweb/jyxx/005003/005003001/MoreInfo.aspx?CategoryNum=005003001 PN',
        'http://221.231.122.12/dfweb/jyxx/005002/005002006/MoreInfo.aspx?CategoryNum=005002006 CN',
        'http://221.231.122.12/dfweb/jyxx/005002/005002004/MoreInfo.aspx?CategoryNum=005002004 CN',
        'http://221.231.122.12/dfweb/jyxx/005002/005002002/MoreInfo.aspx?CategoryNum=005002002 PN',
        'http://221.231.122.12/dfweb/jyxx/005001/005001007/MoreInfo.aspx?CategoryNum=005001007 RN',
        'http://221.231.122.12/dfweb/jyxx/005001/005001006/MoreInfo.aspx?CategoryNum=005001006 CN',
        'http://221.231.122.12/dfweb/jyxx/005001/005001004/MoreInfo.aspx?CategoryNum=005001004 CN',
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                        "DOWNLOAD_DELAY":0.25}

    def __init__(self, start_url=None,history=True):
        super(Dfggzy, self).__init__()
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
            for i in range(2,3):
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
        item['area'] = u'江苏省盐城市大丰区'
        item['source'] = u'大丰公共资源交易网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        item['content'] = ''.join(response.xpath('//td[@id="TDContent"]').extract())
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

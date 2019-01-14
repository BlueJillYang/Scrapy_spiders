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


class Zjsggzyjydzw(scrapy.Spider):
    name = "zjsggzyjydzw" # 无更新
    start_urls = [
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002001&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002002&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002003&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002004&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002005&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001002006&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001003003&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001003004&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001003001&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001003005&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001003006&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004001&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004002&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004003&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004004&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004005&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001004006&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005001&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005002&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005003&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005004&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005005&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001005006&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006001&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006002&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006003&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006004&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006005&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001001006006&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002001&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002002&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002003&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002004&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002005&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002002006&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003001&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003002&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003003&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003004&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003005&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002003006&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004001&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004002&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004003&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004004&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004005&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002004006&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005001&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005002&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005003&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005004&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005005&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002005006&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002006001&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001002006006&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001003001001&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001003003001&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001004001001&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001004003001&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001001&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001002&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001003&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001004&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001005&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006001006&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003001&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003002&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003003&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003004&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003005&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006003006&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002001&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002002&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002003&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002004&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002005&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001006002006&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007001001&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007001005&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007001004&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007001002&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007001003&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007002001&title= PF',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007003001&title= PF',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001007004001&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001008001001&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001008002001&title= RN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005001001&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005002001&title= PN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005003&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005001006&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005002002&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005002003&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005002006&title= CN',
        'http://ggzy.zhenjiang.gov.cn/services/ZjWebService/getGovInfoPubMoreInfo?response=application/json&pageIndex=1&pageSize=20&categorynum=001005004&title= CN',

    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history = True):
        super(Zjsggzyjydzw, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            return_page = job.split()[0].replace('getGovInfoPubMoreInfo','getGovInfoPubByCount').replace('pageIndex=1&pageSize=20&','')
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1],'return_page':return_page})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],'return_page':channel['return_page'],"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = json.loads(json.loads(response.body)['return'])['Table']
        for each in data_list:
            url = each['infoUrl']
            pubtime = each['infodate']
            title = each['title']
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            resp = requests.get(url=response.meta['return_page'])
            page = int(json.loads(resp.text)['return'])/10+1
            for i in range(2,int(page)+1):
                page_url = response.url.replace('pageIndex=1','pageIndex='+str(i))
                yield FormRequest(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省镇江市市'
        item['source'] = u'镇江市公共资源交易电子平台'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        item['content'] = ''.join(response.xpath('//div[@class="article-block"]').extract())
        print item
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

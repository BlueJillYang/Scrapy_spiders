#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'cwq'
import re
import time
import sys
import scrapy
import json
import redis
import urllib
import requests
import urlparse
from scrapy.http import Request
import datetime
from scrapy import Selector
from scrapy.http import FormRequest
from scrapy.utils.response import get_base_url
from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime,create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class jsczwjqggzy(scrapy.Spider):
    name = "jsczwjqggzy"
    start_urls = [
        ### "http://www.wj.gov.cn:8000/wjweb/ggxx/004001/004001001/004001001001/?Paging=1 PN",#建设工程# 无内容，只有附带doc
        "http://www.wj.gov.cn:8000/wjweb/ggxx/004001/004001002/?Paging=1 PN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004001/004001004/?Paging=1 RN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004002/004002001/?Paging=1 PN",#政府采购
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004002/004002002/?Paging=1 CN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004002/004002003/?Paging=1 RN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004002/004002004/?Paging=1 PN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004002/004002005/004002005001/?Paging=1 PN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004002/004002005/004002005002/?Paging=1 RN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004003/004003001/?Paging=1 PN",#医药采购
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004003/004003002/?Paging=1 CN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004003/004003003/?Paging=1 RN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004003/004003004/?Paging=1 PN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004004/004004001/?Paging=1 PN",#产权交易
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004004/004004003/?Paging=1 CN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004004/004004002/?Paging=1 RN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004004/004004004/?Paging=1 PN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004006/004006001/004006001001/?Paging=1 PN",#乡镇-工程建设
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004006/004006001/004006001002/?Paging=1 CN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004006/004006001/004006001003/?Paging=1 RN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004006/004006002/004006002001/?Paging=1 PN",#乡镇-政府采购
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004006/004006002/004006002002/?Paging=1 CN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004006/004006002/004006002003/?Paging=1 RN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004006/004006002/004006002004/?Paging=1 PN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004006/004006003/004006003001/?Paging=1 PN",#乡镇-产权交易
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004006/004006003/004006003002/?Paging=1 CN",
        # "http://www.wj.gov.cn:8000/wjweb/ggxx/004006/004006003/004006003003/?Paging=1 RN"
    ]
    Debug = True
    doredis = True
    source = u"常州市武进区公共资源"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self, start_url=None, history=True):
        super(jsczwjqggzy, self).__init__()
        jobs = self.start_urls
        # jobs = start_url.split('|')
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

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
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True,"page_index":"1"},callback=self.parse_link)

    def parse_link(self, response):
        urls = response.xpath("//a[@title and contains(@href,'/wjweb/')]/@href").extract()

        for index,url in enumerate(urls):
            final = urlparse.urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            yield Request(url=final,method='get',meta={"ba_type": response.meta["ba_type"], "page_index": response.meta["page_index"]}, callback=self.parse_item)

        if response.meta["page_parse"]:
            page = response.xpath("//td[@id='Paging']//font[2]/b/text()").extract()[0].strip()
            if self.history and int(page)>1:
                    for i in range(2,int(page)+1):
                        url = response.url.replace("Paging=1","Paging="+str(i))
                        yield Request(url=url,method='get',meta={"ba_type": response.meta["ba_type"], "page_parse": False, "page_index": str(i)}, callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath("//td[@id='tdTitle']//font[@color and @class]/text()").extract()[0]
        pubtime = pubtime.replace("/","-")
        pubtime = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",pubtime).group(0)
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M")
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省常州市武进区'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath("//td[@id='tdTitle']/font/text()").extract()[0].strip()
        item['content']= response.xpath("//td[@id='TDContent']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            print response.meta["page_index"],item['title'],item["type"]
            yield item


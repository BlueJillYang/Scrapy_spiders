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


class jsnjjncg(scrapy.Spider):
    name = "jsnjjncg"
    start_urls = [
        "http://www.njjncg.gov.cn/purchasingInfo/listPages CGXX-CGGG PN", #147
        "http://www.njjncg.gov.cn/purchasingInfo/listPages CGXX-GZGG CN", #1
        "http://www.njjncg.gov.cn/purchasingInfo/listPages CGXX-ZBCJGG RN", #134
        "http://www.njjncg.gov.cn/purchasingInfo/listPages CGXX-HTGS RN" #182
    ]
    Debug = True
    doredis = False
    source = u"南京市江宁区政府采购网"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self,start_url=None,history=True):  #默认 False 采集所有，
        super(jsnjjncg, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"categoryId2":job.split()[1],"ba_type":job.split()[2]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            url = "http://www.njjncg.gov.cn/purchasingInfo/listPages"
            formdata={
                "page": "1",
                "categoryId2": channel["categoryId2"]
            }
            yield FormRequest(url=url,meta={"ba_type":channel["ba_type"],"page_parse":True,"categoryId2":channel["categoryId2"]},method='post',formdata=formdata,callback=self.parse_link)

    def parse_link(self, response):
        urls = response.xpath("//div[@class='screen_list_item']//h2/a/@href").extract()
        for index,url in enumerate(urls):
            final = urlparse.urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"]},callback=self.parse_item)

        lastPage = response.xpath("//div[@class='paging']//a[last()]/@onclick").extract()
        if len(lastPage) > 0:
            page = re.search("(\d+)",lastPage[0]).group(0)

            if self.history and int(page) > 1 and response.meta["page_parse"]:
                # for i in range(2,int(page)+1):
                for i in range(2,3):
                    formdata={
                        "page": str(i),
                        "categoryId2": response.meta["categoryId2"]
                    }
                    yield FormRequest(url=response.url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},method='post',formdata=formdata,callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()

        pubtime = response.xpath("//div[@class='details_info']/span[1]/em/text()").extract()[0]
        item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",pubtime).group(0) + " 00:00"
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省南京市江宁区'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath("//h2/text()").extract()[0]
        item['content']= response.xpath("//div[@class='details_page']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item


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
import datetime
from scrapy.http import Request
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


class jsszzfcgw(scrapy.Spider):
    name = "jsszzfcgw_old"
    start_urls = [
        'http://www.zfcg.suzhou.gov.cn/html/search.shtml?title=&choose=&projectType=2&zbCode=&appcode= RN',
        'http://www.zfcg.suzhou.gov.cn/html/search.shtml?title=&choose=&projectType=1&zbCode=&appcode= CN',
        'http://www.zfcg.suzhou.gov.cn/html/search.shtml?title=&choose=&projectType=0&zbCode=&appcode= PN',
    ]
    Debug = True
    doredis = True
    source = u"苏州政府采购网"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self, start_url = None,history = "30"):
        super(jsszzfcgw, self).__init__()
        self.histroy = history
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url'].replace("30",str(self.histroy))
            yield FormRequest(url=url,meta={"ba_type":channel["ba_type"]},method='get',callback=self.parse_link)

    def parse_link(self, response):
        rows = json.loads(response.body)["rows"]
        for row in rows:
            newUrl = "../html/project/"+str(row["PROJECTID"])+".shtml"
            final = urlparse.urljoin(response.url,newUrl)
            pubtime = row["RELEASE_TIME"]

            yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime},callback=self.parse_item)

    def parse_item(self, response):
            item=DataItem()

            if response.meta["ba_type"] == "PN":
                infoId = "tab1"
                infoType = "PN"
            elif response.meta["ba_type"] == "CN":
                infoId = "tab2"
                infoType = "CN"
            else:
                if u'(有)' in response.xpath("//ul[@id='menu']/li[3]/a/text()").extract()[0]:
                    infoId = "tab3"
                else:
                    infoId = "tab6"
                infoType = "RN"

            title = "//div[@id='"+infoId+"']//div[@class='M_title']/text()"
            pubtime = "//div[@id='"+infoId+"']//div[@class='date']/span/text()"
            content = "//div[@id='"+infoId+"']//div[@class='Article']"

            item["pubtime"]=response.xpath(pubtime).extract()
            if len(item["pubtime"]) >0:
               item["pubtime"] = item["pubtime"][0] + " 00:00"
            else:
               item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",response.meta["pubtime"]).group(0)

            item["type"] = infoType
            item['url'] = response.url + "#"+item["type"]

            item['area'] = u'江苏省苏州市'
            item['source'] = self.source
            item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
            item['title'] =response.xpath(title).extract()[0]
            item['content']=response.xpath(content).extract()[0]

            # if self.doredis and self.expire_redis.exists(item['url']):
            #     flag = False
            # else:
            #     flag = True
            # if item['pubtime'] and item['title'] and item['content'] and flag:
            if item['pubtime'] and item['title'] and item['content']:
                yield item


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


class jsycjyw(scrapy.Spider):
    name = "jsycjyw"
    start_urls = [
            "http://www.yce.cn/jyfwsy_lb.jsp?totalpage=16&PAGENUM=1&urltype=tree.TreeTempUrl&wbtreeid=1084 PN"
        ]
    Debug = True
    doredis = True
    source = u"盐城市教育局"
    # configure = SpecialConfig()
    post_params = []
    lost_counts = 0

    def __init__(self,start_url=None,history=True):
        super(jsycjyw, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
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
        urls = response.xpath("//div[@class='nry']//li/a/@href").extract()
        titles = response.xpath("//div[@class='nry']//li/a/@title").extract()
        for index,url in enumerate(urls):
            url = "/"+url
            final = urlparse.urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            title = titles[index]
            if u'公告' in title:
                yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"],"page_index":response.meta["page_index"],"title":title},callback=self.parse_item)
            else:
                # print "被过滤...",title
                self.lost_counts +=1

        if response.meta["page_parse"]:
            lastPage = response.xpath("//td[contains(@id,'fanye')]/text()").extract()[0]
            page = re.search(r"/(\d+)",lastPage).group(1)
            if self.history and int(page) > 1:
                for i in range(2, int(page)+1):
                    url = response.url.replace("PAGENUM=1","PAGENUM="+str(i))
                    yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"page_parse":False,"page_index":str(i)},callback=self.parse_link)

    def check_title(self,title):
        cn_conditons = [u"补充"]
        rn_conditons = [u"中标",u"流标"]
        type = "PN"

        for cn_conditon in cn_conditons:
            if cn_conditon in title:
                type = "CN"
                break

        for rn_conditon in rn_conditons:
            if rn_conditon in title:
                type = "RN"
                break

        return type

    def parse_item(self, response):
        item = DataItem()

        pubtime = response.xpath("//div[@class='author']/text()[1]").extract()[0]
        item["pubtime"] = re.search(ur"(\d{4}年\d{1,2}月\d{1,2}日\s\d{1,2}:\d{1,2})",pubtime).group(0).replace("年","-").replace("月","-").replace("日","")
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath("//h1/text()").extract()[0]
        content= response.xpath("//div[@id='vsb_content_2']").extract() or \
                          response.xpath("//div[@id='vsb_content']").extract()
        item['content'] = content[0]

        item["type"] = self.check_title(item['title'])

        if item['pubtime'] and item['title'] and item['content']:
                # print response.meta["page_index"],item['title'],item["type"],"被过滤数:",self.lost_counts
                yield item

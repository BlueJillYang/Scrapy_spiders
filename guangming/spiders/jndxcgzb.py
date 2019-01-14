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


class jndxcgzb(scrapy.Spider):
    name = "jndxcgzb"
    start_urls = [
        "http://zhaobiao.jiangnan.edu.cn/cggg1/hwl.htm PN",
        "http://zhaobiao.jiangnan.edu.cn/cggg1/gcl.htm PN",
        "http://zhaobiao.jiangnan.edu.cn/cggg1/fwl.htm PN",
        "http://zhaobiao.jiangnan.edu.cn/cgjg1/hwl.htm RN",
        "http://zhaobiao.jiangnan.edu.cn/cgjg1/gcl.htm RN",
        "http://zhaobiao.jiangnan.edu.cn/cgjg1/fwl.htm RN"
    ]
    Debug = True
    doredis = True
    source = u"江南大学采购与招标信息网"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self, start_url=None,history=True):
        super(jndxcgzb, self).__init__()
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
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True},callback=self.parse_link)

    def check_page(self,size,pageNum,pageCount,rowCount):
        if pageNum >1:
            return 19
        else:
            return size - rowCount % pageCount

    def parse_link(self, response):
        urls = response.xpath("//div[@id='con_one_1']//li/a/@href").extract()
        page = (response.xpath("//td[@id='fanye140911']/text()").extract() or response.xpath("//td[@id='fanye140914']/text()").extract())[0]
        if re.search(r"/(\d+).htm",response.url):
            rowCount = int(re.search(r"\d+",page).group(0))
            pageNum = int(re.search(r"/(\d+)",response.url).group(1))
            size = int(re.search(r"_vsb_showNewsStaticList\(.*?, (\d+),",response.body).group(1))
            list_index = self.check_page(size,pageNum,20,rowCount)
        else:  #首页
            list_index = 0

        for index,url in enumerate(urls):
            if index < list_index:
                continue
            final = urlparse.urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            yield Request(url=final,method='get',dont_filter=True,meta={"ba_type":response.meta["ba_type"]},callback=self.parse_item)

        page = int(re.search(r"/(\d+)",page).group(1))
        if self.history and int(page) > 1 and response.meta["page_parse"]:
            for i in range(int(page), 1, -1):
                url = response.url.replace(".htm","/"+str(i-1)+".htm")
                yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()

        pubtime = response.xpath("//div[@class='source']/text()").extract()[0]
        item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",pubtime).group(0) + " 00:00"
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['content']= response.xpath("//div[@id='vsb_content']").extract()[0]
        item['title'] = response.xpath("//div[@class='content_tit']/text()").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item


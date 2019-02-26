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
import datetime
from scrapy.utils.response import get_base_url
from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime,create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class jsszjsj(scrapy.Spider):
    name = "jsszjsj"
    start_urls = [
        "http://www.szjsj.gov.cn/InternetZhuJianTing/InfoExtend.action?cmd=GetSZZJ_ZBInfoList_page PN",
        "http://www.szjsj.gov.cn/InternetZhuJianTing/InfoExtend.action?cmd=GetSZZJ_ZhongBInfoList_page RN",
    ]
    Debug = True
    doredis = True
    source = u"苏州市住房和城乡建设局"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"DOWNLOAD_TIMEOUT": 30, "ROBOTSTXT_OBEY": False}

    def __init__(self, start_url=None, history=True):
        super(jsszjsj, self).__init__()
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
            formdata={"pageIndex": "1", "pageSize": "10","siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a"}
            yield FormRequest(url=url,meta={"ba_type":channel["ba_type"],"page_parse":True,"page_index":"1"},method='post',formdata=formdata,callback=self.parse_link)

    def parse_link(self, response):
        custom = json.loads(json.loads(response.body)["custom"])
        url_items = custom["list"]

        for index,url_item in enumerate(url_items):
            if "GetSZZJ_ZhongBInfoList_page" in response.url:
                final = "http://www.szjsj.gov.cn/zhcxdetail/urcInfo_zhongbiaoDetail.html?rowguid=" + url_item["RowGuid"]
            else:
                final = "http://www.szjsj.gov.cn/zhcxdetail/urcInfo_zhaobiaoDetail.html?rowguid=" + url_item["RowGuid"]
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            if response.meta["ba_type"] == "PN":
                title = url_item["Projectname"]
                pubtime = url_item["ReleaseDate"]
            else:
                title = url_item["ProjectName"]
                pubtime = datetime.datetime.strptime(url_item["BADate"], "%Y-%m-%d").strftime("%Y-%m-%d %H:%M")
            yield Request(url=final,method='get',
                          meta={"ba_type": response.meta["ba_type"], "page_index":response.meta["page_index"],
                                "title": title, "pubtime": pubtime},
                          callback=self.parse_item)

        if response.meta["page_parse"]:
            page = int(custom["total"] / 10)
            page += [0,1][custom["total"] % 10 > 0]
            if self.history and int(page)>1 :
                for i in range(2,int(page)+1):
                    formdata={"pageIndex": str(i), "pageSize": "10","siteGuid": "7eb5f7f1-9041-43ad-8e13-8fcb82ea831a"}
                    yield FormRequest(url=response.url,meta={"ba_type": response.meta["ba_type"], "page_parse": False, "page_index": str(i)},
                                      method='post',formdata=formdata,callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()

        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省苏州市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta["title"]
        item['content']= response.xpath("//div[@class='ewb-article']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item


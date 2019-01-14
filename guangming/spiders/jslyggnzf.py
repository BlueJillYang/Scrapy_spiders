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
import time
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


class jslyggnzf(scrapy.Spider):
    name = "jslyggnzf"
    start_urls = [
        # 'http://www.lygzfcg.gov.cn/Home/searchIndex PN',
    ]
    Debug = True
    doredis = True
    source = u"灌南县政府"
    # configure = SpecialConfig()
    post_params = []
    count = 1
    custom_settings = {"DOWNLOAD_DELAY":1.0}

    def __init__(self,start_url=None):
        super(jslyggnzf, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)

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
          formdata = {"searchArea": "灌南县"}
          yield FormRequest(url=url,meta={"ba_type":channel["ba_type"]},method='post',formdata=formdata,callback=self.parse_link)

    def parse_link(self, response):
        urls = response.xpath("//ul[@class='multiple']/li/a/@href").extract()

        for index,url in enumerate(urls):
            final = urlparse.urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"]},callback=self.parse_item)

    def parse_item(self, response):
        item=DataItem()
        item['pubtime'] = None
        item['title'] = None
        item['content'] = None

        pubtime = response.xpath("//h5/text()").extract()
        if len(pubtime) > 0:
            item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", pubtime[0]).group(0)
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省连云港市灌南县'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        title = response.xpath("//h4/text()").extract()
        if len(title) > 0:
            item['title'] = title[0]

        content = response.xpath("//div[@class='data_info']").extract() or response.xpath("//div[@id='content']").extract()
        if len(content)>0:
            item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item




# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import json
import redis
import random
import urllib
import datetime
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


class jsycthzf(scrapy.Spider):
    name = "jsycthzf"
    start_urls = [
        # "http://tinghu.yancheng.gov.cn/col/col18996/index.html PN",
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.5, "DOWNLOAD_TIMEOUT": 5}

    def __init__(self,start_url=None,history=False):
        super(jsycthzf, self).__init__()
        jobs = start_url.split('|')
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True},headers=self.headers,callback=self.parse_link)

    def parse_link(self, response):
        data_list = re.findall(r'<li>(.*?)</li>', response.body)
        for each in data_list:
            url = re.search(r"href=\"(.*?)\"", each).group(1)
            title = re.search(r"title=\"(.*?)\"", each).group(1)
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"], 'title': title},headers=self.headers,callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            columid = re.search(r'\d+', response.url).group()
            total_count = re.search(r'dataAfter.+totalRecord:(\d+)', response.body)
            if total_count:
                total_count = total_count.group(1)
                if int(total_count) % 42 == 0:
                    total_page = int(total_count)//42
                else:
                    total_page = int(total_count)//42 + 1
                for i in range(1, int(total_page)):
                    post_url = 'http://tinghu.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?'
                    start_i = 1 + 42*i
                    if (42 + 42*i) > int(total_count):
                        end_i = int(total_count)
                    else:
                        end_i = 42 + 42*i
                    getData = {'startrecord': str(start_i), 'endrecord': str(end_i), 'perpage': '15'}
                    final_url = post_url + urllib.urlencode(getData)
                    formData = {
                        'col': '1', 'appid': '1', 'webid': '56', 'path': '/', 'columnid': '{}'.format(columid), 'sourceContentType': '1',
                        'unitid': '36489', 'webname': '盐城市亭湖区人民政府', 'permissiontype': '0'
                    }
                    yield FormRequest(url=final_url,formdata=formData,meta={"ba_type":response.meta["ba_type"],"page_parse":False},headers=self.headers,callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath("//span[@class='date']/text()").extract()[0]
        item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", pubtime).group(0)
        title = response.xpath("//p[@class='con-title']/text()").extract()
        if len(title) > 0:
            item['title'] = title[0]
        else:
            item['title'] = response.meta['title']
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市亭湖区'
        item['source'] = u'盐城市亭湖区人民政府'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['content'] = response.xpath("//div[@id='zoom']").extract()[0]
        if u'中标' in item['title'] or u'成交' in item["title"] or u'结果' in item["title"]:
            item["type"] = "RN"
        if u'答疑' in item['title'] or u'更正' in item["title"] or u'补充' in item['title']:
            item["type"] = "CN"
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            raise Exception('{}: 字段缺失！！！'.format(response.url))

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass
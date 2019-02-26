#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import json
import datetime
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


class Zgbh(scrapy.Spider):
    name = "zgbh"
    start_urls = [
        'http://binhai.yancheng.gov.cn/col/col17618/index.html PN',  # 招投标信息 杂乱的 需要判断title分类
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False,
                       "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15}
    final = []

    def __init__(self,start_url=None,history=True):
        super(Zgbh, self).__init__()
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
        data_list = re.findall(r'<a\s*?href="(/art.+?html)"\s*?target="_blank"\s*?title=".+?">(.+?)</a>\s*?\[(20\d{2}-\d{2}-\d{2}).\s*?</li>', response.body)
        for each in data_list:
            url = each[0].strip()
            title = each[1]
            pubtime = each[2].replace(' ', '').strip() + ' 00:00'
            url = urlparse.urljoin(response.url, url)
            self.final.append(url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            # print url, '  len(set(final)): ', len(set(self.final)), '  ', pubtime, title
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"], 'title': title, 'pubtime': pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            columnid = re.search(r'col(\d+)/', response.url).group(1)
            total_count = re.search(r'dataAfter.+totalRecord:(\d+)', response.body)
            if total_count:
                total_count = total_count.group(1)
                if int(total_count) % 45 == 0:
                    total_page = int(total_count)//45
                else:
                    total_page = int(total_count)//45 + 1
                for i in range(1, int(total_page)):
                    post_url = 'http://binhai.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?'
                    start_i = 1 + 45*i
                    end_i = 45 + 45*i
                    getData = {'startrecord': str(start_i), 'endrecord': str(end_i), 'perpage': '15'}
                    final_url = post_url + urllib.urlencode(getData)
                    formData = {
                        'col': '1', 'appid': '1', 'webid': '51', 'path': '/', 'columnid': str(columnid), 'sourceContentType': '1',
                        'unitid': '30645', 'webname': '滨海县人民政府', 'permissiontype': '0'
                    }
                    yield FormRequest(url=final_url,formdata=formData,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath('//p[@class="con-title"]/../div[1]/div/span[1]/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}', pubtime[0]).group()
        else:
            item["pubtime"] = response.meta["pubtime"]
        item['pubtime'] = datetime.datetime.strptime(item['pubtime'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市滨海县'
        item['source'] = u'滨海县人民政府'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        title = response.xpath('//p[@class="con-title"]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        if u'成交' in item['title'] or u'结果' in item['title'] or u'中标' in item['title'] or \
                u'未入围' in item['title'] or u'失败' in item['title'] or u'合同公' in item['title'] or \
                u'结果有关事宜公告' in item['title'] or u'中止' in item['title'] or \
                u'终止' in item['title']:
            item['type'] = 'RN'
        elif u'变更' in item['title'] or u'澄清' in item['title'] or u'答疑' in item['title'] or \
                u'更正' in item['title'] or u'更改' in item['title'] or  u'补充' in item['title']:
            item['type'] = 'CN'
        elif u'预告' in item['title']:
            item['type'] = 'PF'
        content = response.xpath('//div[@class="main-txt"]').extract() or \
                  response.xpath('//div[@class="Section0"]').extract() or \
                  response.xpath("//div[@class='cas_content']").extract() or \
                  response.xpath("//div[@class='TRS_Editor']").extract() or \
                  response.xpath("//td[@style='line-height:28px; font-size:14px; color:#444']").extract()
        item['content'] = content[0]
        print item['title'], item['type'], item['pubtime'], item['url']
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

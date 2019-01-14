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


class Dongtai_education(scrapy.Spider):
    name = "dongtai_education"
    start_urls = [
        'http://www.dongtai.gov.cn/col/col755/index.html?uid=3643&pageNum=1 PN',
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=True):
        super(Dongtai_education, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        self.final = []
        self.count = 0
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
        data_list = re.findall(r'<a href="(/art.+?html)">(.+?)</a>', response.body)
        # print len(data_list)
        for each in data_list:
            url = each[0].strip()
            title = each[1]
            url = urljoin(response.url,url)
            self.final.append(url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            # pubtime = pubtime + " 00:00"
            print url, '  len(set(final)): ', len(set(self.final))
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"], 'title': title},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            total_count = re.search(r'dataAfter.+totalRecord:(\d+)', response.body)
            print '-'*100
            print total_count.group()
            if total_count:
                total_count = total_count.group(1)
                if int(total_count) % 45 == 0:
                    total_page = int(total_count)//45
                else:
                    total_page = int(total_count)//45 + 1
                print total_page
                for i in range(1, int(total_page)):
                    post_url = 'http://www.dongtai.gov.cn/module/web/jpage/dataproxy.jsp?'
                    start_i = 1 + 45*i
                    end_i = 45 + 45*i
                    getData = {'startrecord': str(start_i), 'endrecord': str(end_i), 'perpage': '15'}
                    final_url = post_url + urllib.urlencode(getData)
                    formData = {
                        'col': '1', 'appid': '1', 'webid': '1', 'path': '/', 'columnid': '755', 'sourceContentType': '1',
                        'unitid': '3643', 'webname': '东台市人民政府', 'permissiontype': '0'
                    }
                    # print final_url
                    yield FormRequest(url=final_url,formdata=formData,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        self.count += 1
        print '处理了%d条'%self.count
        pubtime = response.xpath('//span[@class="date"]/b/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}.\d{1,2}.\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', '')).group() + ' 00:00'
        item['title'] = response.xpath('//h1[@class="title"]/text()').extract()
        if len(item['title']) > 0:
            item['title'] = item['title'][0]
        else:
            item['title'] = response.meta['title']
        item["type"] = response.meta["ba_type"]
        if u'成交公' in item['title'] or u'结果' in item['title'] or u'中标' in item['title'] or \
                u'未入围' in item['title'] or u'失败公' in item['title'] or u'合同公' in item['title'] or \
                u'结果有关事宜公告' in item['title'] or u'中止' in item['title'] or \
                u'终止' in item['title']:
            item['type'] = 'RN'
        elif u'变更' in item['title'] or u'澄清' in item['title'] or u'答疑' in item['title'] or \
                u'更正' in item['title'] or u'更改' in item['title']:
            item['type'] = 'CN'
        elif u'招标公' in item['title'] or u'磋商' in item['title'] or u'采购公' in item['title'] or \
                u'出让公告' in item['title']:
            item['type'] = 'PN'
        elif u'预告' in item['title']:
            item['type'] = 'PF'
        item['area'] = u'江苏省盐城市东台市'
        item['source'] = u'东台市人民政府'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = '//div[@id="zoom"]'
        item['content'] = response.xpath(content).extract()[0]
        # print item
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

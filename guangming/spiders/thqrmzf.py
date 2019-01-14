# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import datetime
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


class Thqrmzf(scrapy.Spider):
    name = "thqrmzf"  # 亭湖区人民政府
    start_urls = [
        # 'http://www.tinghu.gov.cn/xxgk_list.asp?classid=17&departid=14 PN',  # 公共资源管理 类型是乱的 需要判断
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":2,
                       "DOWNLOAD_TIMEOUT":5,}

    def __init__(self,start_url=None,history=True):
        super(Thqrmzf, self).__init__()
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
        data_list = response.xpath('//td/a[@class="newstitle1"]')
        print 'len(data): {}'.format(len(data_list))
        for each in data_list:
            url = each.xpath('./@href').extract()[0]
            title = each.xpath('./@title').extract()[0]
            pubtime = each.xpath('./../following-sibling::td/text()').extract()[0]
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime.replace('/','-').replace('.','-'))
            url = urljoin(response.url, url)
            if pubtime:
                pubtime = pubtime.group()
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,'pubtime':pubtime},
                          callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = response.xpath('//td[@class="In-news"]/a[last()]/@href').extract()
            if len(page_rule) > 0:
                total_page = re.search(r'PAGE=(\d+)', page_rule[0]).group(1)
                for i in range(2, int(total_page)+1):
                    final = response.url + '&PAGE={}'.format(i)
                    time.sleep(0.5)
                    yield Request(url=final,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},
                                  callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath('//td[@class="title8 bobg1"]/text()').extract()
        title = response.xpath('//td[@class="title14"]/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime[0].replace('/', '-').strip())
            if item['pubtime']:
                item['pubtime'] = item['pubtime'].group().strip() + ' 00:00'
            else:
                item['pubtime'] = response.meta['pubtime'].strip() + ' 00:00'
        else:
            item['pubtime'] = response.meta['pubtime'].strip() + ' 00:00'
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市亭湖区'
        item['source'] = u'亭湖区人民政府'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//div[@class="padnei"]').extract()
        item['content'] = content[0]
        item['pubtime'] = datetime.datetime.strptime(item['pubtime'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item['pubtime'], item['title'], response.url
            raise Exception('{}'.format(response.url))

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass


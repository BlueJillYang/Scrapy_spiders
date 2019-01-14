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


class Xdjtyxgs(scrapy.Spider):
    name = "xdjtyxgs"  # 湘电集团有限公司
    start_urls = [
        # 'http://123.57.248.129:8999/ForePage/Skin/NewList1.aspx?page=1&pagesize=20&title=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A&keyword=&ClassId=147&GroupId=&ParentId=1 PN',  # 招标公告
        'http://123.57.248.129:8999/ForePage/Skin/NewList1.aspx?page=1&pagesize=20&title=%E9%87%8D%E8%A6%81%E5%85%AC%E5%91%8A&keyword=&ClassId=157&GroupId=&ParentId=1 PN',  # 重要公告
        'http://123.57.248.129:8999/ForePage/Skin/NewList1.aspx?page=1&pagesize=20&title=%E4%B8%AD%E6%A0%87%E5%85%AC%E5%91%8A&keyword=&ClassId=141&GroupId=&ParentId=1 RN',  # 中标公告
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":120, "RETRY_ENABLED":True, "RETRY_TIMES":10}

    def __init__(self,start_url=None,history=True):
        super(Xdjtyxgs, self).__init__()
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
        data_list = response.xpath('/html/body/table[3]/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr[1]/td[2]/a')
        print 'len(data): {}'.format(len(data_list))
        for each in data_list:
            url = each.xpath('./@href').extract()[0]
            title = each.xpath('./text()').extract()[0]
            pubtime = each.xpath('./../following-sibling::td[1]/text()').extract()[0]
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime.replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
            url = urljoin(response.url, url)
            if pubtime:
                pubtime = pubtime.group()
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,'pubtime':pubtime},
                          callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = response.xpath('//div[@class="page-bottom"]/span[1]/text()').extract()
            if len(page_rule) > 0:
                total_page = re.search(r'1/(\d+)', page_rule[0]).group(1)
                # for i in range(2, int(total_page)+1):
                for i in range(2, int(total_page)+1):
                    final = response.url.replace('page=1', 'page={}'.format(i))
                    yield Request(url=final,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},
                                  callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath('//div[@class="infocontent"]//td/div/p[last()]/span/text()').extract()
        title = response.xpath('//div[@class="info"]//h1/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime[0].replace('.', '-').strip())
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
        item['area'] = u'中国'
        item['source'] = u'湘电集团有限公司'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//div[@class="infocontent"]').extract()
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


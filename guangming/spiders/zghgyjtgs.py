# -*- coding: utf-8 -*-
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


class Zghgyjtgs(scrapy.Spider):
    name = "zghgyjtgs"  # 中国核工业集团公司
    start_urls = [
        'http://ecp.cnnc.com.cn/xzbgg/index.jhtml PN',  # 招标公告
        'http://ecp.cnnc.com.cn/xfzbgg/index.jhtml PN',  # 非招标公告
        'http://ecp.cnnc.com.cn/xjggs/index.jhtml RN',  # 结果公示
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":5}

    def __init__(self, start_url=None,history=True):
        super(Zghgyjtgs, self).__init__()
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
        data_list = response.xpath('//div[@class="List1"]/ul/li')
        for each in data_list:
            url = each.xpath('./a/@href').extract()[0]
            pubtime = each.xpath('./span[1]/text()').re('\d+-\d+-\d+')[0]
            title = each.xpath('./a/text()').extract()[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page_rule = response.xpath(u'//a[contains(text(), "尾页")]/@href').extract()
            if len(page_rule) > 0:
                total_page = re.search(r'\d+', page_rule[0]).group()
                for i in range(2, int(total_page)+1):
                    final = response.url.replace('.jhtml', '_{}.jhtml'.format(i))
                    yield Request(url=final, method='get', meta={'ba_type':response.meta['ba_type'],'page_parse':False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath('//div[@class="Padding10 TxtCenter Gray"]/text()[1]').extract()
        title = response.xpath('//div[not(@class="Contnet")]/h1/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{2}-\d{2}\s\d{2}:\d{2}', pubtime[0]).group()
        else:
            item["pubtime"] = response.meta["pubtime"]
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'中国'
        item['source'] = u'中国核工业集团有限公司电子商务平台'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//div[@class="Contnet"]').extract()
        item['content'] = content[0]
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

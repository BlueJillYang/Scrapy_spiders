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

class Zjwzohqzf(scrapy.Spider):
    name = "zjwzohqzf_01"
    start_urls = [
        # 'http://ohztb.ouhai.gov.cn/ohcms/zcggcggs/index.htm PN',  # 采购公示
        # 'http://ohztb.ouhai.gov.cn/ohcms/zfcgcggg/index.htm PN',  # 采购公告
        # 'http://ohztb.ouhai.gov.cn/ohcms/zfcgdybc/index.htm CN',  # 澄清公告
        # 'http://ohztb.ouhai.gov.cn/ohcms/zfcgzbgg/index.htm RN',  # 结果公告
        # 'http://ohztb.ouhai.gov.cn/ohcms/zfcgcght/index.htm RN',  # 合同公告
        # 'http://ohztb.ouhai.gov.cn/ohcms/zfcglyys/index.htm RN',  # 履约验收公告
        # 理论1157条 实际1157
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False,
                       "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15}

    def __init__(self, start_url=None,history=False):
        super(Zjwzohqzf, self).__init__()
        jobs = start_url.split('|')
        for job in jobs:
            self.post_params.append({"url": job.split()[0],"ba_type": job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def start_requests(self):
        # proxy_list = self.configure.get_proxy_from_api(domain="common")
        # proxy = random.choice(proxy_list)
        for channel in self.post_params:
            url = channel['url']
            # yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True,"proxy":proxy},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//ul[contains(@class, "list-box")]/li/ul/li')
        for each in data_list:
            url = each.xpath('./a/@href').extract()[0]
            pubtime = each.xpath('./span/text()').re('\d+-\d+-\d+')[0]
            title = each.xpath('./a/@title').extract()[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime, 'title': title, "proxy": response.meta["proxy"]},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page_rule = response.xpath('//div[contains(@class, "Zy-Page")]/ol/li[last()]/a/@href').extract()
            if len(page_rule) > 0:
                page_rule = page_rule[0]
                if re.search(r'\d+', page_rule):
                    count = int(re.search(r'\d+', page_rule).group())
                    for i in range(2,int(count)+1):
                        page_url = response.url.replace('.htm', '_{}.htm'.format(i))
                        yield Request(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False,"proxy": response.meta["proxy"]},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.xpath('//span[@class="Bold"]/text()').extract()
        if len(item['title']) > 0:
            item['title'] = item['title'][0].strip()
        else:
            item['title'] = response.meta['title'].strip()
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
        item['area'] = u'浙江省温州市瓯海区'
        item['source'] = u'瓯海区人民政府'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = '//div[@class="Main-p"]'
        item['content'] = response.xpath(content).extract()[0]
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass


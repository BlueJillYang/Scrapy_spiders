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
from scrapy.http import Request
import urlparse
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


class jsczzlqzf(scrapy.Spider):
    name = "jsczzlqzf"
    start_urls = [
        'http://zl.changzhou.gov.cn/class/FPKDLMNL/1&template=templates/czzl/xxgk_class_min.html PN',
    ]
    Debug = True
    doredis = True
    source = u"钟楼区政府"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self, start_url=None, history=True):
        super(jsczzlqzf, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            print job
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        self.history = history
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
          yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"]},callback=self.parse_link)

    def parse_link(self, response):
        urls=response.xpath("//a[@onmouseover]/@href").extract()
        titles=response.xpath("//a[@onmouseover]/text()").extract()
        print urls
        for index,url in enumerate(urls):
            final = urlparse.urljoin(response.url,url)
            title = titles[index]
            if u'配发' not in title and u'价格表' not in title and u'配送' not in title and \
                u'清单' not in title and u'目录' not in title and u'通知' not in title:
                # if self.doredis and self.expire_redis.exists(final):
                #     continue
                yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"]},callback=self.parse_item)
        if self.history:
            page_rule = response.xpath('//div[@class="FX_PageDiv"]/div/span[2]/text()').extract()
            if len(page_rule) > 0:
                total_page = int(page_rule[0])
                for i in range(2, total_page+1):
                    final_url = re.sub(r'\d+', str(i), response.url)
                    yield Request(url=final_url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_link)

    def parse_item(self, response):
        item=DataItem()
        item["pubtime"]=response.xpath("//*[@class='GovInfoHead']/../../tr[5]/td[2]/text()").extract()[0] + " 00:00"
        item["type"]=response.meta["ba_type"]
        item['area'] = u'江苏省常州市钟楼区'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath("//*[@class='GovInfoHead']/../../tr[1]/td/text()").extract()[0]
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
        item['content'] = response.xpath("//td[@class='GovInfoContent']").extract()[0]
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item

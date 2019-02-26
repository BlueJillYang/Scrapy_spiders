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
from scrapy.utils.response import get_base_url
from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime,create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class jsycdfggzyjyw(scrapy.Spider):
    name = "jsycdfggzyjyw"
    start_urls = [
        # 'http://www.dfggzy.com/dfweb/jyxx/005001/005001001/ PN',
        # 'http://www.dfggzy.com/dfweb/jyxx/005001/005001003/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005001/005001004/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005001/005001005/ RN',
        'http://www.dfggzy.com/dfweb/jyxx/005001/005001006/ FN',
        'http://www.dfggzy.com/dfweb/jyxx/005001/005001007/ RN',
        'http://www.dfggzy.com/dfweb/jyxx/005002/005002001/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005002/005002003/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005002/005002004/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005002/005002005/ RN',
        'http://www.dfggzy.com/dfweb/jyxx/005002/005002006/ FN',
        'http://www.dfggzy.com/dfweb/jyxx/005003/005003001/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005003/005003003/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005003/005003004/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005003/005003005/ RN',
        'http://www.dfggzy.com/dfweb/jyxx/005003/005003006/ FN',
        'http://www.dfggzy.com/dfweb/jyxx/005004/005004001/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005004/005004001/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005004/005004001/ RN',
        'http://www.dfggzy.com/dfweb/jyxx/005005/005005001/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005005/005005003/ RN',
        'http://www.dfggzy.com/dfweb/jyxx/005006/005006001/ PN',
        'http://www.dfggzy.com/dfweb/jyxx/005006/005006003/ FN',
        'http://www.dfggzy.com/dfweb/jyxx/005006/005006004/ RN',
    ]
    Debug = True
    doredis = True
    source = u"大丰公共资源交易网"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self, start_url = None):
        super(jsycdfggzyjyw, self).__init__()
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
          yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"]},callback=self.parse_link)

    def parse_link(self, response):
        url = re.search(r'<iframe id="iframe" .* src="(.*aspx?)" .*>',response.body)
        if url:
            iframe = urlparse.urljoin(response.url,url.group(1))
            yield Request(url=iframe,method='get',meta={"ba_type":response.meta["ba_type"]},callback=self.parse_iframe)
        else:
            urls = response.xpath("//a[@title]/@href").extract()
            pubtimes = response.xpath("//a[@title]/../../td[3]/text()").extract()
            for index,url in enumerate(urls):
                final = urlparse.urljoin(response.url,url)
                # if self.doredis and self.expire_redis.exists(final):
                #     continue
                pubtime = pubtimes[index].strip() + " 00:00"
                yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime},callback=self.parse_item)

    def parse_iframe(self,response):
        urls = response.xpath("//form/table//tr/td/a[@target]/@href").extract()
        pubtimes = response.xpath("//form/table//tr/td/a[@target]/../../td[3]/text()").extract()
        for index,url in enumerate(urls):
            final=urlparse.urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            pubtime = pubtimes[index].strip() + " 00:00"
            yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()

        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市大丰'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath("//td[@id='tdTitle']/font/b/text()").extract()[0].strip()
        item['content'] = response.xpath("//table[@id='tblInfo']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item

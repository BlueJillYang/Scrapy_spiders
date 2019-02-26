#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import re
import sys
import time
import traceback
import urllib
import urlparse
import codecs
import redis
import requests
import scrapy
from scrapy import Selector
from scrapy import signals
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.utils.response import get_base_url
# from SpeciSpiders.items import DataItem
# from bc_crawler.configs.special_config import SpecialConfig
# from scrapy.xlib.pydispatch import dispatcher
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Linzhou_gov(scrapy.Spider):
    name = "linzhou_gov"  # 红旗渠网
    start_urls = [
        'http://www.linzhou.gov.cn/viewCmsCac.do?cacId=ff8080814486e89f0144950c45400114 news',
        'http://www.linzhou.gov.cn/viewCmsCac.do?cacId=ff8080814486e89f01449511c1b2012c news',
        'http://www.linzhou.gov.cn/viewCmsCac.do?cacId=ff8080814486e89f01449511c1b7012d news',
        'http://www.linzhou.gov.cn/viewCmsCac.do?cacId=ff8080814486e89f01449511c1bb012e news',
    ]
    source = u'红旗渠网'
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Linzhou_gov, self).__init__()
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
            cacId = re.search(r'cacId=(.+)', url).group(1)
            requestUrl = re.search(r'(http.+\.do)\?', url).group(1)
            post_url = 'http://www.linzhou.gov.cn/getHtmlInDivNormal.do?ajaxform'
            formdata = {
                'gwcsCode': 'undefined',
                'divId': '8a8a8a824555d4e00145682824e01970pagelist',
                'requestUrl': requestUrl,
                'cacId': cacId,
                'queryString': 'cacId={}'.format(cacId),
            }
            print formdata
            yield FormRequest(url=post_url,formdata=formdata,dont_filter=True,meta={'ba_type':channel['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        url_list = re.findall(r'"(sitegroup.+?\.html)"', response.body)
        for url in url_list:
            url = urlparse.urljoin(response.url, url)
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'河南省安阳市林州市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        pubtime = response.xpath('//div[@class="context"]/text()[4]').extract()[0]
        medianame = re.search(ur'来源[:：]\s*?(\S+)', pubtime)
        pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}', pubtime).group()
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
        title = response.xpath('//div[@class="context"]/ancestor::table//tr/td/table//tr/td/div/text()[1]').extract()
        if len(title) > 0:
            title = title[0]
        else:
            title = response.meta.get('title')
        item['title'] = title.strip()
        if medianame:
            item['medianame'] = medianame.group(1)
        else:
            item['medianame'] = u'红旗渠网'
        content = response.xpath('//table[@class="context"][1]').extract() or \
                  response.xpath('//table[@class="rerybg"]').extract()
        item['content'] = content[0]

        print item['url'], item['title'], item['pubtime'], item['medianame']
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item



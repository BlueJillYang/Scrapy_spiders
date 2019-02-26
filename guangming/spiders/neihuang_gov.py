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


class Neihuang_gov(scrapy.Spider):
    name = "neihuang_gov"  # 内黄县政府
    start_urls = [
        'http://www.neihuang.gov.cn/viewCmsCac.do?cacId=ff80808157e4d5fd0157fac341d8129a news',
        'http://www.neihuang.gov.cn/viewCmsCac.do?cacId=ff80808157e4d5fd0157fac37662129f news',
        'http://www.neihuang.gov.cn/viewCmsCac.do?cacId=ff80808157e4d5fd0157fac3a17d12a4 news',
        'http://www.neihuang.gov.cn/mailboxList.do?type=1 news',
    ]
    source = u'内黄县政府'
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Neihuang_gov, self).__init__()
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
            if 'mailboxList' in url:
                yield Request(url=url,method='get',meta={'ba_type':channel['ba_type']},callback=self.parse_link)
            else:
                cacId = re.search(r'cacId=(.+)', url).group(1)
                post_url = 'http://www.neihuang.gov.cn/getHtmlInDivNormal.do?ajaxform'
                formdata = {
                    'gwcsCode': 'undefined',
                    'divId': '5a9c10aa499dbf7401499ddb21b10037pagelist',
                    'requestUrl': 'http://www.neihuang.gov.cn/viewCmsCac.do',
                    'cacId': cacId,
                    'queryString': 'undefined',
                }
                print formdata
                yield FormRequest(url=post_url,formdata=formdata,dont_filter=True,meta={'ba_type':channel['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        url_list = re.findall(r'"(sitegroup.+?\.html)"', response.body)
        data_list = response.xpath('//table[@class="rerybg"][2]//tr/td[3]/a')
        for url in url_list:
            url = urlparse.urljoin(response.url, url)
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_item)
        for data in data_list:
            url = data.xpath('./@href').extract()[0]
            title = data.xpath('./text()').extract()[0]
            pubtime = data.xpath('./../../td[4]/text()').extract()[0].strip()
            url = urlparse.urljoin(response.url, url)
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'title':title,'pubtime':pubtime},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'河南省安阳市内黄县'
        item['source'] = self.source
        item['medianame'] = u'内黄县政府'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        pubtime = response.meta.get('pubtime') or response.xpath('//div[@class="context"]/text()[4]').extract()[0]
        pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}', pubtime).group()
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
        title = response.xpath('//div[@class="context"]/ancestor::table//tr/td/table//tr/td/div/text()[1]').extract()
        if len(title) > 0:
            title = title[0]
        else:
            title = response.meta.get('title')
        item['title'] = title.strip()
        content = response.xpath('//table[@class="context"][1]').extract() or \
                  response.xpath('//table[@class="rerybg"]').extract()
        item['content'] = content[0]

        print item['url'], item['title'], item['pubtime']
        if item['pubtime'] and item['title'] and item['content']:
            if re.search(ur'信件查询!', item['content']):
                print '详情页无内容, ', item['url']
            else:
                yield item



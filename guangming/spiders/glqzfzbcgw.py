# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import datetime
import base64
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


class Glqzfzbcgw(scrapy.Spider):
    name = "glqzfzbcgw"  # 广陵区政府招标采购网  文字全部加密了
    start_urls = [
        'http://www.glcgw.gov.cn/news.asp?bigclassname=%B2%C9%B9%BA%B9%AB%B8%E6&smallclassname=%B9%AB%BF%AA%D5%D0%B1%EA PN',  # 采购公告-公开招标
        'http://www.glcgw.gov.cn/news.asp?bigclassname=%B2%C9%B9%BA%B9%AB%B8%E6&smallclassname=%D1%AF%BC%DB%B2%C9%B9%BA PN',  # 询价采购
        'http://www.glcgw.gov.cn/news.asp?bigclassname=%B2%C9%B9%BA%B9%AB%B8%E6&smallclassname=%D1%FB%C7%EB%D5%D0%B1%EA PN',  # 邀请招标
        'http://www.glcgw.gov.cn/news.asp?bigclassname=%B2%C9%B9%BA%B9%AB%B8%E6&smallclassname=%CD%F8%C9%CF%BE%BA%BC%DB PN',  # 网上竞价
        'http://www.glcgw.gov.cn/news.asp?bigclassname=%B2%C9%B9%BA%B9%AB%B8%E6&smallclassname=%B5%A5%D2%BB%C0%B4%D4%B4 PN',  # 单一来源
        'http://www.glcgw.gov.cn/news.asp?bigclassname=%B2%C9%B9%BA%B9%AB%B8%E6&smallclassname=%BE%BA%D5%F9%D0%D4%CC%B8%C5%D0 PN',  # 竞争性谈判
        'http://www.glcgw.gov.cn/news.asp?bigclassname=%D6%D0%B1%EA(%B3%C9%BD%BB)%B9%AB%B8%E6 RN',  # 中标（成交）公告
        'http://www.glcgw.gov.cn/news.asp?bigclassname=%C8%B7%B6%A8%B9%AB%B8%E6 CN',  # 公告 这个频道有CN 有RN 有PF
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":10,}

    def __init__(self,start_url=None,history=True):
        super(Glqzfzbcgw, self).__init__()
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
        data_list = response.xpath('//span[@class="bgline"]')
        for each in data_list:
            url = each.xpath('./../following-sibling::td[1]/a/@href').extract()[0]
            title = each.xpath('./../following-sibling::td[1]/a/text()').extract()[0]
            pubtime = each.xpath('./../following-sibling::td[2]/font/text()').extract()[0]
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime.replace('/','-').replace('.','-'))
            url = urljoin(response.url, url)
            if pubtime:
                pubtime = pubtime.group() + ' 00:00'
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,'pubtime':pubtime},
                          callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = response.xpath(u'//a[contains(text(), "尾页")]/@href').extract()
            if len(page_rule) > 0:
                total_page = re.search(r'page=(\d+)', page_rule[0]).group(1)
                for i in range(2, int(total_page)+1):
                    final = response.url + '&page={}'.format(i)
                    yield Request(url=final,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},
                                  callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath('//div[@class="text"]/h2/text()').extract()
        title = response.xpath('//div[@class="text"]/h1/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime[0].replace('.', '-').strip())
            if item['pubtime']:
                item['pubtime'] = item['pubtime'].group().strip() + ' 00:00'
            else:
                item['pubtime'] = response.meta['pubtime']
        else:
            item['pubtime'] = response.meta['pubtime']
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省扬州市广陵区'
        item['source'] = u'广陵区政府招标采购网 '
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//div[@class="text"]').extract()
        item['content'] = content[0]
        item['pubtime'] = datetime.datetime.strptime(item['pubtime'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")

        item['title'] = urllib.unquote(base64.b64decode(item["content"])).decode("utf-8")
        item['content'] = urllib.unquote(base64.b64decode(item["content"])).decode("utf-8")

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item['pubtime'], item['title'], response.url
            raise Exception('{} 字段缺失!!! pubtime:{}, title:{}'.format(response.url,item['pubtime'],item['title']))

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass


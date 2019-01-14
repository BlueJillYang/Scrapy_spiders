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


class Tjggzy(scrapy.Spider):
    name = "tjggzy"
    start_urls = [
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=87&beginTime=&endTime= PN',  # 政府采购-采购公告 4497
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=90&beginTime=&endTime= CN',  # 政府采购-更正公告 1081
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=88&beginTime=&endTime= RN',  # 政府采购-采购结果 5571
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=81&beginTime=&endTime= PN',  # 工程-招标公告 51608
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=83&beginTime=&endTime= RN',  # 工程-中标结果 37225
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=238&beginTime=&endTime= PN',  # 出让公告　1099
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=239&beginTime=&endTime= RN',  # 出让结果　936
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=246&beginTime=&endTime= CN', # 补充公告 223
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=97&beginTime=&endTime= PN',  # 国有产权-项目公告 1155
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=100&beginTime=&endTime= RN', # 交易公告 1634
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=256&beginTime=&endTime= PN',  # 农村产权-交易公告 639
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=257&beginTime=&endTime= PN', # 农村承包土地经营权 98
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=258&beginTime=&endTime= PN',  # 农村经营性资产 129
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=259&beginTime=&endTime= PN',  #　集体资源性资产468
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=261&beginTime=&endTime= PN',  # 其他 77
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=248&beginTime=&endTime= PN',  # 矿业-出让 6
        # 'http://ggzy.xzsp.tj.gov.cn/queryContent_1-jyxx.jspx?title=&inDates=&ext=&ext1=&origin=&channelId=249&beginTime=&endTime= RN',  # 矿业-出让结果 6
        # 理论106452条 实际条
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url=None,history=True):
        super(Tjggzy, self).__init__()
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
        data_list = response.xpath('//ul[@class="article-list2"]/li/div')
        print len(data_list)
        for each in data_list:
            url = each.xpath('./a/@href').extract()[0]
            pubtime = each.xpath('./div/text()').re('\d+-\d+-\d+')[0]
            title = each.xpath('string(./a)').extract()[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            print url,  '  pubtime: ', pubtime
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime, 'title': title},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page_rule = response.xpath('//div[@class="page"]/a[last()]/@href').extract()
            print page_rule
            if len(page_rule) > 0:
                page_rule = page_rule[0]
                if re.search(r'&page=(\d+)', page_rule):
                    count = int(re.search(r'&page=(\d+)', page_rule).group(1))
                    for i in range(2,int(count)+1):
                        page_url = response.url + '&page={}'.format(i)
                        print page_url
                        yield Request(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.xpath('//div[@class="Titinfo"]/h2/text()').extract()
        if len(item['title']) > 0:
            item['title'] = item['title'][0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'天津市'
        item['source'] = u''
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = '//div[@id="printArea"]'
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


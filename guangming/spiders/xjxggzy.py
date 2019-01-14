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


class Xjxggzy(scrapy.Spider):
    name = "xjxggzy"
    start_urls = [
        ### 'http://xj.dzzyjy.gov.cn/TPFront_xiajin/xmxx/004002/004002003/004002003011/ RN',  # 重复
        # 'http://xj.dzzyjy.gov.cn/TPFront_xiajin/xmxx/004001/004001001/004001001011/ PN',  # 160/207
        # 'http://xj.dzzyjy.gov.cn/TPFront_xiajin/xmxx/004001/004001002/004001002011/ CN',  # 52/52
        # 'http://xj.dzzyjy.gov.cn/TPFront_xiajin/xmxx/004001/004001003/004001003011/ RN',  # 224/224
        # 'http://xj.dzzyjy.gov.cn/TPFront_xiajin/xmxx/004001/004001005/004001005011/ PN',  # 151/154
        # 'http://xj.dzzyjy.gov.cn/TPFront_xiajin/xmxx/004002/004002002/004002002011/ CN',  # 75/75
        # 'http://xj.dzzyjy.gov.cn/TPFront_xiajin/xmxx/004002/004002003/004002003011/ RN',  # 180/307
        # 'http://xj.dzzyjy.gov.cn/TPFront_xiajin/xmxx/004002/004002005/004002005011/ PN',  # 199/224
        # 'http://xj.dzzyjy.gov.cn/TPFront_xiajin/xmxx/004002/004002006/004002006011/ RN',  # 125/125
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=True):
        super(Xjxggzy, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        self.count_num = 0
        self.final = []
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
        data_list = response.xpath('//div[@class="ewb-right-info"]/div/table//tr')
        print 'len(data_list): ', len(data_list)
        if len(data_list) == 0:
            print 'url规则不对'
            raise Exception('没有合适的url规则!!! ')
        # print data_listmeta
        for each in data_list:
            url = each.xpath('./td/a[@class="ewb-list-name"]/@href').extract()[0]
            pubtime = each.xpath('./td[@align="right"]/font/text()').re('\d+-\d+-\d+')[0]
            title = each.xpath('./td/a[@class="ewb-list-name"]/@title').extract()[0]
            url = urljoin(response.url,url)
            # print url
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            self.final.append(url)
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime, 'title': title},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            if response.xpath(ur'//td[contains(text(), "末页")]/@title').re('\d+'):
                count = int(response.xpath(ur'//td[contains(text(), "末页")]/@title').re('\d+')[0])
                print '总页数: %d'%count
                page = count
                for i in range(2,int(page)+1):
                    page_url = response.url + '?Paging=%d'%i
                    print '正在处理翻页 %s'%page_url
                    yield Request(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        self.count_num += 1
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'山东省德州市夏津县'
        item['source'] = u'夏津县公共资源交易中心'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        #  根据类型 选择content规则
        a_href = response.url
        if '004001001011' in response.url:
            content = '//div[@id="menutab_6_1"]//*[contains(@id,"_content")]'
        elif '004001002011' in a_href:
            content = '//div[@id="menutab_6_2"]//*[contains(@id,"_content")]'
        elif '004001003011' in a_href:
            content = '//div[@id="menutab_6_3"]//*[contains(@id,"_content")]'
        elif '004002002011' in a_href:
            content = '//div[@id="menutab_6_2"]//*[contains(@id,"_content")]'
        elif '004002003011' in a_href:
            content = '//div[@id="menutab_6_3"]//*[contains(@id,"_content")]'
        elif '004002006011' in a_href:
            content = '//div[@id="menutab_6_4"]//*[contains(@id,"_content")]'
        else:
            content = '//div[@id="mainContent"]'
        item['content'] = response.xpath(content).extract()[0]
        # print item
        if item['pubtime'] and item['title'] and item['content']:
            print '成功处理 %d条'%self.count_num,  '  去重后%d  总共%d'%(len(set(self.final)), len(self.final))
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass


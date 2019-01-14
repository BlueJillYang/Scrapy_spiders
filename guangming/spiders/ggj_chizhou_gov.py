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


class Ggj_chizhou_gov(scrapy.Spider):
    name = "ggj_chizhou_gov"
    start_urls = [
        # 理论21480条　实际21414 采集率99.69%
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001007/002001007001/ PF', # 23+5
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001007/002001007002/002001007002002/ PF', # 1
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001001/002001001001/ PN', # 113*23+20
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001001/002001001002/002001001002001/ PN', # 20*23+22
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001001/002001001002/002001001002002/ PN', # 14*23+15
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001001/002001001002/002001001002003/ PN', # 25*23+22
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001001/002001001002/002001001002004/ PN', # 12*23
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001002/002001002001/ RN', # 65*23+13
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001002/002001002002/002001002002001/ RN', # 5*23+11
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001002/002001002002/002001002002002/ RN', # 3*23+17
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001002/002001002002/002001002002003/ RN', # 9*23+16
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001002/002001002002/002001002002004/ RN', # 23+9
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001003/002001003001/ RN', # 68*23+22
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001003/002001003002/002001003002001/ RN', # 22*23+22
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001003/002001003002/002001003002002/ RN', # 23*13+13
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001003/002001003002/002001003002003/ RN', # 21*23+3
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001003/002001003002/002001003002004/ RN', # 3*23
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001005/002001005001/ CN',  # 49*23
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001005/002001005002/002001005002001/ CN', # 3*23+19
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001005/002001005002/002001005002002/ CN', # 23+18
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001005/002001005002/002001005002003/ CN', # 6*23+1
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001005/002001005002/002001005002004/ CN', # 23+12
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001010/002001010001/ RN', # 2*23+17
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001010/002001010002/002001010002002/ RN', # 23+9
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002001/002001010/002001010002/002001010002003/ RN', # 5
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002005/002002005001/ PF', # 23*10+6
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002005/002002005002/002002005002001/ PF', # 20
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002005/002002005002/002002005002002/ PF', # 23+19
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002005/002002005002/002002005002003/ PF', # 23
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002005/002002005002/002002005002004/ PF', # 22
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002001/002002001001/ PN', # 98*23+12
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002001/002002001002/002002001002001/ PN', # 23*23+3
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002001/002002001002/002002001002002/ PN', # 20*23+15
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002001/002002001002/002002001002003/ PN', # 28*23+13
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002001/002002001002/002002001002004/ PN', # 25*23+22
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002007/002002007001/ RN', # 2*23+1
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002007/002002007002/002002007002001/ RN', # 20
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002007/002002007002/002002007002002/ RN', # 8
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002007/002002007002/002002007002003/ RN', # 8
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002007/002002007002/002002007002004/ RN', # 23+9
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002003/002002003001/ RN', # 70*23+9
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002003/002002003002/002002003002001/ RN', # 18*23+18
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002003/002002003002/002002003002002/ RN', # 16*23+14
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002003/002002003002/002002003002003/ RN', # 17*23+15
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002003/002002003002/002002003002004/ RN', # 9*23+17
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002004/002002004001/ CN', # 29*23+5
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002004/002002004002/002002004002001/ CN', # 5*23
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002004/002002004002/002002004002002/ CN', # 2*23+4
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002004/002002004002/002002004002003/ CN', # 6*23+20
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002004/002002004002/002002004002004/ CN', # 14*23+14
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002006/002002006001/ RN', # 5*23+13
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002006/002002006002/002002006002001/ RN', # 2
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002006/002002006002/002002006002002/ RN', # 3
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002006/002002006002/002002006002003/ RN', # 23+2
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002002/002002006/002002006002/002002006002004/ RN', # 21
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002003/002003001/002003001001/ PN', # 5*23+11
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002003/002003001/002003001002/002003001002001/ PN', # 23+7
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002003/002003001/002003001002/002003001002002/ PN', # 2*23+9
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002003/002003001/002003001002/002003001002003/ PN', # 30
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002003/002003002/002003002001/ RN', # 4*23+4
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002003/002003002/002003002002/002003002002001/ RN', # 21
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002003/002003002/002003002002/002003002002002/ RN', # 23+6
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002003/002003002/002003002002/002003002002003/ RN', # 12*23+16
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002004/002004001/002004001001/ PN', # 7*23
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002004/002004002/002004002001/ PN', # 6*23+12
        # 'http://ggj.chizhou.gov.cn/chiztpfront/jyxx/002004/002004003/002004003001/ RN', # 5*23+1
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=True):
        super(Ggj_chizhou_gov, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        self.count = 0
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
        data_list = response.xpath('//ul[@class="wb-data-item"]/li')
        # data_list = response.xpath('//td[@class="cl3"]/table[2]/tr[not(@style)]').extract()
        print response.url, ' 找到',len(data_list), '条'
        # print data_listmeta
        for each in data_list:
            url = each.xpath('./div/a/@href').extract()[0]
            pubtime = each.xpath('./span/text()').re('\d+-\d+-\d+')[0]
            title = each.xpath('./div/a/@title').extract()[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            print url,  '  pubtime: ', pubtime
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime, 'title': title,
                                                     'head_url': response.url},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page_rule = response.xpath(u'//td[text()="末页"]/@title').extract()
            print 'page_rule', page_rule, response.url
            if len(page_rule) > 0:
                page_rule = page_rule[0]
                if re.search(r'\d+', page_rule):
                    count = int(re.search(r'\d+', page_rule).group())
                    for i in range(2,int(count)+1):
                        page_url = response.url + '?Paging=%d'%i
                        print page_url
                        print '处理翻页 %s'%page_url
                        yield Request(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        self.count += 1
        print '处理了%d条'%self.count
        head_url = response.meta['head_url']
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.meta['title']
        item["type"] = response.meta["ba_type"]
        item['area'] = u'安徽省池州市'
        item['source'] = u'全国公共资源交易平台（安徽省•池州市） 池州市公共资源交易监督管理局'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        if response.xpath('//div[contains(@id, "menu_6")]'):
            # content_type = response.xpath('//div[@class="ewb-pos"]/table/tbody/tr/td[2]/font[2]/a[3]/font/text()').extract()
            content_type = response.xpath(u'//*[text()="首页"]/ancestor::td/font[2]/a[3]/font/text()').extract()
            # print 'content_type', content_type, response.url
            if len(content_type) > 0:
                x_id = u'//div[contains(@id, "menu_")][contains(text(), "{}")][not(contains(text(), "预{}"))]'.format(content_type[0], content_type[0])
                content_id = response.xpath(x_id)
                # print 'content_id', content_id
                if len(content_id) > 0:
                    content_id = content_id[0].xpath('./@id').extract()
                    id = re.search(r'menu_(\d_\d)', content_id[0]).group(1)
                    # print 'id', id
                    aim_id = 'menutab_{}'.format(id)
                    # print 'aim_id', aim_id
                    content = '//div[@id="{}"]'.format(aim_id)
                    # print 'content', content
                    item['content'] = response.xpath(content).extract()[0]
            # else:
            #     print 'content找寻失败!!!!!!!!',response.url

        else:
            content = '//td[@id="TDContent"]'
            item['content'] = response.xpath(content).extract()[0]
        # print item
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        elif not item['content']:
            print '没有content'

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

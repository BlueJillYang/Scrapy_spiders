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


class Xdjtyxgs(scrapy.Spider):
    name = "xdjtyxgs_dlzb"  # 湘电集团有限公司
    start_urls = [
        'https://xemc.dlzb.com/gongcheng/ PN',  # 工程招标
        'https://xemc.dlzb.com/huowu/ PN',  # 货物招标
        'https://xemc.dlzb.com/fuwu/ PN',  # 服务招标
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":2,
                       "DOWNLOAD_TIMEOUT":5}

    # 这个网站要加proxies
    def __init__(self,start_url=None,history=True):
        super(Xdjtyxgs, self).__init__()
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
        data_list = response.xpath('//div/ul[@class="c_ul5"]/li/a')
        for each in data_list:
            url = each.xpath('./@href').extract()[0]
            title = each.xpath('./text()').extract()[0]
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            headers = {
                'Host': 'www.dlzb.com',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
            }
            cookies = self.get_cookies(response.headers)
            headers['Cookie'] = cookies[1]
            yield Request(url=url,method='get',headers=headers,cookies=cookies[0],
                          meta={"ba_type":response.meta["ba_type"],"title":title},callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = response.xpath(u'//a[contains(text(), "尾页")]/@href').extract()
            if len(page_rule) > 0:
                total_page = re.search(r'page-(\d+)', page_rule[0]).group(1)
                for i in range(2, int(total_page)+1):
                    final = response.url + 'page-{}.shtml'.format(i)
                    yield Request(url=final,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},
                                  callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath('//div[@class="h_40 t_c laiyuan"]/span/text()').extract() or \
                  response.xpath('//div[@class="copyright"]/i/text()').extract()
        pubtime1 = response.xpath('//*[@id="title"]/following-sibling::*[1]')
        title = response.xpath('//div[@id="title"]/text()').extract() or \
                response.xpath('//h1/text()').extract() or \
                response.xpath('//h2[@id="title"]/text()').extract() or \
                response.xpath('//*[@id="title"]/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{2}-\d{2}', pubtime[0]).group().strip() + ' 00:00'
        elif len(pubtime1) > 0 and len(pubtime) == 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{2}-\d{2}', pubtime1.xpath('string(.)').extract()[0]).group().strip() + ' 00:00'
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'中国'
        item['source'] = u'湘电集团有限公司'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//div[@id="content"]').extract()
        item['content'] = content[0]
        print item['pubtime'], item['title'], response.url
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def get_cookies(self, headers):
        # __jsluid / D3z_ipshow-23 / D3z_tin_num 参数需要变动
        count_num = random.choice(range(1,20))  # 这个参数要传，但是不能太大，太大了会被封
        init_cookies = {
            'UM_distinctid': '16825fe7bd90-0f1ac05ba870c-73216752-100200-16825fe7bdf1',
            ' Hm_lvt_c909c1510b4aebf2db610b8d191cbe91': '1546825662,1546845061',
            ' Hm_lpvt_c909c1510b4aebf2db610b8d191cbe91': '1546845304',
            ' __jsluid': '',  # 随代理ip随动
            ' D3z_vi-ds': 'd9be54eec12a5995806e0885d419536c',
            ' D3z_ipshow-23': '23-23',
            ' CNZZDATA1271464492': '1386665700-1546822705-%7C1546844379',
            ' D3z_tin_num': '22',
            ' D3z_ipshow-38': '38-2',
            ' D3z_ipshow-37': '37-1',
        }
        if headers.get('Set-Cookie'):
            # 获取ip的cookie
            init_cookies[' __jsluid'] = headers['Set-Cookie'].split('=')[1].split(';')[0]
        print init_cookies[' __jsluid']
        init_cookies[' D3z_ipshow-23'] = '23-{}'.format(count_num+1)
        init_cookies[' D3z_tin_num'] = '{}'.format(count_num)
        cookie_str = ''
        for index in range(0, len(init_cookies)):
            cookie_str += '{}={}; '.format(init_cookies.keys()[index].strip(), init_cookies.values()[index].strip())

        return init_cookies, cookie_str


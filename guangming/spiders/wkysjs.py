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


class Wkysjs(scrapy.Spider):
    name = "wkysjs"  # 五矿有色金属控股有限公司阳光购销平台
    start_urls = [
        'http://minmetalsec.com/home/listn/invite/id/16/type/1.html PN',  # 招标采购-物资
        'http://minmetalsec.com/home/listn/invite/id/27/type/1.html PN',  # 招标-工程
        'http://minmetalsec.com/home/listn/invite/id/28/type/1.html PN',  # 招标-服务
        'http://minmetalsec.com/home/listn/invite/id/29/type/9.html PN',  # 招标-其他
        'http://minmetalsec.com/home/listn/inquire/id/17/type/3.html PN',  # 询价-物资
        'http://minmetalsec.com/home/listn/inquire/id/31/type/3.html PN',  # 工程
        'http://minmetalsec.com/home/listn/inquire/id/32/type/3.html PN',  # 服务
        'http://minmetalsec.com/home/listn/inquire/id/33/type/9.html PN',  # 其他
        'http://minmetalsec.com/home/listn/inviteks.html PN',  # 销售招标
        'http://minmetalsec.com/home/listn/inviteks/id/392/type/9.html PN',  # 销售招标-其他
        'http://minmetalsec.com/home/listn/bid/id/18.html RN',  # 中标公告
        'http://minmetalsec.com/home/listn/abate/id/19.html RN',  # 废标公告
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":5}

    def __init__(self, start_url=None,history=True):
        super(Wkysjs, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history
        self.headers = {
            'Host': 'minmetalsec.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',headers=self.headers,meta={"ba_type":channel["ba_type"],"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//ul[@id="ajax-data"]/li') or \
                    response.xpath('//div[@class="nyxx_lb kuan"]/ul/li')
        print len(data_list), response.url
        for each in data_list:
            url = each.xpath('./a[1]/@href').extract()[0]
            title = each.xpath('string(./a[1])').extract()[0]
            url = urljoin(response.url, url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page_rule = response.xpath('//ul[@class="pagination"]/li[last()-1]/a/@href').extract()
            if len(page_rule) > 0:
                total_page = re.search(r'page=(\d+)', page_rule[0]).group(1)
                for i in range(2, int(total_page)+1):
                    final = response.url + '?page={}'.format(i)
                    print '处理翻页: {}'.format(final)
                    yield Request(url=final, headers=self.headers, method='get', meta={'ba_type':response.meta['ba_type'],'page_parse':False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath(u'//span[contains(text(), "发布时间")]/span/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{2}-\d{2}\s\d{2}:\d{2}', pubtime[0]).group()
        item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'中国'
        item['source'] = u'五矿有色金属控股有限公司阳光购销平台'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//div[@class="mt45"]').extract()
        item['content'] = content[0]
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

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


class Gzgywdqzf(scrapy.Spider):
    # 贵州贵阳乌当区政府
    name = "gzgywdqzf"
    start_urls = [
        'http://www.gzwd.gov.cn/zwgk/xxgkml/zdlygk/ggzypz/xxgk_list.html PN',  # 公共资源配置 很杂
        'http://www.gzwd.gov.cn/zwgk/xxgkml/zdlygk/zfcg/xxgk_list.html PN',  # 政府采购
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=True):
        super(Gzgywdqzf, self).__init__()
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
        data_list = response.xpath('//td[@class="tits"]')
        for data in data_list:
            url = data.xpath('./a/@href').extract()[0]
            title = data.xpath('./a/text()').extract()[0]
            pubtime = data.xpath('./following-sibling::td/text()').extract()[0]
            pubtime = pubtime + ' 00:00'
            if u'公示' in title or u'出让' in title or u'竞价' in title or u'成交' in title or \
                u'中标' in title or u'采购' in title or u'招标' in title or \
                u'预审' in title or u'预告' in title or u'挂牌' in title or \
                    u'公告' in title or u'结果' in title or u'更正' in title or \
                    u'废标' in title:
                if 'gyggzy' not in url and u'纪要' not in title and u'会议' not in title and 'ccgp' not in url\
                        and u'办法' not in title and u'目录' not in title:
                    yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime, 'title': title},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            total_page = re.search(r'createPageHTML.(\d+), 0, "xxgk_list"', response.body)
            if total_page:
                total_page = int(total_page.group(1))
                for i in range(2, total_page+1):
                    final_url = response.url.replace('.html', '_{}.html'.format(i))
                    yield Request(url=final_url,method='get',meta={"ba_type":response.meta["ba_type"], 'page_parse': False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        self.count += 1
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        if u'成交公' in item['title'] or u'结果' in item['title'] or u'中标' in item['title'] or \
                u'未入围' in item['title'] or u'失败公' in item['title'] or u'合同公' in item['title'] or \
                u'有关事宜公告' in item['title']:
            item['type'] = 'RN'
        elif u'变更' in item['title'] or u'澄清' in item['title'] or u'答疑' in item['title'] or \
                u'更正' in item['title']:
            item['type'] = 'CN'
        elif u'招标公' in item['title'] or u'磋商' in item['title'] or u'采购公' in item['title']:
            item['type'] = 'PN'
        elif u'预告' in item['title']:
            item['type'] = 'PF'
        item['area'] = u'贵州省贵阳市乌当区'
        item['source'] = u'中国贵阳乌当区人民政府网站'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['content'] = response.xpath('//div[@id="content"]').extract() or \
                          response.xpath('//div[@class="Article_zw"]').extract() or \
                          response.xpath('//div[@align="left"]/h3/following-sibling::div[1]').extract()
        if len(item['content']) > 0:
            item['content'] = item['content'][0]
        else:
            print 'content有问题:  %s'%response.url
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

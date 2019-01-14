# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import datetime
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


class Lsxzbcgw(scrapy.Spider):
    name = "lsxzbcgw"  # 涟水县招标采购网
    start_urls = [
        'http://www.lszbb.com/news.php?classid=5 PN',  # 工程类招标 1580
        'http://www.lszbb.com/news.php?classid=6 PN',  # 采购类招标 3601
        'http://www.lszbb.com/news.php?classid=7 PN',  # 产权交易招标 788
        'http://www.lszbb.com/news.php?classid=8 PN',  # 小型工程招标 3871
        'http://www.lszbb.com/news.php?classid=9 PN',  # 工程类最高限价 923
        'http://www.lszbb.com/news.php?classid=10 PN',  # 采购类最高限价 1
        'http://www.lszbb.com/news.php?classid=11 RN',  # 工程中标 2488
        'http://www.lszbb.com/news.php?classid=12 RN',  # 采购中标 2191
        'http://www.lszbb.com/news.php?classid=13 RN',  # 产权中标 417
        'http://www.lszbb.com/news.php?classid=14 RN',  # 小型工程中标 3112
        'http://www.lszbb.com/news.php?classid=15 RN',  # 工程评标结果 206
        'http://www.lszbb.com/news.php?classid=16 RN',  # 采购评标结果 0
        'http://www.lszbb.com/news.php?classid=17 RN',  # 采购合同公示 18
        'http://www.lszbb.com/news.php?classid=18 RN',  # 采购验收公示 1
        'http://www.lszbb.com/news.php?classid=30 CN',  # 采购更正广告 1
        'http://www.lszbb.com/news.php?classid=31 PN',  # 采购其他公告 0
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":5,}

    def __init__(self,start_url=None,history=True):
        super(Lsxzbcgw, self).__init__()
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
        data_list = response.xpath('/html/body/table[3]/tbody/tr/td[3]/table/tbody/tr[3]/td/table/tbody/tr/td/table[3]//a')
        print 'len(data): {}, {}'.format(len(data_list), response.url)
        for each in data_list:
            url = each.xpath('./@href').extract()[0]
            title = each.xpath('./text()').extract()[0]
            pubtime = each.xpath('./../following-sibling::td[1]/text()').extract()[0]
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime.replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '').strip())
            url = urljoin(response.url, url)
            if pubtime:
                pubtime = pubtime.group()
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,'pubtime':pubtime},
                          callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = response.xpath('//td[@valign="absmiddle"]')
            if len(page_rule) > 0:
                page_rule = page_rule.xpath('string(.)').extract()[0]
                total_page = re.search(ur'共\s?(\d+)\s?页', page_rule).group(1)
                if int(total_page) > 1:
                    for i in range(2, int(total_page)+1):
                        num = (i-1)*20
                        final = response.url + '&pagestart={}'.format(num)
                        yield Request(url=final,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},
                                      callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath('//span[@class="font_title"]/ancestor::tr[1]/following-sibling::tr[2]/td[2]/text()').extract()
        title = response.xpath('//span[@class="font_title"]/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime[0].replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '').strip())
            if item['pubtime']:
                item['pubtime'] = item['pubtime'].group().strip() + ' 00:00'
            else:
                item['pubtime'] = response.meta['pubtime'].strip() + ' 00:00'
        else:
            item['pubtime'] = response.meta['pubtime'].strip() + ' 00:00'
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省淮安市涟水县'
        item['source'] = u'涟水县招标采购网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//div[@id="text"]').extract()
        item['content'] = content[0]
        item['pubtime'] = datetime.datetime.strptime(item['pubtime'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item['pubtime'], item['title'], response.url
            raise Exception('{},{},{}'.format(response.url, item['pubtime'], item['title']))

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass


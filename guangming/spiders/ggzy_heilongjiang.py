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


class Ggzy_heilongjiang(scrapy.Spider):
    name = "ggzy_heilongjiang"
    start_urls = [
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=16&type=1 PN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=16&type=5 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=16&type=7 CN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=16&type=4 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=16&type=3 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=17&type=1 PN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=17&type=5 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=17&type=7 CN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=17&type=4 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=17&type=3 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=18&type=1 PN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=18&type=5 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=18&type=7 CN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=18&type=4 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=18&type=3 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=19&type=1 PN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=19&type=5 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=19&type=7 CN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=19&type=4 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=19&type=3 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=20&type=1 PN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=20&type=5 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=20&type=7 CN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=20&type=4 RN',
        'http://hljggzyjyw.gov.cn/trade/tradezfcg?cid=20&type=3 RN',

    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=True):
        super(Ggzy_heilongjiang, self).__init__()
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
        data_list = response.xpath('//div[@class="news_inf"]/div/ul/li')
        # data_list = response.xpath('//td[@class="cl3"]/table[2]/tr[not(@style)]').extract()
        print len(data_list)
        # print data_listmeta
        for each in data_list:
            url = each.xpath('./a/@href').extract()[0]
            pubtime = each.xpath('./span/text()').re('\d+-\d+-\d+')[0]
            title = each.xpath('./a/@title').extract()[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            print url,  '  pubtime: ', pubtime
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime, 'title': title},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page_rule = response.xpath('//div[@class="page"]/span[last()-1]')
            print page_rule
            if len(page_rule) > 0:
                page_rule = page_rule.xpath('string(.)').extract()[0]
                if re.search(ur'当前\d+/(\d+)', page_rule):
                    count = int(re.search(ur'当前\d+/(\d+)', page_rule).group(1))
                    page = count
                    print 'count', count
                    for i in range(2,int(page)+1):
                        page_url = response.url + '&pageNo=%d'%i
                        print page_url
                        print '处理翻页 %s'%page_url
                        yield Request(url=page_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        self.count += 1
        print '处理了%d条'%self.count
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.xpath('//div[@class="news_inf"]/h1/text()').extract()
        if len(item['title']) > 0:
            item['title'] = item['title'][0]
        else:
            item['title'] = response.meta['title']
        item["type"] = response.meta["ba_type"]
        if u'成交公' in item['title'] or u'结果' in item['title'] or u'中标' in item['title'] or \
                u'未入围' in item['title'] or u'失败公' in item['title'] or u'合同公' in item['title']:
            item['type'] = 'RN'
        elif u'变更' in item['title'] or u'澄清' in item['title'] or u'答疑' in item['title'] or\
                u'更正' in item['title']:
            item['type'] = 'CN'
        elif u'招标公' in item['title'] or u'磋商' in item['title'] or u'采购公' in item['title']:
            item['type'] = 'PN'
        elif u'预告' in item['title']:
            item['type'] = 'PF'
        item['area'] = u'黑龙江省'
        item['source'] = u'黑龙江公共资源交易信息网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = '//div[@id="contentdiv"]'
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

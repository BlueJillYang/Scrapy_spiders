#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import re
import time
import sys
import scrapy
import json
import redis
import urllib
import requests
import urlparse
import datetime
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import FormRequest
from scrapy.utils.response import get_base_url
from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime, create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class jshaqxzfcgw(scrapy.Spider):
    name = "jshaqxzfcgw"
    start_urls = [
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/kfq/zbgg/zbgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/kfq/qtgg/qtgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/lsx/zbgg/zbgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/lsx/qtgg/qtgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/xyx/zbgg/zbgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/jhx/zbgg/zbgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/jhx/qtgg/qtgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/hzx/zbgg/zbgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/hzx/qtgg/qtgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/czq/zbgg/zbgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/czq/qtgg/qtgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/hyq/zbgg/zbgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/hyq/qtgg/qtgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/qhq/zbgg/zbgg.html RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/xqgg/qhq/qtgg/qtgg.html RN',
    ]
    Debug = True
    doredis = True
    source = u"淮安政府采购网"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self, start_url=None, history=True):
        super(jshaqxzfcgw, self).__init__()
        self.histroy = history
        jobs = self.start_urls
        # jobs = start_url.split('|')
        for job in jobs:
            self.post_params.append({"url": job.split()[0], "ba_type": job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                                     port=self.configure.yq_filter_db_other.port,
        #                                     db=self.configure.yq_filter_db_other.db,
        #                                     password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            if self.histroy:
                if 'page=history' in channel['url']:
                    url = channel['url'].replace('page=history', 'page=1')
                elif '_history.html' in channel['url']:
                    url = channel['url'].replace('_history.html', '.html')
                else:
                    url = channel['url']
                yield FormRequest(url=url, meta={"ba_type": channel["ba_type"]},
                                  method='get', callback=self.parse_link)
                continue

            for i in range(1, int(self.histroy)+1):
                if 'page=history' in channel['url']:
                    url = channel['url'].replace('page=history', 'page=%s' % i)
                elif '_history.html' in channel['url']:
                    url = channel['url'].replace('_history.html', '_%s.html' % i)
                yield FormRequest(url=url, meta={"ba_type": channel["ba_type"]},
                                  method='get', callback=self.parse_link)

    def parse_link(self, response):
        urls = response.xpath("//tr/td/a[contains(@href, 'content')]/@href").extract()
        titles = response.xpath("//tr/td/a[contains(@href, 'content')]/text()").extract()
        for idx, url in enumerate(urls):
            url = urlparse.urljoin(response.url, url)
            title = titles[idx]
            if 'content' not in url:
                continue
            # if self.expire_redis.exists(url):
            #     continue
            yield Request(url, meta={"ba_type": response.meta["ba_type"], "title": title},
                          callback=self.parse_item)

    def parse_item(self, response):
        content = response.xpath("//font[@id='zoom']").extract()[0]
        ba_type = response.meta['ba_type']
        title = response.meta['title']
        item = DataItem()
        try:
            pubtime = re.compile(u'发布时间：(\d+-\d+-\d+)').search(response.body.decode(response.encoding)).group(1)
            pubtime += ' 00:00'
        except:
            pubtime = ''

        item["type"] = ba_type
        item['url'] = response.url
        item['pubtime'] = pubtime
        item['area'] = u'江苏淮安市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['title'] = title
        item['content'] = content

        if item['pubtime'] and item['title'] and item['content']:
            yield item

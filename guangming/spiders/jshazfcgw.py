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


class jshazfcgw(scrapy.Spider):
    name = "jshazfcgw"
    start_urls = [
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=9911&facolumnId=8799&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=77036&facolumnId=8799&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=77037&facolumnId=8799&pid=&&page=history PF',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=9912&facolumnId=8799&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=9913&facolumnId=8799&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=43516&facolumnId=8799&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=50056&facolumnId=8800&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=77038&facolumnId=8800&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=77039&facolumnId=8800&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=50057&facolumnId=8800&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=50058&facolumnId=8800&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=69656&facolumnId=8800&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=50059&facolumnId=8800&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=77041&facolumnId=77040&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=77042&facolumnId=77040&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=77044&facolumnId=77040&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=77045&facolumnId=77040&pid=&&page=history RN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/gzgg/gzgg.html CN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36662&facolumnId=36658&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36663&facolumnId=36658&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36661&facolumnId=36658&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36655&facolumnId=36652&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36656&facolumnId=36652&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36657&facolumnId=36652&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36649&facolumnId=36646&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36650&facolumnId=36646&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36651&facolumnId=36646&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36643&facolumnId=36640&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36644&facolumnId=36640&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36645&facolumnId=36640&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36637&facolumnId=36634&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36638&facolumnId=36634&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36639&facolumnId=36634&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36632&facolumnId=36628&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36633&facolumnId=36628&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36631&facolumnId=36628&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=55239&facolumnId=36628&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36625&facolumnId=36622&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36626&facolumnId=36622&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36627&facolumnId=36622&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36599&facolumnId=36597&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36600&facolumnId=36597&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=36598&facolumnId=36597&pid=&&page=history PN',
        'http://zfcgzx.huaian.gov.cn/web/zfcgzx/dynamicpage/cgxxgglb.jsp?columnId=55236&facolumnId=36597&pid=&&page=history PN',
    ]
    Debug = True
    doredis = True
    source = u"淮安政府采购网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {
        "CLOSESPIDER_TIMEOUT": 20800
    }

    def __init__(self, start_url=None, history=None):
        super(jshazfcgw, self).__init__()
        self.histroy = history
        # jobs = start_url.split('|')
        jobs = self.start_urls
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
            if not self.histroy:
                if 'page=history' in channel['url']:
                    url = channel['url'].replace('page=history', 'page=1')
                elif 'gzgg_history' in channel['url']:
                    url = channel['url'].replace('gzgg_history', 'gzgg_1')
                yield FormRequest(url=url, meta={"ba_type": channel["ba_type"]},
                                  method='get', callback=self.parse_link)
                continue

            for i in range(1, int(self.histroy)+1):
                if 'page=history' in channel['url']:
                    url = channel['url'].replace('page=history', 'page=%s' % i)
                elif 'gzgg_history' in channel['url']:
                    url = channel['url'].replace('gzgg_history', 'gzgg_%s' % i)
                yield FormRequest(url=url, meta={"ba_type": channel["ba_type"]},
                                  method='get', callback=self.parse_link)

    def parse_link(self, response):
        urls = response.xpath("//tr/td[1]/a/@href").extract()
        titles = response.xpath("//tr/td[1]/a/text()").extract()
        pubtime_list = response.xpath("//tr/td[2]/text()").extract()
        for idx, url in enumerate(urls):
            url = urlparse.urljoin(response.url, url)
            title = titles[idx]
            if 'content' not in url:
                continue
            pubtime = pubtime_list[idx]
            # if self.expire_redis.exists(url):
            #     continue
            yield Request(url, meta={"ba_type": response.meta["ba_type"], "title": title,
                                     "pubtime": pubtime},
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
            try:
                year = re.compile(u'(\d+)年\d+月\d+日').search(re.sub('<.*?>', '', content)).group(1)
            except:
                year = '2018'
            pubtime = year + "-" + response.meta['pubtime'].replace('/', '-').replace('(', '').replace(')', '') \
                      + " 00:00"

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

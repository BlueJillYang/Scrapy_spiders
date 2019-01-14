#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import json
import redis
import urllib
import requests
import urlparse
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import FormRequest
from scrapy.utils.response import get_base_url
from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
# from SpeciSpiders.items import DataItem
# from bc_crawler_ba.configs.special_config import SpecialConfig
# from bc_crawler_ba.sources.data_clean import create_pubtime,create_medianame
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class jsgyzf(scrapy.Spider):
    name = "jsgyzf"
    start_urls = [
        'http://gaoyou.yangzhou.gov.cn/gaoyou/gsgg/list.shtml PN',
    ]
    Debug = True
    doredis = True
    source = u"高邮市人民政府"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self, start_url = None):
        super(jsgyzf, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
          url = channel['url']
          # if self.doredis and self.expire_redis.exists(url):
          #    continue
          yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"], "page_parse": True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//div[@class="list-image"]/div')
        for index,data in enumerate(data_list):
            url = data.xpath('./a/@href').extract()[0]
            title = data.xpath('./a/text()').extract()[0]
            pubtime = data.xpath('./span/text()').extract()[0]
            if u"招标" in title or u'中标' in  title or u'工程' in title or \
                    u'公示' in title or u'公告' in title:
                final=urlparse.urljoin(response.url,url)
                print final
                # if self.doredis and self.expire_redis.exists(final):
                #     continue
                pubtime = pubtime + " 00:00"
                yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)
        if response.meta['page_parse']:
            page_rule = re.search(r"{createPageHTML.'page_div',(\d+)", response.body)
            print page_rule
            if page_rule:
                total_page = page_rule.group(1)
                print total_page
                for i in range(2, int(total_page)+1):
                    final = response.url.replace('.shtml', '_{}.shtml'.format(str(i)))
                    yield Request(url=final,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省高邮市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta["title"]
        # 只有一个频道 信息比较杂 需要判断一下type
        if u'成交公' in item['title'] or u'结果' in item['title'] or u'中标' in item['title'] or \
                u'未入围' in item['title'] or u'失败公' in item['title'] or u'合同公' in item['title'] or \
                u'结果有关事宜公告' in item['title'] or u'中止' in item['title'] or \
                u'终止' in item['title']:
            item['type'] = 'RN'
        elif u'变更' in item['title'] or u'澄清' in item['title'] or u'答疑' in item['title'] or \
                u'更正' in item['title'] or u'更改' in item['title']:
            item['type'] = 'CN'
        elif u'招标公' in item['title'] or u'磋商' in item['title'] or u'采购公' in item['title'] or \
                u'出让公告' in item['title']:
            item['type'] = 'PN'
        elif u'预告' in item['title']:
            item['type'] = 'PF'
        item['content'] = response.xpath("//ucapcontent").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item

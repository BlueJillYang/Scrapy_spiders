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


class jsczzfcgw(scrapy.Spider):
    name = "jsczzfcgw"
    start_urls = [
        # "http://zfcg.changzhou.gov.cn/html/ns/zfjzcg_cggg/index.html PN",#集中采购 600
        # "http://zfcg.changzhou.gov.cn/html/ns/zfjzcg_fsgs/index.html PN", # 600
        # "http://zfcg.changzhou.gov.cn/html/ns/zfjzcg_cjgg/index.html RN", # 600
        # "http://zfcg.changzhou.gov.cn/html/ns/zfjzcg_cgyg/index.html PF", # 225
        # "http://zfcg.changzhou.gov.cn/html/ns/zfjzcg_gzgg/index.html CN", # 600
        # "http://zfcg.changzhou.gov.cn/html/ns/fscg_cjgg/index.html RN", #分散采购 # 3
        # "http://zfcg.changzhou.gov.cn/html/ns/fscg_cggg/index.html PN", # 3
        # "http://zfcg.changzhou.gov.cn/html/ns/dlcg_gzgg/index.html CN",#代理采购 # 600
        # "http://zfcg.changzhou.gov.cn/html/ns/dlcg_fsgs/index.html PN", # 335
        # "http://zfcg.changzhou.gov.cn/html/ns/dlcg_cjgg/index.html RN", # 600
        # "http://zfcg.changzhou.gov.cn/html/ns/dlcg_cgyg/index.html PF", # 108
        # "http://zfcg.changzhou.gov.cn/html/ns/dlcg_cggg/index.html PN", # 600
        # "http://zfcg.changzhou.gov.cn/html/ns/cgr_02/index.html PN",#采购人 # 116
        # "http://zfcg.changzhou.gov.cn/html/ns/cgr_01/index.html PN", # 98
        # "http://zfcg.changzhou.gov.cn/html/ns/bmcg_gzgg/index.html CN",#部门采购 # 133
        # "http://zfcg.changzhou.gov.cn/html/ns/bmcg_fsgs/index.html PN", # 74
        # "http://zfcg.changzhou.gov.cn/html/ns/bmcg_cjgg/index.html RN", # 600
        # "http://zfcg.changzhou.gov.cn/html/ns/bmcg_cgyg/index.html PF", # 86
        # "http://zfcg.changzhou.gov.cn/html/ns/bmcg_cggg/index.html PN"  # 600
    ]
    Debug = True
    doredis = True
    source = u"常州市政府采购网"
    # configure = SpecialConfig()
    post_params = []

    def __init__(self, start_url=None,history=True):
        super(jsczzfcgw, self).__init__()
        jobs = self.start_urls
        # jobs = start_url.split('|')
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

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
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        urls = response.xpath("//td[@class='Text4']//a[@title]/@href").extract()

        for index,url in enumerate(urls):
            final = urlparse.urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(final):
            #     continue
            yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"]},callback=self.parse_item)

        lastPage = response.xpath("//title/text()").extract()[0]
        page = re.search("\(\d+/(\d+)\)",lastPage)
        if page:
            page = page.group(1)
            if self.history and int(page)>1 and response.meta["page_parse"]:
                for i in range(2, int(page)+1):
                    url = response.url.replace("index","index_"+str(i))
                    yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()

        # pubtime = response.xpath("//td[@style='border-top:1px solid #CCC']/text()[1]").extract()[0]
        pubtime = response.xpath(u'//td[contains(@style, "border-top:1px solid #CCC")][contains(text(), "发布日期")]/text()[1]').extract()[0]
        item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",pubtime).group(0)
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省常州市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.xpath("//td[@class='NewsTitle']/text()").extract()[0].strip()
        item['content']= response.xpath("//td[@class='NewsContent']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item


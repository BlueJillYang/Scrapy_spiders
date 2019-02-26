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
import datetime
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


class jsyczfcgw(scrapy.Spider):
    name = "jsyczfcgw"
    start_urls = [
        'http://czj.yancheng.gov.cn/col/col2391/index.html PN',  # 市级采购-采购预告（公示）有PN PF
        'http://czj.yancheng.gov.cn/col/col2392/index.html PN',  # 采购公告
        'http://czj.yancheng.gov.cn/col/col2393/index.html CN',  # 更正公告
        'http://czj.yancheng.gov.cn/col/col2394/index.html RN',  # 中标（成交）公告
        'http://czj.yancheng.gov.cn/col/col2395/index.html RN',  # 合同公示
        'http://czj.yancheng.gov.cn/col/col2399/index.html PN',  # 县级-采购预告（公示）有PN PF
        'http://czj.yancheng.gov.cn/col/col2400/index.html PN',  # 采购公告
        'http://czj.yancheng.gov.cn/col/col2401/index.html CN',  # 更正公告
        'http://czj.yancheng.gov.cn/col/col2402/index.html RN',  # 中标（成交）公告
        'http://czj.yancheng.gov.cn/col/col2403/index.html RN',  # 合同公示
    ]
    Debug = True
    doredis = True
    source = u"盐城市政府采购网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,"DOWNLOAD_DELAY":0.1}
    final = []

    def __init__(self,start_url=None,history=True):
        super(jsyczfcgw, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = re.findall(r'<a\s?href="(/art.+?html)"\s?target="_blank">(.+?)</a>.+?(20\d{2}.*?\d{2}.*?\d{2})</td>', response.body)
        # 备用re规则如下
        # '<![CDATA.+?<a\s?href="(/art.+?html)"\s?target="_blank">(.+?)</a></td>.+?<td\s?width=".+?"\s?align="center">(20\d{2}.*?\d{2}.*?\d{2})</td>\s+?</tr>]]>'
        print len(data_list)
        for each in data_list:
            url = each[0].strip()
            title = each[1]
            pubtime = each[2].replace(' ', '').strip() + ' 00:00'
            url = urlparse.urljoin(response.url,url)
            self.final.append(url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            print url, '  len(set(final)): ', len(set(self.final)), '  ', pubtime, title
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"], 'title': title, 'pubtime': pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            columnid = re.search(r'col(\d+)/', response.url).group(1)
            total_count = re.search(r'dataAfter.+totalRecord:(\d+)', response.body)
            print total_count.group()
            if total_count:
                total_count = total_count.group(1)
                if int(total_count) % 45 == 0:
                    total_page = int(total_count)//45
                else:
                    total_page = int(total_count)//45 + 1
                print total_page
                for i in range(1, int(total_page)):
                    post_url = 'http://czj.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?'
                    start_i = 1 + 45*i
                    end_i = 45 + 45*i
                    getData = {'startrecord': str(start_i), 'endrecord': str(end_i), 'perpage': '15'}
                    final_url = post_url + urllib.urlencode(getData)
                    formData = {
                        'col': '1', 'appid': '1', 'webid': '7', 'path': '/', 'columnid': str(columnid), 'sourceContentType': '1',
                        'unitid': '7729', 'webname': '盐城市财政局', 'permissiontype': '0'
                    }
                    # print final_url, formData
                    yield FormRequest(url=final_url,formdata=formData,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        pubtime = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', response.meta['pubtime'])
        if pubtime:
            item['pubtime'] = response.meta['pubtime']
        else:
            item['pubtime'] = datetime.datetime.strptime(response.meta['pubtime'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        title = response.xpath("//font[@color='null']/text()").extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        if u'预告' in item['title']:
            item['type'] = 'PF'
        content = response.xpath('//div[@class="Section0"]').extract() or \
                  response.xpath("//div[@class='cas_content']").extract() or \
                  response.xpath("//div[@class='TRS_Editor']").extract() or \
                  response.xpath("//td[@style='line-height:28px; font-size:14px; color:#444']").extract()
        item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item


# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import json
import redis
import random
import urllib
import datetime
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


class Dtsrmzf(scrapy.Spider):
    name = "dtsrmzf"  # 东台市人民政府 请求过快的时候会出验证码
    start_urls = [
        'http://dongtai.yancheng.gov.cn/col/col7372/index.html PN',  # 招标公告
        'http://dongtai.yancheng.gov.cn/col/col7837/index.html RN',  # 中标公告
        'http://dongtai.yancheng.gov.cn/col/col6910/index.html PN',  # 采购目录及指南
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":1,
                       "DOWNLOAD_TIMEOUT":5,}

    def __init__(self,start_url=None,history=True):
        super(Dtsrmzf, self).__init__()
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
        data_list = re.findall(r'<a href="(.+?html)">(.+?)</a>', response.body)
        for each in data_list:
            url = each[0].strip()
            title = each[1]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"], 'title': title},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            columid = re.search(r'\d+', response.url).group()
            total_count = re.search(r'dataAfter.+totalRecord:(\d+)', response.body)
            if total_count:
                total_count = total_count.group(1)
                if int(total_count) % 45 == 0:
                    total_page = int(total_count)//45
                else:
                    total_page = int(total_count)//45 + 1
                for i in range(1, int(total_page)):
                    post_url = 'http://dongtai.yancheng.gov.cn/module/web/jpage/dataproxy.jsp?'
                    start_i = 1 + 45*i
                    end_i = 45 + 45*i
                    getData = {'startrecord': str(start_i), 'endrecord': str(end_i), 'perpage': '15'}
                    final_url = post_url + urllib.urlencode(getData)
                    formData = {
                        'col': '1', 'appid': '1', 'webid': '49', 'path': '/', 'columnid': '{}'.format(columid), 'sourceContentType': '1',
                        'unitid': '25630', 'webname': '东台市人民政府', 'permissiontype': '0'
                    }
                    yield FormRequest(url=final_url,formdata=formData,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        print response
        item = DataItem()
        pubtime = response.xpath('//h1/following-sibling::ul/li/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', '')).group() + ' 00:00'
            item['pubtime'] = datetime.datetime.strptime(item['pubtime'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        item['title'] = response.xpath('//h1/text()').extract()
        if len(item['title']) > 0:
            item['title'] = item['title'][0]
        else:
            item['title'] = response.meta['title']
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市东台市'
        item['source'] = u'东台市人民政府'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = '//div[@class="content"]'
        item['content'] = response.xpath(content).extract()[0]
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            raise Exception('{}: 字段缺失！！！'.format(response.url))

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

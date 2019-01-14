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


class Zgnyjsjtyxgs(scrapy.Spider):
    name = "zgnyjsjtyxgs"  # 中国能源建设集团有限公司
    start_urls = [
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MQA=&bigType=WgBCAEcARwA= PN',  # 招标公告 761
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MQA=&bigType=QwBHAFkARwA= PF',  # 采购预告 3
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MgA=&bigType=QwBHAEcARwA=&smallType=aAB3AA== PN',  # 采购公告-货物采购 4080
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MgA=&bigType=QwBHAEcARwA=&smallType=ZwBjAA== PN',  # 工程分包 1856
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MgA=&bigType=QwBHAEcARwA=&smallType=ZgB3AA== PN',  # 服务采购 387
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MgA=&bigType=WgBCAEcAUwA=&smallType=aAB3AA== RN',  # 中标公示-货物采购 1262
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MgA=&bigType=WgBCAEcAUwA=&smallType=ZwBjAA== RN',  # 工程分包 344
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MgA=&bigType=WgBCAEcAUwA=&smallType=ZgB3AA== RN',  # 服务采购 215
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MgA=&bigType=WgBYAEcAUwA=&smallType=aAB3AA== RN',  # 中选公示-货物 628
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MgA=&bigType=WgBYAEcAUwA=&smallType=ZwBjAA== RN',  # 工程分包 84
        'http://ec.ceec.net.cn/HomeInfo/ProjectList.aspx?InfoLevel=MgA=&bigType=WgBYAEcAUwA=&smallType=ZgB3AA== RN',  # 服务采购 42
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":10}

    def __init__(self, start_url=None,history=True):
        super(Zgnyjsjtyxgs, self).__init__()
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
        data_list = response.xpath('//div[@class="list01"]/span[2]/a')
        for each in data_list:
            url = each.xpath('./@href').extract()[0]
            pubtime = each.xpath('./ancestor::span/following-sibling::span[@class="title02"]/text()').re('\d+-\d+-\d+')[0]
            title = ''.join(each.xpath('./@title').extract())
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime + " 00:00"
            # 采购预告的pubtime抓取出来是报名截止时间 去掉
            if response.meta['ba_type'] == 'PF':
                pubtime = ''
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page_rule = response.xpath('//span[@id="outMsg"]/text()').extract()
            if len(page_rule) > 0:
                total_count = int(page_rule[0])
                if total_count % 30 == 0:
                    total_page = total_count // 30
                else:
                    total_page = total_count // 30 + 1
                for i in range(2, int(total_page)+1):
                    final = response.url + '&PageD={}'.format(i)
                    print '处理翻页{}'.format(final)
                    yield Request(url=final, method='get', meta={'ba_type':response.meta['ba_type'],'page_parse':False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        if response.status != 200:
            raise Exception('出错了 status_code:{}'.format(response.status))
        if response.meta['ba_type'] == 'PF':
            pubtime = response.xpath(u'//*[contains(text(), "发布时间")]/text()[1]').extract()
            if len(pubtime) > 0:
                item['pubtime'] = re.search(r'20\d{2}-\d{2}-\d{2}\s\d{2}:\d{2}', pubtime[0]).group()
        else:
            item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'中国'
        item['source'] = u'中国能建电子采购平台'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta['title']
        content = response.xpath('//table[@class="TABLE_tab"]').extract() or \
                  response.xpath('//div[@align="center"]').extract()
        item['content'] = content[0]
        # print '{}'.format(item['url'])
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

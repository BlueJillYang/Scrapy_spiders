#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import re
import sys
import time
import random
import traceback
import urllib
import urlparse
import codecs
import redis
import requests
import scrapy
from scrapy import Selector
from scrapy import signals
from scrapy.http import FormRequest
from scrapy.http import Request
# from SpeciSpiders.items import DataItem
# from bc_crawler.configs.special_config import SpecialConfig
# from scrapy.utils.response import get_base_url
# from scrapy.xlib.pydispatch import dispatcher
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Changzhou_gov(scrapy.Spider):
    # 这个要加代理
    name = "changzhou_gov"  # 常州市人民政府
    start_urls = [
        'http://www.changzhou.gov.cn/talk/talk_history.php?isurban=1 news',  # 历史访谈-辖市区
        'http://www.changzhou.gov.cn/talk/talk_history.php?isurban=2 news',  # 历史访谈-市级

        'http://www.changzhou.gov.cn/page/?url=http://58.216.50.108:8087/webXinFang/jsp/szxj.jsp news',  # 市长信箱
        'http://www.changzhou.gov.cn/page/?url=http://58.216.50.108:8087/webXinFang/jsp/bmxj.jsp news',  # 部门信箱
    ]
    Debug = True
    doredis = True
    source = u"常州市人民政府"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.2,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Changzhou_gov, self).__init__()
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
        proxy_list = self.configure.get_proxy_from_api(domain="common")
        proxy = random.choice(proxy_list)
        for channel in self.post_params:
            url = channel['url']
            param = re.search(r'jsp/(.{2})xj\.jsp', url)
            if param:
                param = param.group(1)
                post_url = 'http://58.216.50.108:8087/webXinFang/memberController/cxxj.do'
                formdata = {'page': '1', 'cxnf': '', 'tszt': '', 'cxtj': param}
                yield FormRequest(url=post_url,formdata=formdata,meta={"ba_type":channel["ba_type"],"proxy":proxy},callback=self.parse_link)
            else:
                yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"]},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('/html/body/div[3]/table[2]//tr/td/table[2]//tr/td/table//tr/td/table//tr/td/strong/a')
        print len(data_list)
        if len(data_list) > 0:
            for data in data_list:
                url = data.xpath('./@href').extract()[0]
                title = data.xpath('./text()').extract()[0].strip()
                pubtime = data.xpath('../../../../tr[2]/td/text()').extract()[0]
                pre_content = data.xpath('./ancestor::table[1]').extract()[0]
                url_id = re.search(r'\d+', url).group()
                get_url = urlparse.urljoin(response.url, url)
                url = 'http://www.changzhou.gov.cn/talk/message_detail.php?theme_id={}&sort=asc'.format(url_id)
                yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'title':title,
                                                         'pubtime':pubtime,'pre_content':pre_content,'get_url':get_url},callback=self.parse_item)
        else:
            result = json.loads(response.body)['msg']
            print result
            for msg in result:
                url_id = msg['xfjbh']
                pubtime = msg['bjsj']
                url = 'http://58.216.50.108:8087/webXinFang/memberController/xjxq.do?xfjbh={}'.format(url_id)
                # 最好加个代理
                time.sleep(1.5)
                yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime,"proxy":response.meta['proxy']},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath('//table[@class="xfcxjg_Table"]//tr[1]/td[2]/text()').extract()
        if len(pubtime) > 0:
            pubtime = pubtime[0].strip()
        else:
            pubtime = response.meta['pubtime']
        pubtime = re.search(r'\d{4}.\d{1,2}.\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}', pubtime).group()
        item['pubtime'] = datetime.datetime.strptime(pubtime.replace('/', '-'), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
        title = response.xpath('//table[@class="xfcxjg_Table"]//tr[3]/td[2]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta.get('title')
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省常州市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['medianame'] = u'常州市人民政府'
        if response.meta.get('get_url'):
            item['url'] = response.meta['get_url']
        else:
            item['url'] = response.url
        content = response.xpath('//div[@id="message_area"]').extract() or \
                  response.xpath('//table[@class="xfcxjg_Table"]').extract()
        if response.meta.get('pre_content'):
            item['content'] = response.meta['pre_content'] + content[0]
        else:
            item['content'] = content[0]
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



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


class Zlzkzbpt(scrapy.Spider):
    name = "zlzkzbpt"  # 中联重科招标平台
    start_urls = [
        'http://zlzkzb.zoomlion.com/tender/mainPage?page=zbgg PN',  # 招标公告
        'http://zlzkzb.zoomlion.com/tender/mainPage?page=zbbgg CN',  # 招标变更公告
        'http://zlzkzb.zoomlion.com/tender/mainPage?page=tzgg PN',  # 通知公告
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":5}

    # 这个网站数据太少，还没体现出翻页规则
    def __init__(self, start_url=None,history=False):
        super(Zlzkzbpt, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

    def start_requests(self):
        post_url = 'http://zlzkzb.zoomlion.com/tender/anncet/getFroTenderAnncetList'
        for channel in self.post_params:
            url = channel['url']
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            formdata = {"page":1,"limit":10,"id":None,"tenderType":"0"}
            headers = {
                'Host': 'zlzkzb.zoomlion.com',
                # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'http://zlzkzb.zoomlion.com/tender/mainPage?page=zbgg',
                'Content-Type': 'application/json;charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
            }
            yield Request(url=post_url,body=json.dumps(formdata),method='post',headers=headers,  # cookies=cookies,
                              meta={"ba_type":channel["ba_type"],"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = json.loads(response.body_as_unicode())
        jsonDict = data_list['data']
        for each in jsonDict:
            url_id = each['id']
            url_type = each['tenderType']
            pubtime = each['pubTm']
            pubtime = re.search(r'20\d{2}-\d{2}-\d{2}\s\d{2}:\d{2}', pubtime).group()
            title = each['tenderTitle']
            url = 'http://zlzkzb.zoomlion.com/tender/anncet/getAnncetOrEditInfo?id={}&anncetType={}'.format(url_id, url_type)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            print url, pubtime
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        pubtime = response.xpath('//div[@class="detail-info"]/span[2]/text()').extract()
        title = response.xpath('//div[@class="detail-header"]/text()').extract()
        if len(pubtime) > 0:
            item['pubtime'] = re.search(r'20\d{2}-\d{2}-\d{2}\s\d{2}:\d{2}', pubtime[0]).group()
        else:
            item["pubtime"] = response.meta["pubtime"]
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'中国'
        item['source'] = u'中联重科招标平台'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//div[@class="deatil-content"]').extract()
        item['content'] = content[0]
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

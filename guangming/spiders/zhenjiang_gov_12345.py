#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import re
import sys
import time
import codecs
import traceback
import urllib
import urlparse
import codecs
import redis
import requests
import scrapy
# from SpeciSpiders.items import DataItem
# from bc_crawler.configs.special_config import SpecialConfig
from scrapy import Selector
from scrapy import signals
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.utils.response import get_base_url
# from scrapy.xlib.pydispatch import dispatcher
from ..items import DataItem
import execjs
import commands

reload(sys)
sys.setdefaultencoding('utf-8')


class Zhenjiang_gov_12345(scrapy.Spider):
    name = "zhenjiang_gov_12345"  # 镇江市12345公共服务热线
    start_urls = [
        'http://12345.zhenjiang.gov.cn/gzsq/wssq/ news',
    ]
    Debug = True
    doredis = True
    source = u"镇江市12345公共服务热线"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Zhenjiang_gov_12345, self).__init__()
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
            yield Request(url=url,method='get',meta={'ba_type':channel['ba_type']},callback=self.parse_cookie)

    def parse_cookie(self, response):
        url = 'http://12345.zhenjiang.gov.cn/zjxx/outMailList.action'  # 网上诉求
        formdata = {
            'mailBoxID': 'ff8080813af26209013af3806cb400ab',
            'isUser': 'false',
            'isSpecial': '0',
            'queryEqStepName': '%E5%85%AC%E5%BC%80%E5%8F%91%E5%B8%83',
            'queryUneqStepName': '',
            'sCondition': '',
            'cpage': '1',
            'len': '7',
        }
        yield FormRequest(url=url,formdata=formdata,meta={'ba_type':response.meta['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        # f**k 这个gbk编码
        result = json.loads(response.body.decode('gbk'))['pc']['list']
        for info in result:
            title = info['title']
            url_id = info['id']
            pubtime = info['insertTime']
            mailBoxID = info['mailBoxID']
            # 需要加密的字符串
            str_needEnc = " and ID = '{}' and mailBoxID = '{}'".format(url_id, mailBoxID)
            formdata = {'mailBoxID': mailBoxID, 'sCondition': self.strEnc(str_needEnc)}
            post_url = 'http://12345.zhenjiang.gov.cn/zjxx/outMailShow.action'
            yield FormRequest(url=post_url,dont_filter=False,formdata=formdata,meta={'ba_type':response.meta['ba_type'],'title':title,
                                                                   'pubtime':pubtime,'url_id':url_id,'mailBoxID':mailBoxID},callback=self.parse_json)

    def parse_json(self, response):
        result = json.loads(response.body.decode('gbk'))['mailMap']
        url = 'http://12345.zhenjiang.gov.cn/gzsq/wssq/xjnr/?id={}&mailBoxID={}'.format(response.meta['url_id'], response.meta['mailBoxID'])
        yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'title':response.meta['title'],
                                                 'pubtime':response.meta['pubtime'],'result':result},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省镇江市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['medianame'] = u'镇江市12345公共服务热线'
        item['url'] = response.url
        pubtime = response.meta['pubtime']
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M')
        item['title'] = response.meta['title'].strip()
        content = response.xpath('//table[@bgcolor="fafafa"]').extract()[0]
        lables = response.xpath('//table[@bgcolor="fafafa"]//td[@align="left"]/@id').extract()
        item['content'] = self.parse_content(content, lables, response.meta['result']['address']['form']['columns'])
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])

    def parse_content(self, content, labels, result):
        print labels
        for each in result:
            if each:
                # print each[u'columnName']
                if each[u'columnName'] in labels:
                    label_value = each['columnValue']
                    label_key = each['columnName']
                    content = re.sub(r'(?P<text>id="{}".*?>)'.format(label_key), r'\g<text>{}'.format(label_value), content)
        return content

    def strEnc(self, str_needEnc):
        js_code = self.get_js()
        ctx = execjs.compile(js_code)
        result = ctx.call('strEnc', str_needEnc, '1', '2', '3')
        # print result
        return result

    def get_js(self):
        f = codecs.open('/home/python/Desktop/Test_spiders/guangming/guangming/spiders/zhenjiang_gov_12345.js', 'r', encoding='utf-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr += line
            line = f.readline()
        return htmlstr


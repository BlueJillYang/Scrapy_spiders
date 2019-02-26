#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import re
import sys
import time
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

reload(sys)
sys.setdefaultencoding('utf-8')


class Wuxi_gov_12345(scrapy.Spider):
    name = "wuxi_gov_12345"  # 无锡市12345政府公共服务热线
    start_urls = [
        'http://xzfw.wuxi.gov.cn/intertidwebapp/LeadingMail/GOV_LeadingManageList news',  # 诉求件列表
    ]
    Debug = True
    doredis = True
    source = u"无锡市12345政府公共服务热线"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Wuxi_gov_12345, self).__init__()
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
            formdata = {
                'DoProjectID': 'bfffa273-086a-47cb-a7a8-7ae8140550db',
                'DoState': '2',
                'OpenState': '0',
                'PageSize': '15',
                'PageIndex': '1',
                'Keywords': '',
                'EndTime_Begin': '',
                'EndTime_End': '',
                'SearchID': '',
            }
            yield FormRequest(url=url,formdata=formdata,meta={'ba_type':channel['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        jsonDict = json.loads(response.body)['list']['list']
        for info in jsonDict:
            answerID = info['answerID']
            title = info['title']
            pubtime = info['beginTime']
            post_url = 'http://xzfw.wuxi.gov.cn/intertidwebapp/LeadingMail/Gov_LeadingInfo?AnswerID=' + answerID
            formdata = {}
            # 明明是POST请求，formdata为空 用GET请求也能获取数据
            yield FormRequest(url=post_url,formdata=formdata,meta={'ba_type':response.meta['ba_type'],'title':title,'pubtime':pubtime,'answerID':answerID},callback=self.parse_content)

    def parse_content(self, response):
        jsonDict = json.loads(response.body)['LinkMayorAskAnswerMainList']
        get_url = 'http://xzfw.wuxi.gov.cn/fzlm/hdjlgny/lxblgny/xjxq/index.shtml?AnswerID=' + response.meta['answerID']
        yield Request(url=get_url,method='get',meta={'ba_type':response.meta['ba_type'],'title':response.meta['title'],
                                                     'pubtime':response.meta['pubtime'],'jsonDict':jsonDict},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省无锡市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['medianame'] = u'无锡市12345政府公共服务热线'
        item['url'] = response.url
        pubtime = response.meta['pubtime'].replace('/', '-')
        item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d").strftime('%Y-%m-%d %H:%M')
        item['title'] = response.meta['title'].strip()

        # 拼接节点
        tips = re.findall(ur"htm \+=\s?'([^空]+?)';", response.body)
        jsonDict = response.meta['jsonDict'][0]
        content = ''
        for tip in tips:
            replace_param = re.search(r'\+josn\[i\]\.(.+?)\+', tip)
            if u'为空' in tip:
                pass
            elif replace_param:
                param_key = replace_param.group(1)
                param_value = jsonDict[param_key]
                new_tip = tip.replace("\'+josn[i].{}+\'".format(param_key), param_value)
                line = new_tip + '\n'
                content += line
            else:
                line = tip + '\n'
                content += line
        print content
        item['content'] = content

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])


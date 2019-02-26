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


class Lyg_gov_12345(scrapy.Spider):
    name = "lyg_gov_12345"  # 连云港12345在线
    start_urls = [
        'http://218.92.36.75:8081/WZ/jswebsite/pages/newdefault/list.html news',  # 典型案例
        'http://www.lyg.gov.cn/TrueCMS/visitorController/getDeptletterList.do?type=ybj&mailBoxId=d45bcbba-2f9a-4202-a050-a44ba8b1a4ed news',  # 主任信箱
        'http://xxgk.lyg.gov.cn/lygbcms/front/datacall/channel/info.do?iid=21&siteid=64&ctype=2&pagesize=17&cid=0 news',  # 公共服务中心
    ]
    Debug = True
    doredis = True
    source = u"连云港12345在线"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None):
        super(Lyg_gov_12345, self).__init__()
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
            if 'newdefault' in url:
                post_url = 'http://218.92.36.75:8081/WZ/rest/websiteCaseStatistics/getCaseList'
                get_url = url.rpartition('/')[0]
                formdata = {"params": json.dumps({"pageindex": 0, "pagesize": 10}), "token": ""}
                print formdata
                yield FormRequest(url=post_url,formdata=formdata,meta={"ba_type":channel["ba_type"],"get_url":get_url},callback=self.parse_link)
            else:
                yield Request(url=url,method='get',meta={'ba_type':channel['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        if 'getCaseList' in response.url:
            listInfo = json.loads(response.body)['custom']['listInfo']
            for info in listInfo:
                id = info['cserial']
                pubtime = info['case_date'].strip()
                title = info['case_title'].strip()
                get_url = response.meta['get_url'] + '/straightmatter.html?guid=' + id
                post_url = 'http://218.92.36.75:8081/WZ/rest/websiteCaseStatistics/getCaseDetial'
                formdata = {'params': json.dumps({"cguid": id}), 'token': ''}
                yield FormRequest(url=post_url,formdata=formdata,dont_filter=True,meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime,'title':title,'get_url':get_url},callback=self.parse_item)
        else:
            data_list = response.xpath('//div[@class="gajxj_con"]/table//tr//a')
            data_list1 = response.xpath('//div[@id="azmore1"]/table[4]//tr//a')
            if len(data_list) > 0:
                for data in data_list:
                    url = data.xpath('./@href').extract()[0]
                    pubtime = data.xpath('./../following-sibling::td[3]/text()').extract()[0].strip() + ' 00:00'
                    url = urlparse.urljoin(response.url, url)
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime},callback=self.parse_item)
            elif len(data_list1) > 0:
                for data in data_list1:
                    url = data.xpath('./@onclick').extract()[0]
                    url = re.search(r"window.open\('(http.+?html)'\)", url).group(1)
                    pubtime = data.xpath('./../following-sibling::td[last()]/text()').extract()[0].strip() + ' 00:00'
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省连云港市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['medianame'] = u'连云港12345在线'
        if 'websiteCase' in response.url:
            jsonDict = json.loads(response.body)['custom']['caseInfo']
            pubtime = jsonDict['createdate']
            item['pubtime'] = re.search(r'20\d{2}-\d{2}-\d{2}\s\d{2}:\d{2}', pubtime).group()
            item['title'] = jsonDict['rqsttitle']
            content = jsonDict['rqstcontent'] + '\n 处理结果: ' + jsonDict['endcontent']
            item['content'] = content
            item['url'] = response.meta['get_url']
        else:
            item['url'] = response.url
            pubtime = response.meta['pubtime']
            item['pubtime'] = datetime.datetime.strptime(pubtime, "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
            title = response.xpath('//div[@class="formContent"]/fieldset[1]/table//tr[1]/td[2]/text()').extract() or \
                    response.xpath('/html/body/table//tr/td[2]/table[3]//tr[4]/td[2]/text()').extract()
            item['title'] = title[0].strip()
            content = response.xpath('//div[@class="formContent"]').extract() or \
                      response.xpath('/html/body/table').extract()
            item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



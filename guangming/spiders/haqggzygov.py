# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import datetime
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


class Haqggzygov(scrapy.Spider):
    name = "haqggzygov"  # 淮安区招投标网
    start_urls = [
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001001/005001001001/MoreInfo.aspx?CategoryNum=005001001001 PN',  # 工程建设-招标公告-房屋建筑 418
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001001/005001001002/MoreInfo.aspx?CategoryNum=005001001002 PN',  # 市政基础 220
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001001/005001001003/MoreInfo.aspx?CategoryNum=005001001003 PN',  # 装饰装修 36
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001001/005001001004/MoreInfo.aspx?CategoryNum=005001001004 PN',  # 园林绿化 56
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001001/005001001005/MoreInfo.aspx?CategoryNum=005001001005 PN',  # 设备采购 106
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001001/005001001006/MoreInfo.aspx?CategoryNum=005001001006 PN',  # 其他 614
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001003/MoreInfo.aspx?CategoryNum=005001003 PN',  # 工程建设-最高限价 332
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001004/005001004001/MoreInfo.aspx?CategoryNum=005001004001 RN',  # 工程建设-评标结果-房屋建筑 552
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001004/005001004002/MoreInfo.aspx?CategoryNum=005001004002 RN',  # 市政基础 273
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001004/005001004003/MoreInfo.aspx?CategoryNum=005001004003 RN',  # 装饰装修 54
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001004/005001004004/MoreInfo.aspx?CategoryNum=005001004004 RN',  # 园林绿化 84
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001004/005001004005/MoreInfo.aspx?CategoryNum=005001004005 RN',  # 工程监理 116
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001004/005001004006/MoreInfo.aspx?CategoryNum=005001004006 RN',  # 设备采购 103
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001004/005001004007/MoreInfo.aspx?CategoryNum=005001004007 RN',  # 其他 869
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001005/MoreInfo.aspx?CategoryNum=005001005 RN',  # 工程建设-中标人公告 245
        'http://www.czztb.gov.cn/czztb/jyxx/005001/005001006/MoreInfo.aspx?CategoryNum=005001006 RN',  # 工程-未入围 6
        'http://www.czztb.gov.cn/czztb/jyxx/005002/005002001/MoreInfo.aspx?CategoryNum=005002001 PN',  # 政府采购-采购公告 1404
        'http://www.czztb.gov.cn/czztb/jyxx/005002/005002002/MoreInfo.aspx?CategoryNum=005002002 PN',  # 更正-补充公告 146
        'http://www.czztb.gov.cn/czztb/jyxx/005002/005002003/MoreInfo.aspx?CategoryNum=005002003 RN',  # 评审结果公告 602
        'http://www.czztb.gov.cn/czztb/jyxx/005002/005002004/MoreInfo.aspx?CategoryNum=005002004 RN',  # 中标成交公示 870
        'http://www.czztb.gov.cn/czztb/jyxx/005003/005003001/MoreInfo.aspx?CategoryNum=005003001 PN',  # 产权交易-信息发布 228
        'http://www.czztb.gov.cn/czztb/jyxx/005003/005003002/MoreInfo.aspx?CategoryNum=005003002 CN',  # 更正信息 0
        'http://www.czztb.gov.cn/czztb/jyxx/005003/005003003/MoreInfo.aspx?CategoryNum=005003003 RN',  # 结果公示 211
        'http://www.czztb.gov.cn/czztb/jyxx/005004/MoreInfo.aspx?CategoryNum=005004 CN',  # 其他项目 17
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.25,
                       "DOWNLOAD_TIMEOUT":15,}

    def __init__(self,start_url=None,history=True):
        super(Haqggzygov, self).__init__()
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
        data_list = response.xpath('//table[@id="MoreInfoList1_moreinfo"]//tr[3]/td/table//tr/td/a')
        print 'len(data): {}, {}'.format(len(data_list), response.url)
        for each in data_list:
            url = each.xpath('./@href').extract()[0]
            title = each.xpath('./@title').extract()[0]
            pubtime = each.xpath('./../following-sibling::td[1]/text()').extract()[0]
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime.strip())
            url = urljoin(response.url, url)
            if pubtime:
                pubtime = pubtime.group()
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,'pubtime':pubtime},
                          callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = response.xpath('//a[contains(@href, "javascript")][last()]/@title').extract()
            view_value = response.xpath('//input[contains(@id,"VIEWSTATE")]/@value').extract()
            if len(page_rule) > 0 and len(view_value) > 0:
                total_page = re.search(ur'\d+', page_rule[0]).group()
                view_value = view_value[0]
                if int(total_page) > 1:
                    for i in range(2, int(total_page)+1):
                        post_params = {'__VIEWSTATE': view_value, '__EVENTTARGET': 'MoreInfoList1$Pager',
                                       '__EVENTARGUMENT': str(i)}
                        final = response.url
                        yield FormRequest(url=final,formdata=post_params,meta={'ba_type':response.meta['ba_type'],'page_parse':False},
                                      callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        title = response.xpath('//td[@id="tdTitle"]/font/b/text()').extract()
        item['pubtime'] = response.meta['pubtime'].strip() + ' 00:00'
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title'].strip()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省淮安市淮安区'
        item['source'] = u'淮安区招投标网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//table[@id="tblInfo"]').extract()
        item['content'] = content[0]
        item['pubtime'] = datetime.datetime.strptime(item['pubtime'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item['pubtime'], item['title'], response.url
            raise Exception('{},{},{}'.format(response.url, item['pubtime'], item['title']))

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass


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


class jslygggzy(scrapy.Spider):
    name = "jslygggzy"
    start_urls = [
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001001/001001001/tradeInfo.html PN',  # 建设工程-招标公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001001/001001002/tradeInfo.html RN',  # 未入围
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001001/001001003/tradeInfo.html PN',  # 最高限价
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001001/001001004/tradeInfo.html RN',  # 评标结果
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001001/001001005/tradeInfo.html RN',  # 中标结果
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001003/001003001/tradeInfo.html PN',  # 水利工程-招标公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001003/001003003/tradeInfo.html RN',  # 评标结果
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001003/001003002/tradeInfo.html RN',  # 中标结果
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001002/001002001/tradeInfo.html PN',  # 交通工程-招标公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001002/001002003/tradeInfo.html RN',  # 评标结果
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001002/001002002/tradeInfo.html RN',  # 中标结果
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001004/001004001/tradeInfo.html PN',  # 政府采购-采购公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001004/001004003/tradeInfo.html PF',  # 采购预告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001004/001004006/tradeInfo.html CN',  # 更正公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001004/001004002/tradeInfo.html RN',  # 成交公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001004/001004004/tradeInfo.html RN',  # 废标公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001004/001004005/tradeInfo.html RN',  # 合同公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001008/001008001/tradeInfo.html PN',  # 医药采购-采购公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001008/001008002/tradeInfo.html RN',  # 中标结果
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001006/001006001/tradeInfo.html PN',  # 国有产权-出让公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001006/001006003/tradeInfo.html RN',  # 成交公示
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001007/001007001/tradeInfo.html PN',  # 其它行业-招标公告
        'http://spzx.lyg.gov.cn/lygweb/jyxx/001007/001007002/tradeInfo.html RN',  # 中标
    ]
    Debug = True
    doredis = True
    source = u"连云港市公共资源交易网"
    # configure = SpecialConfig()
    post_params = []
    real_counts = 0

    def __init__(self, start_url=None,history=True):
        super(jslygggzy, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
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
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True},callback=self.parse_link)

    def parse_link(self, response):
        data_list = response.xpath('//table[@class="ewb-trade-tb"]/tbody/tr')
        if len(data_list) == 0:
            raise Exception('没有抓取到目标数据节点！')
        for data in data_list:
            url = data.xpath('./td[2]/a/@href').extract()[0]
            title = data.xpath('./td[2]/a/@title').extract()[0]
            pubtime = data.xpath('./td[4]/text()').extract()[0]

            url = urlparse.urljoin(response.url, url)
            pubtime = pubtime + ' 00:00'
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'title':title,'pubtime':pubtime},callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = response.xpath(u'//li/a[contains(text(), "末页")]/@href').extract()
            print 'page_rule', page_rule
            if len(page_rule) > 0:
                total_page = re.search(r'(\d+).html', page_rule[0].rpartition('/')[-1]).group(1)
                for i in range(2, int(total_page)+1):
                    final = response.url.replace('tradeInfo.html', '{}.html'.format(i))
                    yield Request(url=final,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.meta["title"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省连云港市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//div[@class="article-info"]').extract() or \
                 response.xpath("//*[@class='infodetail']").extract() or \
                 response.xpath("//span[@id='spnContent']").extract() or \
                 response.xpath("//table[@id='moreinfo']").extract()
        item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item


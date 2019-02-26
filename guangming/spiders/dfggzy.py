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


class Dfggzy(scrapy.Spider):
    name = "dfggzy"  # 大丰公共资源电子交易平台
    start_urls = [
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005006/005006001/MoreInfo.aspx?CategoryNum=005006001 PN',  # 其他-招标公告 10
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005005/005005003/MoreInfo.aspx?CategoryNum=005005003 RN',  # 土地交易-成交公告 7
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005005/005005001/MoreInfo.aspx?CategoryNum=005005001 RN',  # 土地-交易公告 16
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005004/005004003/MoreInfo.aspx?CategoryNum=005004003 RN',  # 产权-结果公告 12
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005004/005004002/MoreInfo.aspx?CategoryNum=005004002 PN',  # 产权-资审公告 1
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005004/005004001/MoreInfo.aspx?CategoryNum=005004001 PN',  # 产权-交易信息 30
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005003/005003006/MoreInfo.aspx?CategoryNum=005003006 CN',  # 药品-答疑补充 13
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005003/005003005/MoreInfo.aspx?CategoryNum=005003005 PN',  # 药品-最高限价 1
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005003/005003004/MoreInfo.aspx?CategoryNum=005003004 PN',  # 药品-招标文件 58
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005003/005003003/MoreInfo.aspx?CategoryNum=005003003 RN',  # 药品-结果公告 43
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005003/005003002/MoreInfo.aspx?CategoryNum=005003002 PN',  # 药品-资审公示 1
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005003/005003001/MoreInfo.aspx?CategoryNum=005003001 PN',  # 药品-采购公告 104
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005002/005002006/MoreInfo.aspx?CategoryNum=005002006 CN',  # 政府采购-答疑补充 923
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005002/005002004/MoreInfo.aspx?CategoryNum=005002004 PN',  # 政府采购-最高限价 42
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005002/005002003/MoreInfo.aspx?CategoryNum=005002003 PN',  # 政府采购-资审公示 5
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005002/005002002/MoreInfo.aspx?CategoryNum=005002002 PN',  # 政府采购-招标文件 1878
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005001/005001007/MoreInfo.aspx?CategoryNum=005001007 RN',  # 工程建设-中标候选人 3089
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005001/005001006/MoreInfo.aspx?CategoryNum=005001006 CN',  # 工程建设-答疑补充 1858
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005001/005001004/MoreInfo.aspx?CategoryNum=005001004 PN',  # 工程建设-招标控制价 2650
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005001/005001003/MoreInfo.aspx?CategoryNum=005001003 PN',  # 工程建设-资格预审 73
        'http://ggzy.dafeng.gov.cn/dfweb/jyxx/005001/005001002/MoreInfo.aspx?CategoryNum=005001002 PN',  # 工程建设-招标文件 2109

        'http://ggzy.dafeng.gov.cn/dfweb/commonpages/jggssearch.aspx RN',  # 政府采购-结果公告 2345
        'http://ggzy.dafeng.gov.cn/dfweb/commonpages/cgggsearch.aspx PN',  # 政府采购-采购公告 3422
        'http://ggzy.dafeng.gov.cn/dfweb/commonpages/zbgssearch.aspx RN',  # 工程建设-中标公示 4492
        'http://ggzy.dafeng.gov.cn/dfweb/commonpages/zbggsearch.aspx PN',  # 工程建设-招标公告 5360
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,}

    def __init__(self, start_url=None,history=True):
        super(Dfggzy, self).__init__()
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
        if 'search.aspx' in response.url:
            data_list = response.xpath('//body//table[2]//tr')
        else:
            data_list = response.xpath("//table[@id='MoreInfoList1_DataGrid1']//tr")
        current_page = response.xpath('//div[@id="MoreInfoList1_Pager"]/table//tr/td[1]/font[3]//text()').extract() or \
                       response.xpath('//div[contains(@id, "List1_Pager")]/table//tr/td/font[3]//text()').extract()
        current_page = current_page[0]
        print 'len(): {} , {} cur_page:{}'.format(len(data_list), response.url, current_page)
        for each in data_list:
            url = ''.join(each.xpath('.//td[2]/a/@href').extract())
            title = each.xpath('.//td[2]/a/@title').extract() or \
                    each.xpath('.//td[2]/a/text()').extract()
            title = ''.join(title)
            pubtime = each.xpath('.//td[3]//text()').re('\d+-\d+-\d+')[0]
            url = urljoin(response.url,url)
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            pubtime = pubtime.strip() + " 00:00"
            # print url,pubtime,title
            yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],"title":title,"pubtime":pubtime},callback=self.parse_item)
        if self.history and response.meta["page_parse"]:
            page = response.xpath('//div[@id="MoreInfoList1_Pager"]/table//tr/td[1]/font[2]//text()').extract()
            if 'search.aspx' in response.url:
                   page = response.xpath('//div[contains(@id, "List1_Pager")]/table//tr/td/font[2]//text()').extract()
            print page
            if len(page) > 0:
                page = page[0].strip()
                print 'page={}'.format(page)
                for i in range(2, int(page)+1):
                    data={
                        '__VIEWSTATE':response.xpath("//input[@id='__VIEWSTATE']/@value").extract()[0],
                        ' __VIEWSTATEGENERATOR':response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract()[0],
                        '__EVENTTARGET':'MoreInfoList1$Pager',
                        '__EVENTARGUMENT':str(i),
                        '__VIEWSTATEENCRYPTED':''}
                    if 'search.aspx' in response.url:
                        data['__EVENTVALIDATION'] = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract()[0]
                        data_params1 = re.search(r'/(\S{4,6})search.aspx', response.url).group(1)
                        data_params2 = '{}List1$'.format(data_params1.upper())
                        data['__EVENTTARGET'] = data_params2 + 'Pager'
                        another_params = response.xpath('//*[contains(@id, "List1_")][not(contains(@id, "Button"))]/@name').extract()
                        for param in another_params:
                            data['{}'.format(param)] = ''
                    yield FormRequest(url=response.url,formdata=data,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省盐城市大丰区'
        item['source'] = u'大丰公共资源交易网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        title = response.xpath('//td[@id="tdTitle"]/font/b/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta['title']
        item['content'] = ''.join(response.xpath('//table[@id="tblInfo"]').extract())
        if item['pubtime'] and item['title'] and item['content']:
            yield item

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import time
import sys
import scrapy
import json
import datetime
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


class Jsjsgczbw(scrapy.Spider):
    name = "jsjsgczbw"  # 江苏省建设工程招标网
    start_urls = [
        'http://www.jszb.com.cn/JSZB/YW_info/ZhaoBiaoGG/MoreInfo_ZBGG.aspx?categoryNum=012 PN',  # 招标公告
        'http://www.jszb.com.cn/JSZB/YW_info/ZuiGaoXJ/MoreInfo_ZGXJ.aspx?categoryNum=012 PN',  # 最高限价公告
        'http://www.jszb.com.cn/JSZB/YW_info/ZiGeYS/MoreInfo_ZGYS.aspx?categoryNum=012 RN',  # 未入围公示
        'http://www.jszb.com.cn/JSZB/YW_info/HouXuanRenGS/MoreInfo_HxrGS.aspx?categoryNum=012 RN',  # 评标结果公示
        'http://www.jszb.com.cn/JSZB/YW_info/ZhongBiaoGS/MoreInfo_ZBGS.aspx?categoryNum=012 RN',  # 中标结果公告
    ]
    Debug = True
    doredis = True
    source = u"江苏省建设工程招标网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.15,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}
    final = []

    def __init__(self,start_url=None,history=True):
        super(Jsjsgczbw, self).__init__()
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
        data_list = response.xpath('//table[contains(@id, "MoreInfoList")]//tr/td/a[contains(@onclick, "window.open")]')
        print 'len: ', len(data_list), response.url
        if len(data_list) > 0:
            for data in data_list:
                url = data.xpath('./@onclick').extract()[0]
                title = data.xpath('./@title').extract()[0]
                pubtime = data.xpath('./../following-sibling::td[2]/text()').extract()[0]
                url = re.search(r'window.open\("(.+?)",', url).group(1).strip()
                url = urlparse.urljoin(response.url, url)
                pubtime = pubtime.strip() + ' 00:00'
                self.final.append(url)
                # print url, pubtime,' list:',len(self.final), ' set:', len(set(self.final))
                yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'title':title,'pubtime':pubtime},callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            headers = {
                "Host": "www.jszb.com.cn",
                "Origin": "http://www.jszb.com.cn",
                "Upgrade-Insecure-Requests": "1",
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": response.url,
            }
            page_rule = response.xpath('//div[contains(@id, "Pager")]//a[last()]/@title').extract()
            post_params = response.xpath('//input[@type="hidden"]')
            another_params = response.xpath('//*[contains(@name, "MoreInfoList")]')
            formdata = {}
            for param in post_params:
                name = param.xpath('./@name').extract()[0].encode('utf-8')
                value = param.xpath('./@value').extract()[0].encode('utf-8')
                formdata[name] = value
            for param in another_params:
                name = param.xpath('./@name').extract()[0].encode('utf-8')
                if 'jpd' in name:
                    formdata[name] = '-1'
                elif 'btnOK' in name:
                    pass
                else:
                    formdata[name] = ''
            if 'MoreInfo_HxrGS.aspx?' in response.url:
                formdata['__EVENTTARGET'] = 'MoreInfoList_HXRGS1$Pager'
            else:
                formdata['__EVENTTARGET'] = 'MoreInfoList1$Pager'
            if len(page_rule) > 0:
                total_page = re.search(r'\d+', page_rule[0]).group()
                # print total_page
                for i in range(2, int(total_page)+1):
                    formdata['__EVENTARGUMENT'] = str(i)
                    # print formdata.keys()
                    yield FormRequest(url=response.url,headers=headers,formdata=formdata,dont_filter=True,meta={"ba_type":response.meta["ba_type"],"page_parse":False},callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        notitle_list = [u'江苏省工程建设项目评标结果公示', u'评标结果公示']
        item["pubtime"] = response.meta["pubtime"]
        item['pubtime'] = datetime.datetime.strptime(item['pubtime'], "%Y-%m-%d %H:%M").strftime("%Y-%m-%d %H:%M")
        title = response.xpath('//*[@id="Table1"]//tr[1]/td/font/b/text()').extract() or \
                response.xpath('//*[@id="Form1"]/font/table//tr/td//tr[1]/td/p/font[1]/strong/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = response.meta["title"]
        for notitle in notitle_list:
            if notitle in item['title']:
                item['title'] = response.meta["title"]
        if '...' in item['title']:
            title_1 = response.xpath('//span[@id="lblBDName"]/text()').extract() or \
                      response.xpath('//span[@id="lblProjectName"]/text()').extract()
            if len(title_1) > 0:
                item['title'] = title_1[0].strip()
            else:
                if '（' in item['title']:
                    item['title'] = item['title'].rpartition('（')[0]
                title_str = re.search(ur'(\S{3})\.\.\.', item['title'])
                if title_str:
                    title_str = title_str.group(1)
                    title_2 = response.xpath(u'//*[contains(text(), "{}")][not(contains(text(), "公司"))]/text()'.format(title_str)).extract() or \
                              response.xpath(u'//b[contains(text(), "{}")]/text()'.format(title_str)).extract()
                    print '特殊处理 title', item['title'], title_str, title_2
                    if len(title_2) > 0:
                        item['title'] = title_2[0].strip()
                    else:
                        if re.search(r'\[.*?]', item['title']):
                            title_str = re.search(r'\[.*?](.+)', item['title']).group(1)
                        else:
                            title_str = item['title']
                        title_3 = response.xpath(u'//*[contains(text(), "{}")][not(contains(text(), "公司"))]/text()'.format(title_str[0:4])).extract()
                        print '特殊处理 title', item['title'], title_str, title_3
                        if len(title_3) > 0:
                            item['title'] = title_3[0].strip()
            print item['title']

        # print 'title: ', len(title), item['title']
        if '...' in item['title']:
            print '--'*100
            print '--'*100
            print item['title'], response.url
            print '--'*100
            print '--'*100
            raise Exception('title有问题')
        # print response.url
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        content = response.xpath('//form[@id="Form1"]/font/table').extract() or \
                  response.xpath('//form[@name="form1"]/div/table').extract()
        item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])


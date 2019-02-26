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
import datetime
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


class jsszzfcgw(scrapy.Spider):
    name = "jsszzfcgw"
    start_urls = [
        'http://www.zfcg.suzhou.gov.cn/content/searchContents.action PN',  # 采购公告type=0 补充公告type=1 中标公告type=2
    ]
    Debug = True
    doredis = True
    source = u"苏州政府采购网"
    # configure = SpecialConfig()
    custom_settings = {'DOWNLOAD_DELAY': 0.2, 'DOWNLOAD_TIMEOUT': 20, 'ROBOTSTXT_OBEY': False}
    post_params = []
    final_list = []

    def __init__(self,start_url=None,history=True):
        super(jsszzfcgw, self).__init__()
        self.histroy = history
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_read_redis.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

    def start_requests(self):
        for channel in self.post_params:
            url = channel['url']
            type_list = [0, 1, 2]
            for type in type_list:
                formdata = {'type': str(type), 'title': '', 'choose': '', 'zbCode': '',
                            'appcode': '', 'page': '1', 'rows': '30'}
                if type == 0:
                    channel["ba_type"] = 'PN'
                elif type == 1:
                    channel["ba_type"] = 'CN'
                elif type == 2:
                    channel["ba_type"] = 'RN'
                yield FormRequest(url=url,formdata=formdata,dont_filter=True,meta={"ba_type": channel["ba_type"], "page_parse": True, "formdata": formdata},method='post',callback=self.parse_link)

    def parse_link(self, response):
        rows = json.loads(response.body)["rows"]
        for row in rows:
            ba_type = response.meta["ba_type"]
            url_id = row['PROJECTID']
            pubtime = row["RELEASE_TIME"]
            newUrl = "../html/project/{}.shtml".format(str(url_id))
            final = urlparse.urljoin(response.url,newUrl)
            title = row['TITLE']
            self.final_list.append(final)
            # print final, pubtime,title
            if u'成交' in title or u'单一来源' in title or u'结果' in title:
                ba_type = 'RN'
            elif u'招标' in title:
                ba_type = 'PN'
            elif u'变更' in title or u'补充' in title or u'更正' in title:
                ba_type = 'CN'
            yield Request(url=final,method='get',meta={"ba_type":ba_type,"pubtime":pubtime,"title":title},callback=self.parse_item)

        if self.histroy and response.meta['page_parse']:
            total_count = json.loads(response.body)['total']
            print total_count
            if int(total_count) % int(response.meta['formdata']['rows']) == 0:
                total_page = int(total_count) // int(response.meta['formdata']['rows'])
            else:
                total_page = int(total_count) // int(response.meta['formdata']['rows']) + 1
            print total_page
            for i in range(2, total_page+1):
                response.meta['formdata']['page'] = str(i)
                formdata = response.meta['formdata']
                yield FormRequest(url=response.url, method='post', formdata=formdata, dont_filter=True, meta={"ba_type": response.meta["ba_type"], "page_parse": False}, callback=self.parse_link)

    def parse_item(self, response):
            item = DataItem()
            print "response_status:  ",response.status,'list_len: ', len(self.final_list),'set: ', len(set(self.final_list))
            if response.status != 200:
                print '状态码错误!'
            if response.meta["ba_type"] == "PN":
                infoId = "tab1"
                infoType = "PN"
            elif response.meta["ba_type"] == "CN":
                infoId = "tab2"
                infoType = "CN"
            else:
                infoId = 'tab6'
                infoType = 'RN'
                if len(response.xpath("//ul[@id='menu']/li[3]/a/text()").extract()) > 0:
                    if u'有' in response.xpath("//ul[@id='menu']/li[3]/a/text()").extract()[0]:
                        infoId = "tab3"
            title = "//div[@id='{}']//div[@class='M_title']/text()"
            pubtime = "//div[@id='{}']//div[@class='date']/span/text()"
            content = "//div[@id='{}']//div[@class='Article']"

            item["pubtime"]=response.xpath(pubtime.format(infoId)).extract()
            if len(item["pubtime"]) > 0:
               item["pubtime"] = item["pubtime"][0].strip() + " 00:00"
            else:
               item["pubtime"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})",response.meta["pubtime"]).group(0)
            item["type"] = infoType
            item['url'] = response.url + "#"+item["type"]
            item['area'] = u'江苏省苏州市'
            item['source'] = self.source
            item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
            item['title'] = response.xpath(title.format(infoId)).extract()
            item['content'] = response.xpath(content.format(infoId)).extract()
            if len(item['title']) > 0:
                item['title'] = item['title'][0].strip()
                item['content'] = item['content'][0]
            else:
                item['title'] = response.meta['title']
                titles_list = response.xpath('//div[@class="M_title"]')
                print 'title_list: ', titles_list
                for titles in titles_list:
                    title = titles.xpath('./text()').extract()[0].strip()
                    print title
                    if title in item['title']:
                        item['content'] = titles.xpath('./../div[@class="Article"]').extract()[0]

            # if self.doredis and self.expire_redis.exists(item['url']):
            #     flag = False
            # else:
            #     flag = True
            if item['pubtime'] and item['title'] and item['content']:
                yield item
            else:
                print response.url, '\n字段缺失!!! {}, {},{}'.format(item['title'],item['content'], infoType)

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
from scrapy import Selector
from scrapy import signals
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.utils.response import get_base_url
# from SpeciSpiders.items import DataItem
# from bc_crawler.configs.special_config import SpecialConfig
# from scrapy.xlib.pydispatch import dispatcher
from ..items import JobItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Job51(scrapy.Spider):
    name = "job51"  # 北京时间
    start_urls = [
        # 'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E6%258C%2596%25E6%258E%2598,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare= jobs',
        'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%25BC%2580%25E5%258F%2591,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare= jobs',
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.5,
                       "DOWNLOAD_TIMEOUT": 10}

    def __init__(self,start_url=None,history=True):
        super(Job51, self).__init__()
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
            yield Request(url=url,method='get',meta={'ba_type':channel['ba_type'],"parse_page":True},callback=self.parse_link)

    def parse_link(self, response):
        url_list = response.xpath('//div[@class="el"]//p/span/a')
        page_rule = response.xpath('//div[@class="dw_page"]//li[@class="bk"][last()]/a/@href').extract()
        print 'url_list',len(url_list), response.url
        for info in url_list:
            try:
                url = info.xpath('./@href').extract()[0]
                job_name = info.xpath('./@title').extract()[0]
                location = info.xpath('./ancestor::div[1]/span[@class="t3"]/text()').extract()[0]
                salary = info.xpath('./ancestor::div[1]/span[@class="t4"]/text()').extract()[0]
                pubtime = info.xpath('./ancestor::div[1]/span[@class="t5"]/text()').extract()[0]
                url = urlparse.urljoin(response.url, url)
            except Exception, e:
                print e.message
                pass
            # if self.doredis and self.expire_redis.exists(final):
            #    continue
            else:
                print job_name, location, salary, pubtime
            # yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime,'medianame':medianame},callback=self.parse_item)
        if self.history and response.meta['parse_page'] and len(page_rule) > 0:
            next_url = page_rule[0]
            yield Request(url=next_url,method='get',meta={'ba_type':response.meta['ba_type'],"parse_page":True},callback=self.parse_link)


    def parse_item(self, response):
        item = JobItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'中国'
        item['source'] = u"51job"
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url

        medianame = response.xpath('//span[@class="col cite"]/text()').extract() or \
                    response.xpath('//span[@class="cite"]/text()').extract()
        if len(medianame) > 0:
            medianame = medianame[0].strip().replace(' ', '')
            if medianame:
                item['medianame'] = medianame
            else:
                item['medianame'] = u'北京时间'
        elif response.meta.get('medianame'):
            item['medianame'] = response.meta['medianame']
        else:
            item['medianame'] = u'北京时间'

        pubtime = response.xpath('//span[@class="col time"]/text()').extract() or \
                  response.xpath('//span[@class="time"]/text()').extract()
        if len(pubtime) == 0:
            pubtime = response.meta['pubtime']
        final_pubtime1 = re.search(r'20\d{2}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
        final_pubtime2 = re.search(r'20\d{2}-\d{1,2}-\d{1,2}\d{1,2}:\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
        final_pubtime3 = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
        if final_pubtime1:
            item['pubtime'] = datetime.datetime.strptime(final_pubtime1.group(), "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
        elif final_pubtime2:
            item['pubtime'] = datetime.datetime.strptime(final_pubtime2.group(), "%Y-%m-%d%H:%M").strftime('%Y-%m-%d %H:%M')
        elif final_pubtime3:
            item['pubtime'] = datetime.datetime.strptime(final_pubtime3.group(), "%Y-%m-%d").strftime('%Y-%m-%d %H:%M')
        else:
            item['pubtime'] = response.meta['pubtime']

        title = response.xpath('//h1[@id="title"]/text()').extract()
        title1 = response.xpath('//div[@class="headline"]/h1//text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        elif len(title1) > 0:
            item['title'] = ''.join(title1)

        content = response.xpath('//div[@class="article"]').extract() or \
                  response.xpath('//div[@class="gallery-list"]').extract() or \
                  response.xpath('//div[@class="video-content-txt"]').extract() or \
                  response.xpath('//div[@id="main"]').extract()
        item['content'] = content[0]
        pagination_rule = response.xpath(u'//*[@id="article-pagination"]/div/a[contains(text(), "下一页")]/@href').extract()
        if len(pagination_rule) > 0:
            page_url = pagination_rule[0]
            if 'page=-1' not in page_url:
                yield Request(url=page_url,method='get',meta={'item':item,'parse_content':True},callback=self.parse_item)

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



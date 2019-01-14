#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import re
import time
import base64
import scrapy
import json
import requests
import redis
import urllib
from scrapy.http import Request
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


def timeStamp(pubtime):
    timeStamp = float(pubtime/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

 
class CzjyjsSpider(scrapy.Spider):
    name = "czjyjs"
    start_urls = [
        'http://zbz.czedu.com.cn/WZ/getNewList.do PN 202 JTIwQ19pbnRfbmV3bG1pZCUyMD01NiUyMGFuZCUyMENfaW50X25ld3R5cGVpZD02MiUyMGFuZCUyMENfRFRfSW5zZXJ0VGltZSUzRT0nMjAxNS0wNC0wMyc=',
        'http://zbz.czedu.com.cn/WZ/getNewList.do PN 66 JTIwQ19pbnRfbmV3bG1pZCUyMD01NiUyMGFuZCUyMENfaW50X25ld3R5cGVpZD02NCUyMGFuZCUyMENfRFRfSW5zZXJ0VGltZSUzRT0nMjAxNS0wNC0wMyc=',
        'http://zbz.czedu.com.cn/WZ/getNewList.do PN 44 JTIwQ19pbnRfbmV3bG1pZCUyMD01NiUyMGFuZCUyMENfaW50X25ld3R5cGVpZD02NiUyMGFuZCUyMENfRFRfSW5zZXJ0VGltZSUzRT0nMjAxNS0wNC0wMyc=',
        'http://zbz.czedu.com.cn/WZ/getNewList.do PN 317 JTIwQ19pbnRfbmV3bG1pZCUyMD01NiUyMGFuZCUyMENfaW50X25ld3R5cGVpZD02OCUyMGFuZCUyMENfRFRfSW5zZXJ0VGltZSUzRT0nMjAxNS0wNC0wMyc=',
        'http://zbz.czedu.com.cn/WZ/getNewList.do PN 0 JTIwQ19pbnRfbmV3bG1pZCUyMD01NiUyMGFuZCUyMENfaW50X25ld3R5cGVpZD03NiUyMGFuZCUyMENfRFRfSW5zZXJ0VGltZSUzRT0nMjAxNS0wNC0wMyc=',
        'http://zbz.czedu.com.cn/WZ/getNewList.do CN 133 JTIwQ19pbnRfbmV3bG1pZCUyMD01NiUyMGFuZCUyMENfaW50X25ld3R5cGVpZD03MyUyMGFuZCUyMENfRFRfSW5zZXJ0VGltZSUzRT0nMjAxNS0wNC0wMyc=',
        'http://zbz.czedu.com.cn/WZ/getNewList.do RN 653 JTIwQ19pbnRfbmV3bG1pZCUyMD01NiUyMGFuZCUyMENfaW50X25ld3R5cGVpZD03MCUyMGFuZCUyMENfRFRfSW5zZXJ0VGltZSUzRT0nMjAxNS0wNC0wMyc=',
        'http://zbz.czedu.com.cn/WZ/getNewList.do PN 24 JTIwQ19pbnRfbmV3bG1pZCUyMD01NiUyMGFuZCUyMENfaW50X25ld3R5cGVpZD03OCUyMGFuZCUyMENfRFRfSW5zZXJ0VGltZSUzRT0nMjAxNS0wNC0wMyc=',
        # 理论1446 实际1446
    ]
    Debug = True
    doredis = True
    source = u"常州市教育基本建设与装备管理中心"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"DOWNLOAD_TIMEOUT":30}
    headers={"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8", 
             "Accept":"application/json, text/javascript, */*; q=0.01",
             "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}

    def __init__(self, start_url = None):
        super(CzjyjsSpider, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        for job in jobs:
            param = {}
            url = job.split()[0]
            ba_type = job.split()[1]
            count = job.split()[2]
            simple = job.split()[3]
            param["url"] = url
            param["ba_type"] = ba_type
            param['count'] = count
            param['simple'] = simple
            self.post_params.append(param)
        # dispatcher.connect(self.initial, signals.engine_started)

    def start_requests(self):
        for channel in self.post_params:
            count = channel['count']
            simple = channel['simple']
            ba_type = channel['ba_type']
            if count == 0:
                formdata = {"pageNumber": "1", "pageSize": "10", 'simple': simple}
                yield FormRequest(url="http://zbz.czedu.com.cn/WZ/getNewList.do", headers=self.headers,
                                  meta={"ba_type":ba_type,'count':count,'simple':simple,'page_parse': False},
                                  formdata=formdata,callback=self.parse_link)
            else:
                formdata = {"pageNumber": "1", "pageSize": "10", 'count': count, 'simple': simple}
                yield FormRequest(url="http://zbz.czedu.com.cn/WZ/getNewList.do", headers=self.headers,
                                  meta={"ba_type":ba_type,'count':count,'simple':simple,'formdata':formdata, 'page_parse': True},
                                  formdata=formdata,callback=self.parse_link)

    def parse_link(self, response):
        json_data = json.loads(response.body)
        count = response.meta['count']
        simple = response.meta['simple']
        for id in json_data['rows']:
            Ida = id["C_int_newlmid"]
            Idb = id["C_int_newtypeid"]
            Idc = id["P_int_newid"]
            title = id["C_nvc200_newtitle"]
            pubtime = id["C_dt_inserttime"]
            content = id["C_nvcmax_newcontent"]
            pubtime = re.search('(\d+)',pubtime).group()
            pubtime = timeStamp(int(pubtime))
            pubtime = re.search('\d+-\d+-\d+ \d+:\d+',pubtime).group()
            real_url = 'http://zbz.czedu.com.cn/CGPT/WZ/cggg/infoDetail.html?id={}&ntp={}&lmid={}'.format(Idc,Idb,Ida)
            print real_url
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0", "Content-Type": "application/json"}
            # if self.doredis and self.expire_redis.exists(real_url):
            #     continue
            yield Request(url=real_url, dont_filter=True, meta={"pubtime":pubtime, "title":title, "content":content, "ba_type":response.meta["ba_type"]}, headers=headers, callback=self.parse_item)
        if response.meta['page_parse']:
            count = response.meta['count']
            formdata = response.meta['formdata']
            if int(count) % 10 == 0:
                total_page = int(count) // 10
            else:
                total_page = int(count) // 10 + 1
            for i in range(2, total_page+1):
                formdata['pageNumber'] = str(i)
                yield FormRequest(url="http://zbz.czedu.com.cn/WZ/getNewList.do", headers=self.headers,
                                  meta={"ba_type":response.meta['ba_type'],'count':count,'simple':simple,'formdata':formdata, 'page_parse': False},
                                  formdata=formdata,callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        item['type'] = response.meta["ba_type"]
        item['area'] = u'江苏省常州市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        item['title'] = response.meta["title"]
        item['pubtime'] = response.meta["pubtime"]
        item['url'] = response.url
        print item['title']
        print item['pubtime']
        item['content'] = urllib.unquote(base64.b64decode(response.meta["content"])).decode("utf-8")
        item['type'] = response.meta['ba_type']
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print item

    def initial(self):
        # 利用redis去重
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass


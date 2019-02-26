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


class jsszggzy(scrapy.Spider):
    name = "jsszggzy"
    start_urls = [
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/jyzxmore.aspxCategoryNum=002001001 PN',  # 建设工程-招标公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/zgscmore.aspx?CategoryNum=002001002 PN',  # 资格预审公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/zgxjmore.aspx?CategoryNum=002001003 PN',  # 招标控制价
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/zgxjmore.aspx?CategoryNum=002001004 RN',  # 评标结果
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/zgxjmore.aspx?CategoryNum=002001005 RN',  # 中标候选人
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/zbgsmore.aspx?CategoryNum=002001006 RN',  # 中标公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002001/002001007/ CN',  # 变更公告

        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/gcjs_more.aspx?CategoryNum=002002002 PN',  # 交通公告-招标公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/gcjs_more.aspx?CategoryNum=002002003 RN',  # 评标结果公示
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/gcjs_more.aspx?CategoryNum=002002004 RN',  # 中标公告

        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/gcjs_more.aspx?CategoryNum=002003001 PN',  # 水利工程-招标公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/gcjs_more.aspx?CategoryNum=002003003 PN',  # 最高限价
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/gcjs_more.aspx?CategoryNum=002003006 RN',  # 中标候选人
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/ShowInfo/gcjs_more.aspx?CategoryNum=002003005 RN',  # 中标公告

        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002004/002004001/ PN',  # 政府采购-招标公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002004/002004002/ RN',  # 中标公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002004/002004003/ CN',  # 补充公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002004/002004004/ RN',  # 供货协议（中标结果）
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002004/002004005/ PN',  # 采购方式确定公示
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002004/002004006/ PN',  # 进口产品采购公示

        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002005/002005001/ PN',  # 国土交易-挂牌公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002005/002005004/ PN',  # 出让公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002005/002005005/ RN',  # 成交公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002005/002005006/ PN',  # 工业用地（杂乱的）要判断

        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002006/002006001/ PN',  # 产权交易-交易公告
        'http://szzyjy.fwzx.suzhou.gov.cn/Front/jyzx/002006/002006002/ RN',  # 成交公告

        ## 旧的
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003001001&bianhao=&xmmc= PN", #建设
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003001007&bianhao=&xmmc= RN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003001008&bianhao=&xmmc= RN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003001005&bianhao=&xmmc= PN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003001006&bianhao=&xmmc= RN",

        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003002001&bianhao=&xmmc= PN",#交通工程
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003002002&bianhao=&xmmc= CN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003002003&bianhao=&xmmc= RN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003002004&bianhao=&xmmc= RN",

        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003003001&bianhao=&xmmc= PN",#水利工程
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003003002&bianhao=&xmmc= CN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003003003&bianhao=&xmmc= RN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003003004&bianhao=&xmmc= RN",

        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003004002&bianhao=&xmmc= PN",#政府采购
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003004003&bianhao=&xmmc= CN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003004004&bianhao=&xmmc= CN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003004005&bianhao=&xmmc= RN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003004006&bianhao=&xmmc= RN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003004007&bianhao=&xmmc= RN",

        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003005002&bianhao=&xmmc= PN", #土地矿产
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003005003&bianhao=&xmmc= PN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003005004&bianhao=&xmmc= RN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003005005&bianhao=&xmmc= RN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003005006&bianhao=&xmmc= PN",

        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003006001&bianhao=&xmmc= PN",#国土产权
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003006003&bianhao=&xmmc= CN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003006004&bianhao=&xmmc= RN",

        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003007001&bianhao=&xmmc= PN", #药品采购
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003007002&bianhao=&xmmc= CN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003007003&bianhao=&xmmc= RN",

        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003008001&bianhao=&xmmc= PN", #机电设备
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003008002&bianhao=&xmmc= CN",
        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003008003&bianhao=&xmmc= RN",

        # "http://218.4.45.172:8085/services/XzsJsggWebservice/getListByCount?response=application/json&&categorynum=003009&bianhao=&xmmc= PN" #其他交易
    ]
    Debug = True
    doredis = True
    # source = u"苏州市公共资源交易电子服务平台"
    source = u"苏州市公共资源交易中心"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"DOWNLOAD_TIMEOUT":60.0}

    def __init__(self,start_url=None,history=False):
        super(jsszggzy, self).__init__()
        # jobs = start_url.spli t('|')
        jobs = self.start_urls
        for job in jobs:
            self.post_params.append({"url":job.split()[0],"ba_type":job.split()[1]})
        # dispatcher.connect(self.initial, signals.engine_started)
        self.history = history

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
            # if self.doredis and self.expire_redis.exists(url):
            #    continue
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"],"page_parse":True,"get_page":True},callback=self.parse_link)

    def parse_link(self, response):
        totalcounts = int(json.loads(response.body)["return"])
        categorynum = re.search(r"categorynum=(.*?)&",response.url).group(1)
        if totalcounts % 15 == 0:
            page = totalcounts / 15
        else:
            page = totalcounts / 15 + 1
        if page >= 1:
            for i in range(1,int(page)+1):
                if i >1 and not self.history:
                    break
                url = "http://218.4.45.172:8085/services/XzsJsggWebservice/getList?response=application/json"
                url += "&pageIndex="+str(i)+"&pageSize=15&&categorynum="+categorynum+"&xmbh=&xmmc="
                yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"]},callback=self.parse_get_json)

    def parse_get_json(self,response):
            urls = json.loads(json.loads(response.body)["return"])["Table"]

            for index,url in enumerate(urls):
                final = urlparse.urljoin(response.url,url["href"])
                # if self.doredis and self.expire_redis.exists(final):
                #     continue
                pubtime = url["postdate"] + " 00:00"
                title = url["title"]
                yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"],"pubtime":pubtime,"title":title},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()

        item["pubtime"] = response.meta["pubtime"]
        item["type"] = response.meta["ba_type"]
        item['area'] = u'江苏省苏州市'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['title'] = response.meta["title"]
        item['content']= response.xpath("//div[@class='con']").extract()[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item


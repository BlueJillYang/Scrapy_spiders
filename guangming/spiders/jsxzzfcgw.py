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


class jsxzzfcgw(scrapy.Spider):
    name = "jsxzzfcgw"
    start_urls = [   #很恶心的一个网站，留着调试
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=4&page=1&pagesize=20 PN",
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=5&page=1&pagesize=20 PN",
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=331&page=1&pagesize=20 PN",
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=332&page=1&pagesize=20 CN",
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=333&page=1&pagesize=20 RN",
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=9&page=1&pagesize=20 RN",  #第二种
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=10&page=1&pagesize=20 RN", #第二种
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=44&page=1&pagesize=20 PN",
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=55&page=1&pagesize=20 PN",
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=334&page=1&pagesize=20 PN",
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=335&page=1&pagesize=20 CN",
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=336&page=1&pagesize=20 RN",
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=919&page=1&pagesize=20 RN", #第二种
        "http://www.ccgp-xuzhou.gov.cn/Home/PageListJson?sidx=createdate&category_id=1010&page=1&pagesize=20 RN"  #第二种
    ]
    Debug = True
    doredis = True
    source = u"徐州政府采购网"
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"CLOSESPIDER_TIMEOUT": 10800}

    def __init__(self, start_url = None,history = True):
        super(jsxzzfcgw, self).__init__()
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
            # if self.doredis and self.expire_redis.exists(url):
            #     continue
            if self.history:
                parse_page = True
            else:
                parse_page = False
            yield Request(url=url,method='get',meta={"ba_type":channel["ba_type"], "parse_page":parse_page},callback=self.parse_item)

    def get_category_id(self,category_id):
        if category_id == 9:
            return {"id":"2","key":"contractsid","title":"contractsname","pubtime":"entrytime"}
        elif category_id == 919:
            return {"id":"919","key":"contractsid","title":"contractsname","pubtime":"entrytime"}
        elif category_id == 331 or category_id ==332 or category_id ==333 or category_id ==334 or category_id ==335 or category_id ==336:
            return {"id":"0","key":"bulletinid","title":"bulletintitle","content":"bulletinidcontent","pubtime":"createdate"}
        elif category_id == 10 or  category_id ==1010:
            return {"id":"10","key":"contractid","title":"contracttitle","pubtime":"createdate"}
        elif category_id == 22:
            return {"id":"1","key":"articleid","title":"title","pubtime":"createdate"}
        else:
            return {"id":str(category_id),"key":"articleid","title":"title","content":"content","pubtime":"createdate"}

    def get_Time(self,time):
        if "." not in time:
                utc = "%Y-%m-%dT%H:%M:%S"
        else:
                utc = "%Y-%m-%dT%H:%M:%S.%f"
        return datetime.datetime.strptime(time, utc).strftime("%Y-%m-%d %H:%M")

    def change_uncode_str(self,row):
        new_row = {}
        for key in row.keys():
            if row[key]:
               new_row[key] = row[key]
            else:
               new_row[key] = u""
        return new_row

    def get_content(self,category_id,row):
         row = self.change_uncode_str(row)
         content = ""
         if category_id == 2:
               content = u"<p>一、采购单位：" + row["purchasingunit"] \
               + u"</p><p>二、采购预算（元）：" + str(row["procurementbudget"]).decode('utf-8') \
               + u"</p><p>三、编号：" + row["contractscode"] \
               + u"</p><p>四、合同名称：" + row["contractsname"] \
               + u"</p><p>五、采购项目编号：" + row["purchaseitemcode"] \
               + u"</p><p>六、项目名称：" + row["purchaseitemname"] \
               + u"</p><p>七、中标供应商：" + row["bidwinner"] \
               + u"</p><p>八、合同金额（元）：" + str(row["contractamount"]).decode('utf-8') \
               + u"</p><p>九、合同签订日期：" + self.get_Time(row["datesigned"]) \
               + u"</p><p>十、合同公告日期：" + self.get_Time(row["noticedate"]) \
               + u"</p><p>十一、代理机构：" + row["agentname"] \
               + u"</p><p>合同附件：<a href='" + row["attachment"] + u"'>点击下载</p>"
         elif category_id == 919:
               content = u"<p>一、采购单位：" + row["purchasingunit"] \
               + u"</p><p>二、采购预算（元）：" + str(row["procurementbudget"]).decode('utf-8') \
               + u"</p><p>三、编号：" + row["contractscode"] \
               + u"</p><p>四、合同名称：" + row["contractsname"] \
               + u"</p><p>五、采购项目编号：" + row["purchaseitemcode"] \
               + u"</p><p>六、项目名称：" + row["purchaseitemname"] \
               + u"</p><p>七、中标供应商：" + row["bidwinner"] \
               + u"</p><p>八、合同金额（元）：" +  str(row["contractamount"]).decode('utf-8') \
               + u"</p><p>九、合同签订日期：" + self.get_Time(row["datesigned"]) \
               + u"</p><p>十、合同公告日期：" + self.get_Time(row["noticedate"]) \
               + u"</p><p>十一、代理机构：" + row["agentname"] \
               + u"</p><p>合同附件2：<a href='" + row["attachment"] + u"'>点击下载</a></p>"
         elif category_id == 10:
                fj = u""
                if row["attachment"]:
                    fj =u"<a href='" + row["attachment"] + u"' target='_blank'>点击下载</a>"
                content = u"<p>一、合同名称：" + row["contractname"] \
                + u"</p><p>二、中标（成交）供应商：" + row["supplier"]\
                + u"</p><p>三、 合同金额：" + str(row["money"]).decode('utf-8') \
                + u"</p><p>四、履约主要内容：" + row["maincontent"]\
                + u"</p><p>五、验收结论性意见：" + row["concludingcomments"] \
                + u"</p><p>六、验收小组成员名单：" + row["members"] \
                + u"</p><p>七、联系方式：" + row["phone"] \
                + u"</p><p>八、验收附件：" + fj + u"</p>"
         return content

    def parse_item(self, response):
        jsonMap = json.loads(response.body)
        category_id = re.search(r"category_id=(\d+?)&",response.url).group(1)
        category = self.get_category_id(int(category_id))

        for row in jsonMap["rows"]:
            final = "HomeDetails?type="+ category["id"] +"&articleid=" + row[category["key"]]
            final = urlparse.urljoin(response.url,final)
            # if self.doredis and self.expire_redis.exists(final):
            #      continue
            item = DataItem()
            item["type"] = response.meta["ba_type"]
            item['area'] = u'江苏省徐州市'
            item['source'] = self.source
            item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
            item["pubtime"] = self.get_Time(row[category["pubtime"]])
            item["title"] = row[category["title"]]
            item["url"] = final
            if category["id"] == "2" or category["id"] == "10" or category["id"] == "919" or category["id"] == "1010":
               content_url = final.replace("HomeDetails","PageDetailsJson")
               yield Request(url=content_url,method='get',meta={"category_id":int(category["id"]),"item":item},callback=self.parse_get_content)
            else:
                item["content"] = row[category["content"]]
                if item['pubtime'] and item['title'] and item['content']:
                   yield item
        if self.history and response.meta["parse_page"] and int(jsonMap["total"]) > 1:
            for i in range(2,int(jsonMap["total"])+1):
                final = re.sub(r"page=\d{1,3}?&","page="+str(i)+"&",response.url)
                yield Request(url=final,method='get',meta={"ba_type":response.meta["ba_type"],"parse_page": False},callback=self.parse_item)

    def parse_get_content(self,response):
         rows = json.loads(response.body)["rows"]
         item = response.meta["item"]
         item["content"] = self.get_content(response.meta["category_id"],rows[0])
         if item['pubtime'] and item['title'] and item['content']:
            yield item

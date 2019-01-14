#!/usr/bin/python
#-*- coding: utf-8 -*-import sys
import re
import time
import sys
import scrapy
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
from scrapy.http.cookies import CookieJar
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


class Sdjnggzyjy(scrapy.Spider):
    name = "sdjnggzyjy"
    start_urls = [
        'http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=503000 PN',  # 招标公告
        # 'http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=503002 CN',  # 更正公告
        # 'http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=504002 CN',  # 澄清答疑
        # 'http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=511001 RN',  # 中标公示
        # 'http://www.jnggzyjy.gov.cn/JiNing/Bulletins?CategoryCode=513001 RN',  # 中标结果公告
        # 理论上条 实际采集条
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY":False,
                       "DOWNLOAD_DELAY":0.1,
                       "DOWNLOAD_TIMEOUT":15}

    def __init__(self, start_url = None,history=True):
        super(Sdjnggzyjy, self).__init__()
        # jobs = start_url.split('|')
        jobs = self.start_urls
        self.cookie_jar = CookieJar()
        self.count = 0
        for job in jobs:
            self.headers = {
                'Accept application/json, text/javascript, */*;':'q=0.01',
                # 'Accept-Encoding':'gzip,deflate',
                'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Connection':'keep-alive',
                'Content-Length':'90',
                'Content-Type':'application/json',
                # 'User-Agent Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101':'Firefox/64.0',
                'Host': 'www.jnggzyjy.gov.cn',
                'Referer': job.split()[0],
                'Public-X-XSRF-TOKEN': '',
                # 'X-Requested-With':'XMLHttpRequest',
            }
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
        cookies = None
        post_json_url = 'http://www.jnggzyjy.gov.cn/api/services/app/stPrtBulletin/GetBulletinList'
        categoryCodes = response.xpath('//div[@class="table-panel-body"]/div[@id]/@id').extract()
        if response.headers.get('Set-Cookie'):
            cookies = response.headers['Set-Cookie']
        if cookies:
            cookie_dict = {}
            cookie_list = []
            self.cookie_jar.extract_cookies(response, response.request)
            for cookie in self.cookie_jar:
                # print str(cookie)
                result = re.search(r'<Cookie\s(\S+)=(\S+)\s.+>', str(cookie))
                cookie_dict['%s'%result.group(1)] = result.group(2)
                cookie_list.append(re.search(r'<Cookie\s(\S+=\S+)\s.+>', str(cookie)).group(1))
            cookie_str = ';'.join(cookie_list)
            print cookie_str
            # print cookies
            XSRF_KEY = re.search(r'Public-XSRF-TOKEN=(\S+);', response.headers.get('Set-Cookie')).group(1)
            self.headers['Public-X-XSRF-TOKEN'] = XSRF_KEY
            # self.headers['Cookie'] = cookie_str
            if len(categoryCodes) > 0:
                for categoryCode in categoryCodes:
                    categoryCode = re.search(r'\d+', categoryCode).group()
                    # print categoryCode
                    formData = {'categoryCode': str(categoryCode), 'FilterText': ' ',
                                'maxResultCount': '20', 'skipCount': '0', 'tenantld': '3'}
                    print '开始请求post ', formData
                    yield FormRequest(url=post_json_url,formdata=formData,headers=self.headers,cookies=cookie_dict,
                                      meta={"ba_type":response.meta["ba_type"],
                                            "page_parse":False},callback=self.parse_link)
        else:
            print response.body
            print '处理json'
            splitUrls = response.url.split('?')  # 之后做目标url处理需要
            jsonDict = json.loads(response.body_as_unicode())
            jsonDict = jsonDict['result']
            totalCount = jsonDict['totalCount']
            if int(totalCount)%20 == 0:
                totalPage = int(totalCount)//20
            else:
                totalPage = int(totalCount)//20 + 1
            print 'totalPage', totalPage
            items = jsonDict['items']
            for each in items:
                title = each['title']
                id = each['id']
                categoryCode = each['categoryCode']
                pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', each['releaseDate']).group() + '00:00'
                url = splitUrls[0]+ '/Detail/%s?CategoryCode=%s'.format(str(id),str(categoryCode))
                print url
                yield Request(url=url,method='get',meta={"ba_type":response.meta["ba_type"],
                                                         'title': title, 'pubtime': pubtime,
                                                         "page_parse":False},callback=self.parse_item)

            # if self.history and response.meta["page_parse"]:
            #     formdata = {'categoryCode': '这个要找cateID', 'FilterText': '', 'maxResultCount': '20', 'skipCount': '要变0', 'tenantld': '3'}
            #     page_rule = response.xpath('//div[@class="kongge"][last()]/span/text()').extract()
            #     if len(page_rule) > 0:
            #         final_page = re.search(r'\d+', page_rule[0]).group()
            #         for i in range(1, int(final_page)):
            #             pageStart = str(1+33*i)
            #             final_url = 'http://gkfw.xq.gov.cn:8080/gk/list_zfxxgkml.jsp?pageStart=%s&pageSize=33&xxCode=080100'%pageStart
            #             print final_url
            #             yield Request(url=final_url,meta={"ba_type":response.meta["ba_type"],"page_parse":False},
            #                           callback=self.parse_link)

    def parse_item(self, response):
        item = DataItem()
        self.count += 1
        print '处理了%d条'%self.count
        item["pubtime"] = response.meta["pubtime"]
        item['title'] = response.xpath('//h2/text()').extract()
        if len(item['title']) > 0:
            item['title'] = item['title'][0].strip()
        else:
            item['title'] = response.meta['title']
        item["type"] = response.meta["ba_type"]
        if u'成交公' in item['title'] or u'结果' in item['title'] or u'中标' in item['title'] or \
                u'未入围' in item['title'] or u'失败公' in item['title'] or u'合同公' in item['title'] or \
                u'结果有关事宜公告' in item['title'] or u'中止' in item['title'] or \
                u'终止' in item['title']:
            item['type'] = 'RN'
        elif u'变更' in item['title'] or u'澄清' in item['title'] or u'答疑' in item['title'] or \
                u'更正' in item['title'] or u'更改' in item['title']:
            item['type'] = 'CN'
        elif u'招标公' in item['title'] or u'磋商' in item['title'] or u'采购公' in item['title'] or\
                u'出让公告' in item['title'] or u'资格预审' in item['title']:
            item['type'] = 'PN'
        elif u'预告' in item['title']:
            item['type'] = 'PF'
        item['area'] = u'山东省济宁市'
        item['source'] = u'济宁市公共资源交易网'
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url
        item['content'] = response.xpath('//div[@class="panel-body"]').extract()
        if len(item['content']) > 0:
            item['content'] = item['content'][0]
        else:
            print 'content有问题:  %s'%response.url
        # print item
        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            raise Exception('字段出现问题 pubtime:{}, title:{}, url:{},content:{}'.format(item['pubtime'],
                                                                                    item['title'], response.url, item['content']))

    def initial(self):
        # if self.doredis:
        #     self.expire_redis = redis.Redis(host=self.configure.yq_filter_db_other.host,
        #                              port=self.configure.yq_filter_db_other.port,
        #                              db=self.configure.yq_filter_db_other.db,
        #                              password=self.configure.yq_filter_db_other.password)
        pass

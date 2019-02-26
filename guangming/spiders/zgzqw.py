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
import time
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
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Zgzqw(scrapy.Spider):
    name = "zgzqw"  # 中国证券网
    start_urls = [
        'http://news.cnstock.com/bwsd/index.html news',  # 快讯
        'http://news.cnstock.com/news/sns_jg/index.html news',  # 要闻
        'http://news.cnstock.com/news/sns_yw/index.html news',  # 宏观
        'http://news.cnstock.com/industry/sid_rdjj news',  # 产业聚焦
        'http://app.cnstock.com/api/theme/get_theme_list?callback=jQuery1910763797256853403_{}&maxid=0&minid=0&size=5&_={} news',  # 上证四小时
        'http://ggjd.cnstock.com/gglist/search/qmtbbdj news',  # 本网独家
        'http://ggjd.cnstock.com/gglist/search/ggkx news',  # 公告快讯
        'http://company.cnstock.com/company/scp_gsxw news',  # 公司聚焦
        'http://stock.cnstock.com/live news',  # 直播
        'http://stock.cnstock.com/xg/sx_ipopl news',  # ipo
        'http://stock.cnstock.com/xg/sx_zcdt news',  # 政策动态
        'http://stock.cnstock.com/xg/sx_xgcl news',  # 新股策略
        'http://stock.cnstock.com/xg/sx_xgjj news',  # 新股聚焦
        'http://news.cnstock.com/news/sns_qy/index.html news',  # 券页
        'http://jrz.cnstock.com/ news',  # 中国新三板
        'http://blog.cnstock.com/NewsList.aspx?cat=djsy news',  # 名家声音
        ##  'http://blog.cnstock.com/ShowList.aspx?action=14 news',  # 基本上一个博客页面就是一种规则
        'http://ggjd.cnstock.com/company/scp_ggjd/tjd_ggjj news',  # 公告集锦
        'http://stock.cnstock.com/stock/smk_dsyp news',  # 大势研判
        'http://stock.cnstock.com/stock/smk_jjdx news',  # 集锦动向
        'http://jrz.cnstock.com/yw/ news',  # 新三板-要闻
        'http://news.cnstock.com/news/sns_zxk/index.html news',  # 咨询库
        'http://ggjd.cnstock.com/company/scp_ggjd/tjd_ggjj news',  # 公告集锦
        'http://data.cnstock.com/list/industrylist-1.html news',  # 数据-最新报告
        'http://data.cnstock.com/list/focuslist-1.html news',  # 数据-焦点

        # 不同请求类型
        'http://company.cnstock.com/ggjj.html news',  # 公告集锦
        'http://stock.cnstock.com/stare.html news',  # 帮你盯盘
        'http://www.cnstock.com/goldrush.html news',  # 市场淘金
        'http://stock.cnstock.com/jj.html news',  # 基金
        'http://stock.cnstock.com/zq.html news',  # 债券
        'http://stock.cnstock.com/xt.html news',  # 信托
        'http://www.cnstock.com/reading.html news',  # 开盘必读
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.1,
                       "DOWNLOAD_TIMEOUT": 10}

    def __init__(self,start_url=None,history=True):
        super(Zgzqw, self).__init__()
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
            current_time = int(time.time()*1000)
            url = url.format(current_time, current_time+1)
            if 'api' in url:
                print 'api类型', url
                yield Request(url=url,method='get',meta={'ba_type':channel['ba_type']},callback=self.parse_ajax_link)
            elif 'html' in url and 'index' not in url and 'list' not in url:
                print 'jquery类型', url
                type_jquery = {'jj': '19103124428547938849', 'zq': '19108781173118268422',
                               'xt': '19106709901839700254', 'goldrush': '19103843607145964574',
                               'ggjj': '19107906189864170476', 'reading': '191020722508899016634',
                               'stare': 'Another_type'}
                j_type = re.search(r'com/(.+?)\.html', url).group(1)
                if j_type == 'goldrush':
                    j_type_format = 'sctj'
                elif j_type == 'reading':
                    j_type_format = 'kpbd'
                else:
                    j_type_format = j_type
                final_url = 'http://app.cnstock.com/api/waterfall?callback=jQuery{}'.format(type_jquery[j_type]) + '_{}&colunm='.format(current_time) + j_type_format + '&page=1&num=20&showstock=0&_={}'.format(current_time+1)
                headers = {
                    'Host': 'app.cnstock.com',
                    'Referer': url
                }
                if 'stare' in url:
                    final_url = 'http://zb.cnstock.com/quoteMot/getQuteScanData.do?callback=jQuery19101448920715932731_{}&colunm=watchingStock&page=1&num=20&showstock=0&_={}'.format(current_time, current_time+1)
                    print final_url
                    yield Request(url=final_url,method='get',headers=headers,meta={'ba_type':channel['ba_type'],'url':url},callback=self.parse_another_item)
                else:
                    print final_url
                    yield Request(url=final_url,method='get',headers=headers,meta={'ba_type':channel['ba_type']},callback=self.parse_ajax_link)
            else:
                print '普通类型', url
                yield Request(url=url,method='get',meta={'ba_type':channel['ba_type']},callback=self.parse_link)

    def get_xpath_rules(self, response):
        xpath_rules = [
            '//body/div[3]/div[2]/div/ul/li/a/@href',
            '//*[@id="bw-list"]/li/p/a/@href',
            '//ul[@class="new-list article-mini"]//a/@href',
            '//ul[@class="focus-list"]//a/@href',
            '//ul[@class="new-list"]//a/@href',
            '//ul[@class="zb-list"]//a/@href',
            '//h1/a/@href',
            '//ul[@class="article-mini new-list focus-list"]//li/a[1]/@href',
            '//ul[@id="j_waterfall_list"]//a/@href',
        ]
        for xpath_rule in xpath_rules:
            result = response.xpath(xpath_rule)
            if len(result) > 0:
                print '套用规则： ', xpath_rule
                return xpath_rule
        print '需要xpath规则', response.url

    def parse_ajax_link(self, response):
        # print response.url
        # print response.body
        # jsonDict = json.loads(re.search(r'\{.+}', response.body).group())
        # print jsonDict
        id_list = re.findall(r'id.*?(\d+)', response.body)
        link_list = re.findall(r'link.*?"(http.+?)"', response.body)
        if len(link_list) > 0:
            print 'link类型'
            for link in link_list:
                link = link.replace('\\', '')
                print link
                if 'theme' in link:
                    yield Request(url=link,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_link)
                else:
                    yield Request(url=link,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_item)
        else:
            print 'id类型'
            for ids in id_list:
                get_url = 'http://news.cnstock.com/theme,{}.html'.format(ids)
                print get_url
                # print ids
                yield Request(url=get_url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        xpath_rule = self.get_xpath_rules(response)
        print xpath_rule
        url_list = response.xpath(xpath_rule).extract()
        # print 'url_list',len(url_list), response.url
        for url in url_list:
            url = urlparse.urljoin(response.url, url)
            print url
            # if self.doredis and self.expire_redis.exists(final):
            #    continue
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_item)

    # 帮你盯盘特殊item
    def parse_another_item(self, response):
        # print response.body
        jsonDict =json.loads(re.search(r'{.+}', response.body).group())['item']
        # print jsonDict
        for info in jsonDict:
            item = DataItem()
            item["type"] = response.meta["ba_type"]
            item['area'] = u'中国'
            item['source'] = u"中国证券网"
            item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
            item['url'] = response.meta['url']

            pubtime = info['time']
            final_pubtime = re.search(r'20\d{2}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}', pubtime).group()
            item['pubtime'] = final_pubtime

            title = info.get('title') or info.get('id')
            item['title'] = title

            content = info['desc']
            item['content'] = content
            item['medianame'] = u'中国证券网'
            yield item

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'中国'
        item['source'] = u"中国证券网"
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url

        medianame = response.xpath('//span[@class="col cite"]/text()').extract() or \
                    response.xpath('//span[@class="cite"]/text()').extract()
        medianame1 = response.xpath('//span[@class="source"]/a/text()').extract()
        if len(medianame) > 0:
            medianame = medianame[0].strip().replace(' ', '')
            if medianame:
                item['medianame'] = medianame
            else:
                item['medianame'] = u"中国证券网"
        elif len(medianame1) > 0:
            item['medianame'] = ''.join(medianame1)
        elif response.meta.get('medianame'):
            item['medianame'] = response.meta['medianame']
        else:
            item['medianame'] = u"中国证券网"

        pubtime = response.xpath('//span[@class="timer"]/text()').extract() or \
                  response.xpath('//div[@class="ll-time"]/text()').extract() or \
                  response.xpath('//span[@class="time"]/text()').extract() or \
                  response.xpath('//span[@id="arttitle"]/ancestor::tr[1]/following-sibling::tr//span[@class="textbox-label"]/text()[1]').extract() or \
                  response.xpath('//p[@id="arttitle"]/following-sibling::p/text()[last()]').extract()
        pubtime1 = response.xpath('//div[@class="comtime"]') or \
                   response.xpath('//*[@id="chkvip"]/..')
        if len(pubtime) == 0 and len(pubtime1) > 0:
            pubtime = pubtime1.xpath('string(.)').extract()

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

        title = response.xpath('//div[@class="title"]/text()').extract() or \
                response.xpath('//h1[@class="title"]/text()').extract() or \
                response.xpath('//*[@id="arttitle"]/text()').extract() or \
                response.xpath('//*[@class="Ptitle"]/text()[1]').extract()
        title1 = response.xpath('//div[@class="headline"]/h1//text()').extract() or \
                 response.xpath('//div[@class="topic"]/text()').extract()
        if len(title) > 0:
            item['title'] = title[0].strip()
        elif len(title1) > 0:
            item['title'] = ''.join(title1)

        content = response.xpath('//div[@class="content"]').extract() or \
                  response.xpath('//*[@class="logtext"]').extract() or \
                  response.xpath('//*[@class="Pcontent"]').extract() or \
                  response.xpath('//*[@class="artbody"]').extract() or \
                  response.xpath('//*[@class="textbox-content"]').extract()
        item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content']:
            yield item
        else:
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



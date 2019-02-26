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
from ..items import DataItem

reload(sys)
sys.setdefaultencoding('utf-8')


class Btime(scrapy.Spider):
    name = "btime"  # 北京时间
    start_urls = [
        'https://www.btime.com/recommend news',  # 推荐
        'https://www.btime.com/xinshidai news',  # 新时代
        'https://www.btime.com/news news',  # 新闻
        'https://www.btime.com/world news',  # 国际
        'https://www.btime.com/ent news',  # 娱乐
        'https://www.btime.com/video news',  # 视频
        'https://www.btime.com/finance news',  # 财经
        'https://www.btime.com/sports news',  # 运动
        'https://www.btime.com/mil news',  # 军事
        ### 'https://www.btime.com/live news',  # 直播
        'https://www.btime.com/auto news',  # 汽车
        'https://www.btime.com/House news',  # 房产
        'https://www.btime.com/tech news',  # 科技
        'https://www.btime.com/dongao news',  # 东奥
        'https://www.btime.com/life news',  # 生活
        'https://www.btime.com/fun news',  # 搞笑
        'https://www.btime.com/culture news',  # 文化
        'https://www.btime.com/Health news',  # 健康
        'https://www.btime.com/internet news',  # 互联网
        'https://www.btime.com/game news',  # 游戏
        'https://www.btime.com/fashion news',  # 时尚
        'https://www.btime.com/baby news',  # 亲子
        'https://www.btime.com/bitcoin news',  # 区块链
        'https://www.btime.com/tour news',  # 旅游
        'https://www.btime.com/astro news',  # 星座
        'https://www.btime.com/emotion news',  # 情感
        'https://www.btime.com/education news',  # 教育
        'https://www.btime.com/cyol news',  # 中情报
        'https://www.btime.com/bjMediaXjb news',  # 新京报
        'https://www.btime.com/bjMediaSb news',  # 北京商报
        'https://www.btime.com/bjMediaFzwb news',  # 法制晚报
        'https://www.btime.com/bjMediaBjqnb news',  # 北京青年报

        # # BTV等 有部分是直播 有部分加载不出 有部分是专题
        'https://www.btime.com/btv/btvsy_index news',  # btv 有部分是专题
        'https://www.btime.com/btv/btvws_index news',  # 北京卫视
        'https://www.btime.com/btv/btvwy_index news',  # BTV文艺
        'https://www.btime.com/btv/btvkj_index news',  # BTV科教
        'https://www.btime.com/btv/btvys_index news',  # BTV影视
        'https://www.btime.com/btv/btvcj_index news',  # BTV财经
        'https://www.btime.com/btv/btvty_index news',  # BTV体育
        ## 'https://www.btime.com/btv/btvsh_index news',  # BTV i生活 这个频道没有响应内容
        'https://www.btime.com/btv/btvqn_index news',  # BTV青年
        'https://www.btime.com/btv/btvxw_index news',  # BTV新闻
        'https://www.btime.com/btv/btvse_index news',  # 卡酷少儿
        'https://www.btime.com/btv/btvjs_index news',  # BTV纪实

        'https://www.btime.com/local/110000 news',  # 北京市
        'https://www.btime.com/local/120000 news',  # 天津市
        'https://www.btime.com/local/130000 news',  # 河北省
        'https://www.btime.com/local/140000 news',  # 山西省
        'https://www.btime.com/local/150000 news',  # 内蒙古自治区
        'https://www.btime.com/local/210000 news',  # 辽宁省
        'https://www.btime.com/local/220000 news',  # 吉林省
        'https://www.btime.com/local/230000 news',  # 黑龙江省
        'https://www.btime.com/local/310000 news',  # 上海市
        'https://www.btime.com/local/320000 news',  # 江苏省
        'https://www.btime.com/local/340000 news',  # 安徽省
        'https://www.btime.com/local/330000 news',  # 浙江省
        'https://www.btime.com/local/350000 news',  # 福建省
        'https://www.btime.com/local/360000 news',  # 江西省
        'https://www.btime.com/local/370000 news',  # 山东省
        'https://www.btime.com/local/410000 news',  # 河南省
        'https://www.btime.com/local/420000 news',  # 湖北省
        'https://www.btime.com/local/430000 news',  # 湖南省
        'https://www.btime.com/local/440000 news',  # 广东省
        'https://www.btime.com/local/450000 news',  # 广西壮族自治区
        'https://www.btime.com/local/460000 news',  # 海南省
        'https://www.btime.com/local/500000 news',  # 重庆市
        'https://www.btime.com/local/510000 news',  # 四川省
        'https://www.btime.com/local/520000 news',  # 贵州省
        'https://www.btime.com/local/530000 news',  # 云南省
        'https://www.btime.com/local/540000 news',  # 西藏自治区
        'https://www.btime.com/local/610000 news',  # 陕西省
        'https://www.btime.com/local/620000 news',  # 甘肃省
        'https://www.btime.com/local/630000 news',  # 青海省
        'https://www.btime.com/local/640000 news',  # 宁夏回族自治区
        'https://www.btime.com/local/650000 news',  # 新疆维吾尔自治区
        'https://record.btime.com/show?uid=2213419 news',  # 大佬时间
        'https://record.btime.com/show?uid=2426339 news',  # 时间娱乐
        'https://record.btime.com/show?uid=1077616 news',  # 时间财经
        'https://record.btime.com/show?uid=1667407 news',  # 时间视频
        'https://h5.btime.com/news/subjectNewsList?cid=f580bkthpe48vcb59oimmd8274n news',  # 时间新闻
        'http://h5.btime.com/news/subjectNewsList?cid=f40u5e3rb5b9vfo12fj7e3h5v6i news',  # 时间夜总会
        'http://h5.btime.com/news/subjectNewsList?cid=f2lthchf0oq8blohmhja1ivu5p9 news',  # 法治时间
        'http://h5.btime.com/news/subjectNewsList?cid=f7nrhtjlgpq8ffa6a8rllgnmvg4 news',  # 时间新闻室
        'http://h5.btime.com/news/subjectNewsList?cid=f4kh3tqnpht8qtoos2e8gk38u5c news',  # 锐评
        'http://h5.btime.com/news/subjectNewsList?cid=f3e8cvpeakl9s1amn44iv8vsjma news',  # 昨夜今晨
        'http://h5.btime.com/news/subjectNewsList?cid=f1kvqvjopb68r0adphhdhbuuuve news',  # 时间晚参
        'http://h5.btime.com/news/subjectNewsList?cid=f523gkg6dtp8j2rpiv47k5h2e2b news',  # 北京电台
        'http://h5.btime.com/news/subjectNewsList?cid=artificial_0iij1c9as68okpiu8edj9t2mda news',  # 24小时热点
    ]
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.5,
                       "DOWNLOAD_TIMEOUT": 10}

    def __init__(self,start_url=None,history=True):
        super(Btime, self).__init__()
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
            if 'uid' in url:
                uid = re.search(r'uid=(\d+)', url).group(1)
                url = 'https://record.btime.com/getNews?tab=all&lastTime=&pageRow=10&uid={}&refresh=1&target=v4'.format(uid)
            elif 'cid' in url:
                cid = re.search(r'cid=(\S+)', url).group(1)
                url = 'https://h5.btime.com/news/getSubjectNews?cid={}&refresh_total=1&_=&callback=jsonp1'.format(cid)
            yield Request(url=url,method='get',meta={'ba_type':channel['ba_type']},callback=self.parse_link)

    def parse_link(self, response):
        url_list = re.findall(r'"gid":"(.*?)",.+?pdate.+?(\d+).+?"source":"(\S+?)",', response.body)
        print 'url_list',len(url_list), response.url
        for url, timestamp,source in url_list:
            if url:
                url = urlparse.urljoin('https://item.btime.com/', url)
                timeArray = time.localtime(int(timestamp))
                pubtime = time.strftime('%Y-%m-%d %H:%M', timeArray)
                medianame = source
                # if self.doredis and self.expire_redis.exists(final):
                #    continue
                yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime,'medianame':medianame},callback=self.parse_item)

    def parse_item(self, response):
        if u'//专题页' in response.body:
            url_list = re.findall(r'"gid":"(.*?)",.+?pdate.+?(\d+).+?"source":"(\S+)",', response.body)
            print 'url_list',len(url_list), response.url
            for url, timestamp,source in url_list:
                if url:
                    url = urlparse.urljoin('https://item.btime.com/', url)
                    timeArray = time.localtime(int(timestamp))
                    pubtime = time.strftime('%Y-%m-%d %H:%M', timeArray)
                    medianame = source
                    # if self.doredis and self.expire_redis.exists(final):
                    #    continue
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'pubtime':pubtime,'medianame':medianame},callback=self.parse_item)

        else:
            item = DataItem()
            item["type"] = response.meta["ba_type"]
            item['area'] = u'北京市'
            item['source'] = u"北京时间"
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

            if u'给主播捧个场吧' in response.body:
                print '直播类型'
            elif item['pubtime'] and item['title'] and item['content']:
                yield item
            else:
                print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'])



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


class Dahewang(scrapy.Spider):
    name = "dahewang"  # 大河网
    start_urls = [
        # 新闻中心
        'https://news.dahe.cn/hnyw/ news',  # 新闻中心-聚焦河南
        'https://news.dahe.cn/dybd/ news',  # 新闻中心-第一报道
        'https://news.dahe.cn/nxw/ news',  # 暖新闻
        'https://news.dahe.cn/sjldbdj/ news',  # 省领导报道集
        'https://news.dahe.cn/rsrm/ news',  # 人事任免
        'https://news.dahe.cn/ty/ news',  # 体育
        'https://news.dahe.cn/shgc27/ news',  # 史海钩沉
        'https://news.dahe.cn/nxss/ news',  # 女性时尚
        'https://news.dahe.cn/gn27/ news',  # 国内新闻
        'https://news.dahe.cn/gj27/ news',  # 国际新闻
        'https://news.dahe.cn/sh27/ news',  # 社会
        'https://news.dahe.cn/kj27/ news',  # 科技
        'https://news.dahe.cn/ws27/ news',  # 文史
        'https://news.dahe.cn/dysj/ news',  # 第一时间
        'https://news.dahe.cn/yl/ news',  # 娱乐
        'https://news.dahe.cn/sd365/ news',  # 深读365
        'https://news.dahe.cn/jd27/ news',  # 荐读
        'https://news.dahe.cn/dhclf/ news',  # 大河财立方

        # 图片频道
        'https://photo.dahe.cn/dhyc/ news',  # 大河网景
        'https://photo.dahe.cn/gsh/ news',  # 故事汇
        'https://photo.dahe.cn/xwy/ news',  # 新闻眼
        'https://photo.dahe.cn/mpt/ news',  # 名品堂
        'https://photo.dahe.cn/yxz/ news',  # 影像志
        'https://photo.dahe.cn/txg/ news',  # 天下观

        # 评论频道
        'https://opinion.dahe.cn/ news',

        # 视频
        'https://v.dahe.cn/syjdt26/ news',  # 豫视点
        'https://v.dahe.cn/dhwy26/ news',  # 大河网约
        'https://v.dahe.cn/wzhn26/ news',  # 我@河南
        'https://v.dahe.cn/dhwwsp26/ news',  # 大河网微视频
        'https://v.dahe.cn/jlhn26/ news',  # 视频集萃
        'https://v.dahe.cn/gddh26/ news',  # 高端对话
        'https://v.dahe.cn/rddjt26/ news',  # 热点大家谈

        # bbs众多论坛
        'http://bbs.dahe.cn/ forum',

        # 理论
        'https://theory.dahe.cn/zdtj19/ news',  # 重点推荐
        'https://theory.dahe.cn/llzx19/ news',  # 理论资讯
        'https://theory.dahe.cn/wszy19/ news',  # 微视中原
        'https://theory.dahe.cn/xstj19/ news',  # 新书推荐
        'https://theory.dahe.cn/mjzl19/ news',  # 名家专栏

        # 专题
        ### 'https://news.dahe.cn/2018xwzthz27/ news',  # 专题类 一个专题一个规则

        # 教育
        'https://edu.dahe.cn/2jyyw/ news',  # 教育要闻
        'https://edu.dahe.cn/2xyxw/ news',  # 校园新闻
        'https://edu.dahe.cn/gdxw/ news',  # 滚动新闻
        'https://edu.dahe.cn/2hdkb/ news',  # 活动快报
        'https://edu.dahe.cn/2tpxw/ news',  # 图片新闻
        'https://edu.dahe.cn/2xyzp/ news',  # 校园招聘
        'https://edu.dahe.cn/2jqts/ news',  # 近期投诉
        'https://edu.dahe.cn/2tszz/ news',  # 投诉追踪
        'https://edu.dahe.cn/2jylx/ news',  # 教育乱象

        # 健康
        'https://hnwj.dahe.cn/5xw/ news',  # 新闻
        'https://hnwj.dahe.cn/5ft/ news',  # 访谈

        ### 'https://hnwj.dahe.cn/5zt/ news',  # 专题
        'https://hnwj.dahe.cn/5jk/ news',  # 疾控
        'https://hnwj.dahe.cn/5fy/ news',  # 妇幼
        'https://hnwj.dahe.cn/5jcws/ news',  # 基层卫生
        'https://hnwj.dahe.cn/5hnzy/ news',  # 中医
        'https://hnwj.dahe.cn/5sy/ news',  # 食药
        'https://hnwj.dahe.cn/5wsjd/ news',  # 卫生监督
        'https://hnwj.dahe.cn/5yzyg/ news',  # 医政医馆
        'https://hnwj.dahe.cn/5sydj/ news',  # 生育登记
        'https://hnwj.dahe.cn/5jsjf/ news',  # 计生奖扶
        'https://hnwj.dahe.cn/5zccx/ news',  # 行业资讯
        'https://hnwj.dahe.cn/5pdtj/ news',  # 频道推荐
        'https://hnwj.dahe.cn/5xyxw/ news',  # 行业新闻
        'https://hnwj.dahe.cn/5yydt/ news',  # 医院动态
        'https://hnwj.dahe.cn/5yzhfz/ news',  # 院长话发展
        'https://hnwj.dahe.cn/5jrrd/ news',  # 今日热点
        'https://hnwj.dahe.cn/5yjxw/ news',  # 业界新闻
        'https://hnwj.dahe.cn/5ys/ news',  # 养生
        'https://hnwj.dahe.cn/5tsjk/ news',  # 图说健康
        'https://hnwj.dahe.cn/5ms/ news',  # 美食
        'https://hnwj.dahe.cn/5js/ news',  # 健身
        'https://hnwj.dahe.cn/5lx/ news',  # 两性
        'https://hnwj.dahe.cn/5mr/ news',  # 美容
        'https://hnwj.dahe.cn/5yy/ news',  # 医院

        # 旅游
        'https://tour.dahe.cn/ news',

        # 金融
        'https://jr.dahe.cn/cjyw/ news',  # 财经要闻
        'https://jr.dahe.cn/hncj/ news',  # 河南财经
        'https://jr.dahe.cn/lcbd/ news',  # 理财宝典
        'https://jr.dahe.cn/hlwhy/ news',  # 互联网+行业
        'https://jr.dahe.cn/cjxw/ news',  # 产经新闻
        'https://jr.dahe.cn/cjyhzx/ news',  # 银行资讯
        'https://jr.dahe.cn/cjjdt/ news',  # 焦点图
        'https://jr.dahe.cn/cjyhxw/ news',  # 银行新闻
        'https://jr.dahe.cn/ygyw/ news',  # 豫股要闻

        # 消费
        'https://xf.dahe.cn/ news',  # 消费

        # 大河号
        'https://dhh.dahe.cn/list news',

        # 电子报
        'http://newpaper.dahe.cn/hnrb/ newspaper',
        'http://newpaper.dahe.cn/hnrbncb/ newspaper',
        'http://newpaper.dahe.cn/dhb/ newspaper',
        'http://newpaper.dahe.cn/dhjkb/ newspaper',
        'http://newpaper.dahe.cn/hnsb/ newspaper',
        'http://newpaper.dahe.cn/jrab/ newspaper',
        'http://newpaper.dahe.cn/jrxf/ newspaper',

        ### 'http://wzw.dahe.cn/ newspaper',  #  这个子频道无法访问
        ### 'http://newpaper.dahe.cn/jrabybb/ newspaper',  # 太旧了 是2015年的文章 舍弃

        # 地方频道
        'https://city.dahe.cn/zhengzhou/ news',  # 郑州
        'https://city.dahe.cn/zhzw17/ news',  # 开封-智慧政务
        'https://city.dahe.cn/wzkf17/ news',  # 开封-问政开封
        'https://city.dahe.cn/rsrm17/ news',  # 开封-人事任免
        'https://city.dahe.cn/qxxw17/ news',  # 开封-杞县新闻
        'https://city.dahe.cn/wsxw17/ news',  # 开封-尉氏新闻
        'https://city.dahe.cn/cxythsfqxw17/ news',  # 开封-城乡一体化
        'https://city.dahe.cn/lyms17/ news',  # 开封-旅游美食
        'https://city.dahe.cn/jyws17/ news',  # 开封-教育卫生
        'https://city.dahe.cn/zfxw17/ news',  # 开封-政法新闻
        'https://city.dahe.cn/yw17/ news',  # 开封-要闻
        'https://city.dahe.cn/luoyang/ news',  # 洛阳
        'https://city.dahe.cn/pingdingshan/ news',  # 平顶山
        'https://city.dahe.cn/anyang/ news',  # 安阳
        'https://city.dahe.cn/hebi/ news',  # 鹤壁
        'https://city.dahe.cn/xinxiang/ news',  # 新乡
        'https://city.dahe.cn/jiaozuo/ news',  # 焦作
        'https://city.dahe.cn/puyang/ news',  # 濮阳
        'https://city.dahe.cn/xuchang/ news',  # 许昌
        'https://city.dahe.cn/luohe/ news',  # 漯河
        'https://city.dahe.cn/sanmenxia/ news',  # 三门峡
        'https://city.dahe.cn/nanyang/ news',  # 南阳
        'https://city.dahe.cn/shangqiu/ news',  # 商丘
        'https://city.dahe.cn/xinyang/ news',  # 信阳
        'https://city.dahe.cn/zhoukou/ news',  # 周口
        'https://city.dahe.cn/zhumadian/ news',  # 驻马店
        'https://city.dahe.cn/jiyuan/ news',  # 济源
    ]
    source = u'大河网'
    Debug = True
    doredis = True
    # configure = SpecialConfig()
    post_params = []
    custom_settings = {"ROBOTSTXT_OBEY": False, "DOWNLOAD_DELAY": 0.5,
                       "DOWNLOAD_TIMEOUT": 15, "RETRY_ENABLED": True, "RETRY_TIMES": 3}

    def __init__(self,start_url=None,history=True):
        super(Dahewang, self).__init__()
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
            channel_type = channel['ba_type']
            if channel_type == 'newspaper':
                yield Request(url=url,method='get',meta={'ba_type':channel_type,'page_parse':True},callback=self.re_direct)
            elif 'list' in url:
                formdata = {'page': '0', 'size': '40', 'userid': '', 'pageid': ''}
                yield FormRequest(url=url,formdata=formdata,meta={'ba_type':channel_type,'parse_json':True},callback=self.parse_link)
            else:
                yield Request(url=url,method='get',meta={'ba_type':channel_type},callback=self.parse_link)

    def re_direct(self, response):
        # 新闻报类有部分需要重定向
        url = re.search(r"document.location.href=\s*?'(http:\D+?htm)';", response.body)
        if url:
            url = url.group(1)
        else:
            url = response.url
        yield Request(url=url,method='get',dont_filter=True,meta={'ba_type':response.meta['ba_type'],'page_parse':response.meta['page_parse']},callback=self.parse_newspaper_link)

    def get_parse_link_urls(self, response, url):
        xpath_rules = [
            '//ul[@id="content"]/li[position()<41]/a/@href',
            '//div[@id="listAll"]/dl[position()<41]/div/a/@href',
            '//div[@id="listAll"]//dl[position()<41]/dt/a/@href',
            '//div[@id="content"]/dl//a/@href',
            '//div[contains(@id, "category")]//a[not(contains(@href, "lastpost"))]/@href',
            '//ul[@id="itemContainer"]/li[position()<41]/a/@href',
            '//ul[@id="listAll"]/li[position()<41]/h3/a/@href',
            '//div[@id="listAll"]//p/a/@href',
            '//ul[@id="newsList"]/li[position()<41][@class="listitem"]/a/@href'
        ]
        for xpath_rule in xpath_rules:
            result = response.xpath(xpath_rule).extract()
            if len(result) > 0:
                print url,xpath_rule,len(result)
                return xpath_rule
        print '-'*100
        print '需要新规则 ', url
        print '-'*100

    def parse_link(self, response):
        if response.meta.get('parse_json'):
            jsonDict = json.loads(response.body)['obj']['content']
            for info in jsonDict:
                url = info['selfUrl']
                final_url = urlparse.urljoin(response.url, '/con/{}'.format(url))
                yield Request(url=final_url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_item)
        else:
            xpath_rule = self.get_parse_link_urls(response, response.url)
            data_list = response.xpath(xpath_rule).extract()
            for url in data_list:
                url = urlparse.urljoin(response.url, url)
                if response.meta['ba_type'] == 'forum' and 'dahe.cn' in url:
                    print url
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_forum_link)
                elif 'dahe.cn' in url and not re.search(r'dahe\.cn/200\d/', url) and 'jdms.dahe.cn' not in url:
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type']},callback=self.parse_item)

    def parse_newspaper_link(self, response):
        data_list = response.xpath('//div[@id="btdh"]//table//tr/td/a')
        medianame = response.xpath('//head/title/text()').extract()[0]
        for data in data_list:
            url = data.xpath('./@href').extract()[0]
            title = ''.join(data.xpath('.//text()').extract())
            url = urlparse.urljoin(response.url, url)
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'title':title,'medianame':medianame},callback=self.parse_item)
        if self.history and response.meta['page_parse']:
            page_rule = response.xpath('//a[@id="pageLink"][not(@class)]/@href').extract()
            for page in page_rule:
                url = urlparse.urljoin(response.url, page)
                if url != response.url:
                    yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'page_parse':False},callback=self.parse_newspaper_link)

    def parse_forum_link(self, response):
        data_list = response.xpath('//table[contains(@summary, "forum_2")]/script/following-sibling::tbody/tr/td/a[not(@title)]/@href').extract()
        for url in data_list:
            url = urlparse.urljoin(response.url, url)
            medianame = response.xpath('/html/head/title/text()').extract()[0].replace(' ','').replace(u'-河南最大社情民意平台', '')
            # print url
            yield Request(url=url,method='get',meta={'ba_type':response.meta['ba_type'],'medianame':medianame},callback=self.parse_item)

    def parse_item(self, response):
        item = DataItem()
        item["type"] = response.meta["ba_type"]
        item['area'] = u'河南省'
        item['source'] = self.source
        item['collecttime'] = time.strftime('%Y-%m-%d %H:%M')
        item['url'] = response.url

        medianame = response.meta.get('medianame')
        medianame1 = response.xpath('//h1/../div[1]/p[2]/text()').extract() or \
                     response.xpath('//span[@class="subtime"][@id]/following-sibling::span[1]/text()').extract() or \
                     response.xpath('//div[@class="detail-content"]/section/section[7]/section/section/p/text()').extract() or \
                     response.xpath('//*[@id="top"]/article/header/div/p/span/text()').extract() or \
                     response.xpath('//i[@id="pubtime_baidu"]/following-sibling::span/text()').extract() or \
                     response.xpath('//*[@id="source_baidu"]/text()').extract() or \
                     response.xpath('//div[@class="newstitle"]/following-sibling::div[@id="news-l4"]/text()').extract() or \
                     response.xpath('//p[@id="pubtime_baidu"]/following-sibling::p[1]/text()').extract() or \
                     response.xpath('//div[@class="xinwen"]/div[1]/p/small/span/text()').extract()
        if medianame:
            item['medianame'] = medianame.strip()
        elif len(medianame1) > 0:
            item['medianame'] = re.search(ur'来?源?[:：]?\s?([^)\s]+)', medianame1[0].strip()).group(1)
        else:
            item['medianame'] = u'大河网'

        pubtime = response.xpath('//*[@id="con1"]/div[2]/div[3]/strong/text()').extract() or \
                  response.xpath('//h1/../div[1]/p[1]/text()').extract() or \
                  response.xpath('//div[contains(@class, "detail-title")]/div/div[1]/span[1]/text()').extract() or \
                  response.xpath('//span[@class="subtime"][@id]/text()').extract() or \
                  response.xpath('//div[@class="article"]/p[1]/span[1]/text()').extract() or \
                  response.xpath('//*[@id="top"]/article/header/div/p/text()').extract() or \
                  response.xpath('//*[@id="pubtime_baidu"]/text()').extract() or \
                  response.xpath('//em[contains(@id, "authorposton")]/span/@title').extract() or \
                  response.xpath('//em[contains(@id, "authorposton")]/text()').extract() or \
                  response.xpath('//div[@class="newstitle"]/following-sibling::div[@id="news-l4"]/text()').extract() or \
                  response.xpath('//div[@class="xinwen"]/div[1]/p/small/text()[1]').extract() or \
                  response.xpath('//div[@class="detail-box"]/div[1]/div[1]/div[1]/span[1]/text()').extract()
        print pubtime, response.url
        final_pubtime1 = re.search(r'20\d{2}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
        final_pubtime2 = re.search(r'20\d{2}-\d{1,2}-\d{1,2}\d{1,2}:\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
        final_pubtime3 = re.search(r'20\d{2}-\d{1,2}-\d{1,2}', pubtime[0].replace(u'年', '-').replace(u'月', '-').replace(u'日', ''))
        if final_pubtime1:
            item['pubtime'] = datetime.datetime.strptime(final_pubtime1.group(), "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
        elif final_pubtime2:
            item['pubtime'] = datetime.datetime.strptime(final_pubtime2.group(), "%Y-%m-%d%H:%M").strftime('%Y-%m-%d %H:%M')
        elif final_pubtime3:
            item['pubtime'] = datetime.datetime.strptime(final_pubtime3.group(), "%Y-%m-%d").strftime('%Y-%m-%d %H:%M')

        title = response.xpath('//div[@class="newsleft"]/h1/text()').extract() or \
                response.xpath('//div[contains(@class, "detail-title")]/p/text()').extract() or \
                response.xpath('//div[@class="container"]/h1/text()').extract() or \
                response.xpath('//header[@class="newsTitle"]/h1/text()').extract() or \
                response.xpath('//div[@class="xinwen"]/div[1]/h2/text()').extract() or \
                response.xpath('//h1/span[@id="thread_subject"]/text()').extract() or \
                response.xpath('//div[@id="article"]//h1/text()').extract() or \
                response.xpath('//*[@id="4g_title"]/text()').extract() or \
                response.xpath('//div[@class="newstitle"]/text()').extract() or \
                response.xpath('//div[@class="detail-box"]/div[1]/p/text()').extract()
        title1 = ''.join(response.xpath('//h1/table//tr/text()').extract())
        # print title,' titel1: ', title1, response.meta.get('title')
        if len(title) > 0:
            item['title'] = title[0].strip()
        else:
            item['title'] = title1 or response.meta.get('title')

        content = response.xpath('//div[@class="dContents"]').extract() or \
                  response.xpath('//div[@class="newscontent"]').extract() or \
                  response.xpath('//div[@class="detail-content"]').extract() or \
                  response.xpath('//div[@class="article"]').extract() or \
                  response.xpath('//*[@id="top"]/article/section').extract() or \
                  response.xpath('//div[@id="mainCon"]').extract() or \
                  response.xpath('//div[@class="pct"]').extract() or \
                  response.xpath('//div[@id="article"]').extract() or \
                  response.xpath('//div[@id="mainCon"]').extract() or \
                  response.xpath('//div[@class="newstitle"]/..').extract() or \
                  response.xpath('//div[@class="xinwen"]').extract()
        item['content'] = content[0]

        if item['pubtime'] and item['title'] and item['content'] and item['medianame']:
            yield item
        else:
            print item['url']
            print '字段缺失: {}, {}, {}'.format(item['title'], item['pubtime'], item['content'][:11])

